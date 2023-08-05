#    Copyright 2018 - 2019 Alexey Stepanov aka penguinolog.

#    Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Execution result."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

# Standard Library
import datetime
import json
import logging
import threading
import typing


# External Dependencies
import defusedxml.ElementTree  # type: ignore
import six
import yaml

# Exec-Helpers Implementation
from exec_helpers import exceptions
from exec_helpers import proc_enums

try:
    import lxml.etree  # type: ignore  # nosec
except ImportError:
    lxml = None  # pylint: disable=invalid-name

if typing.TYPE_CHECKING:
    import xml.etree.ElementTree  # nosec  # noqa  # pylint: disable=unused-import

__all__ = ("ExecResult",)

logger = logging.getLogger(__name__)


def _get_str_from_bin(src):  # type: (bytearray) -> str
    """Join data in list to the string.

    :param src: source to process
    :type src: bytearray
    :return: decoded string
    :rtype: str
    """
    return src.strip().decode(encoding="utf-8", errors="backslashreplace")


def _get_bytearray_from_array(src):  # type: (typing.Iterable[bytes]) -> bytearray
    """Get bytearray from array of bytes blocks.

    :param src: source to process
    :type src: typing.List[bytes]
    :return: bytearray
    :rtype: bytearray
    """
    return bytearray(b"".join(src))


class LinesAccessProxy(object):
    """Lines access proxy."""

    __slots__ = ("_data",)

    def __init__(self, data):  # type: (typing.Sequence[bytes]) -> None
        """Lines access proxy.

        :param data: data to work with.
        :type data: typing.Sequence[bytes]
        """
        self._data = tuple(data)  # type: typing.Tuple[bytes, ...]

    def __getitem__(
        self, item
    ):  # type: (typing.Union[int, slice, typing.Iterable[typing.Union[int, slice, "ellipsis"]]]) -> typing.Text
        """Access magic.

        :param item: index
        :type item: typing.Union[int, slice, typing.Iterable[typing.Union[int, slice, ellipsis]]]
        :returns: Joined selected lines
        :rtype: str
        :raises TypeError: Unexpected key
        """
        if isinstance(item, six.integer_types):
            return _get_str_from_bin(_get_bytearray_from_array([self._data[item]]))
        if isinstance(item, slice):
            return _get_str_from_bin(_get_bytearray_from_array(self._data[item]))
        if isinstance(item, tuple):
            buf = []  # type: typing.List[bytes]
            for rule in item:
                if isinstance(rule, six.integer_types):
                    buf.append(self._data[rule])
                elif isinstance(rule, slice):
                    buf.extend(self._data[rule])
                elif rule is Ellipsis:
                    buf.append(b"...\n")
                else:
                    raise TypeError("Unexpected key type: {rule!r} (from {item!r})".format(rule=rule, item=item))
            return _get_str_from_bin(_get_bytearray_from_array(buf))
        raise TypeError("Unexpected key type: {item!r}".format(item=item))

    def __len__(self):  # type: () -> int  # pragma: no cover
        """Data len."""
        return len(self._data)

    def __unicode__(self):  # type: () -> typing.Text  # pragma: no cover
        """Get string for debug purposes."""
        return self[:]

    def __repr__(self):  # type: () -> typing.Text
        """Repr for debug purposes."""
        return "{cls}(data={self._data!r})".format(cls=self.__class__.__name__, self=self)


class ExecResult(object):
    """Execution result."""

    __slots__ = [
        "__cmd",
        "__stdin",
        "_stdout",
        "_stderr",
        "__exit_code",
        "__timestamp",
        "_stdout_str",
        "_stderr_str",
        "_stdout_brief",
        "_stderr_brief",
        "__stdout_lock",
        "__stderr_lock",
        "__started",
    ]

    def __init__(
        self,
        cmd,  # type: typing.Union[str, typing.Text]
        stdin=None,  # type: typing.Union[bytes, str, bytearray, None]
        stdout=None,  # type: typing.Optional[typing.Iterable[bytes]]
        stderr=None,  # type: typing.Optional[typing.Iterable[bytes]]
        exit_code=proc_enums.INVALID,  # type: typing.Union[int, proc_enums.ExitCodes]
        started=None,  # type: typing.Optional[datetime.datetime]
    ):  # type: (...) -> None
        """Command execution result.

        :param cmd: command
        :type cmd: str
        :param stdin: string STDIN
        :type stdin: typing.Union[bytes, str, bytearray, None]
        :param stdout: binary STDOUT
        :type stdout: typing.Optional[typing.Iterable[bytes]]
        :param stderr: binary STDERR
        :type stderr: typing.Optional[typing.Iterable[bytes]]
        :param exit_code: Exit code. If integer - try to convert to BASH enum.
        :type exit_code: typing.Union[int, proc_enums.ExitCodes]
        :param started: Timestamp of command start
        :type started: typing.Optional[datetime.datetime]
        """
        self.__stdout_lock = threading.RLock()
        self.__stderr_lock = threading.RLock()

        self.__cmd = cmd
        if isinstance(stdin, six.binary_type):
            self.__stdin = _get_str_from_bin(bytearray(stdin))  # type: typing.Optional[typing.Text]
        elif isinstance(stdin, bytearray):
            self.__stdin = _get_str_from_bin(stdin)
        else:
            self.__stdin = stdin

        if stdout is not None:
            self._stdout = tuple(stdout)  # type: typing.Tuple[bytes, ...]
        else:
            self._stdout = ()

        if stderr is not None:
            self._stderr = tuple(stderr)  # type: typing.Tuple[bytes, ...]
        else:
            self._stderr = ()

        self.__exit_code = proc_enums.INVALID  # type: typing.Union[int, proc_enums.ExitCodes]
        self.__timestamp = None  # type: typing.Optional[datetime.datetime]
        self.exit_code = exit_code

        self.__started = started  # type: typing.Optional[datetime.datetime]

        # By default is none:
        self._stdout_str = None  # type: typing.Optional[typing.Text]
        self._stderr_str = None  # type: typing.Optional[typing.Text]
        self._stdout_brief = None  # type: typing.Optional[typing.Text]
        self._stderr_brief = None  # type: typing.Optional[typing.Text]

    @property
    def stdout_lock(self):  # type: () -> threading.RLock
        """Lock object for thread-safe operation.

        :return: internal lock for stdout
        :rtype: threading.RLock

        .. versionadded:: 1.9.0
        """
        return self.__stdout_lock

    @property
    def stderr_lock(self):  # type: () -> threading.RLock
        """Lock object for thread-safe operation.

        :return: internal lock for stderr
        :rtype: threading.RLock

        .. versionadded:: 1.9.0
        """
        return self.__stderr_lock

    @property
    def timestamp(self):  # type: () -> typing.Optional[datetime.datetime]
        """Timestamp.

        :return: exit code timestamp
        :rtype: typing.Optional[datetime.datetime]
        """
        return self.__timestamp

    def set_timestamp(self):  # type: () -> None
        """Set timestamp if empty.

        This will block future object changes.

        .. versionadded:: 1.11.0
        """
        if self.timestamp is None:
            self.__timestamp = datetime.datetime.utcnow()

    @classmethod
    def _get_brief(cls, data):  # type: (typing.Tuple[bytes, ...]) -> typing.Text
        """Get brief output: 7 lines maximum (3 first + ... + 3 last).

        :param data: source to process
        :type data: typing.Tuple[bytes, ...]
        :return: brief from source
        :rtype: str
        """
        if len(data) <= 7:
            return _get_str_from_bin(_get_bytearray_from_array(data))
        return LinesAccessProxy(data)[:3, ..., -3:]

    @property
    def cmd(self):  # type: () -> typing.Text
        """Executed command.

        :rtype: str
        """
        return self.__cmd

    @property
    def stdin(self):  # type: () -> typing.Optional[typing.Text]
        """Stdin input as string.

        :rtype: typing.Optional[typing.Text]
        """
        return self.__stdin

    @property
    def stdout(self):  # type: () -> typing.Tuple[bytes, ...]
        """Stdout output as list of binaries.

        :rtype: typing.Tuple[bytes, ...]
        """
        return self._stdout

    @property
    def stderr(self):  # type: () -> typing.Tuple[bytes, ...]
        """Stderr output as list of binaries.

        :rtype: typing.Tuple[bytes, ...]
        """
        return self._stderr

    @staticmethod
    def _poll_stream(
        src,  # type: typing.Iterable[bytes]
        log=None,  # type: typing.Optional[logging.Logger]
        verbose=False,  # type: bool
    ):  # type: (...) -> typing.List[bytes]
        dst = []  # type: typing.List[bytes]
        try:
            for line in src:
                dst.append(line)
                if log:
                    log.log(
                        level=logging.INFO if verbose else logging.DEBUG,
                        msg=line.decode("utf-8", errors="backslashreplace").rstrip(),
                    )
        except IOError:
            pass
        return dst

    def read_stdout(
        self,
        src=None,  # type: typing.Optional[typing.Iterable[bytes]]
        log=None,  # type: typing.Optional[logging.Logger]
        verbose=False,  # type: bool
    ):  # type: (...) -> None
        """Read stdout file-like object to stdout.

        :param src: source
        :type src: typing.Optional[typing.Iterable]
        :param log: logger
        :type log: typing.Optional[logging.Logger]
        :param verbose: use log.info instead of log.debug
        :type verbose: bool
        :raises RuntimeError: Exit code is already received

        .. versionchanged:: 1.2.0 - src can be None
        """
        if not src:
            return
        if self.timestamp:
            raise RuntimeError("Final exit code received.")

        with self.stdout_lock:
            self._stdout_str = self._stdout_brief = None
            self._stdout += tuple(self._poll_stream(src, log, verbose))

    def read_stderr(
        self,
        src=None,  # type: typing.Optional[typing.Iterable[bytes]]
        log=None,  # type: typing.Optional[logging.Logger]
        verbose=False,  # type: bool
    ):  # type: (...) -> None
        """Read stderr file-like object to stdout.

        :param src: source
        :type src: typing.Optional[typing.Iterable]
        :param log: logger
        :type log: typing.Optional[logging.Logger]
        :param verbose: use log.info instead of log.debug
        :type verbose: bool
        :raises RuntimeError: Exit code is already received

        .. versionchanged:: 1.2.0 - src can be None
        """
        if not src:
            return
        if self.timestamp:
            raise RuntimeError("Final exit code received.")

        with self.stderr_lock:
            self._stderr_str = self._stderr_brief = None
            self._stderr += tuple(self._poll_stream(src, log, verbose))

    @property
    def stdout_bin(self):  # type: () -> bytearray
        """Stdout in binary format.

        Sometimes logging is used to log binary objects too (example: Session),
        and for debug purposes we can use this as data source.
        :rtype: bytearray
        """
        with self.stdout_lock:
            return _get_bytearray_from_array(self.stdout)

    @property
    def stderr_bin(self):  # type: () -> bytearray
        """Stderr in binary format.

        :rtype: bytearray
        """
        with self.stderr_lock:
            return _get_bytearray_from_array(self.stderr)

    @property
    def stdout_str(self):  # type: () -> typing.Text
        """Stdout output as string.

        :rtype: str
        """
        with self.stdout_lock:
            if self._stdout_str is None:
                self._stdout_str = _get_str_from_bin(self.stdout_bin)
            return self._stdout_str

    @property
    def stderr_str(self):  # type: () -> typing.Text
        """Stderr output as string.

        :rtype: str
        """
        with self.stderr_lock:
            if self._stderr_str is None:
                self._stderr_str = _get_str_from_bin(self.stderr_bin)
            return self._stderr_str

    @property
    def stdout_brief(self):  # type: () -> typing.Text
        """Brief stdout output (mostly for exceptions).

        :rtype: str
        """
        with self.stdout_lock:
            if self._stdout_brief is None:
                self._stdout_brief = self._get_brief(self.stdout)
            return self._stdout_brief

    @property
    def stderr_brief(self):  # type: () -> typing.Text
        """Brief stderr output (mostly for exceptions).

        :rtype: str
        """
        with self.stderr_lock:
            if self._stderr_brief is None:
                self._stderr_brief = self._get_brief(self.stderr)
            return self._stderr_brief

    @property
    def stdout_lines(self):  # type: () -> LinesAccessProxy
        """Get lines by indexes.

        :rtype: LinesAccessProxy

        Usage example:

        .. code-block::python

            res.stdout_lines[<line_number>, <index_start>:<index_end>, ...]
        """
        return LinesAccessProxy(self.stdout)

    @property
    def stderr_lines(self):  # type: () -> LinesAccessProxy
        """Magic to get lines human-friendly way."""
        return LinesAccessProxy(self.stderr)

    @property
    def exit_code(self):  # type: () -> typing.Union[int, proc_enums.ExitCodes]
        """Return(exit) code of command.

        :return: exit code
        :rtype: typing.Union[int, proc_enums.ExitCodes]
        """
        return self.__exit_code

    @exit_code.setter
    def exit_code(self, new_val):  # type: (typing.Union[int, proc_enums.ExitCodes]) -> None
        """Return(exit) code of command.

        :param new_val: new exit code
        :type new_val: typing.Union[int, proc_enums.ExitCodes]
        :raises RuntimeError: Exit code is already received
        :raises TypeError: exit code is not int instance

        If valid exit code is set - object became read-only.
        """
        if self.timestamp:
            raise RuntimeError("Exit code is already received.")
        if not isinstance(new_val, (six.integer_types, proc_enums.ExitCodes)):
            raise TypeError("Exit code is strictly int, received: {code!r}".format(code=new_val))
        with self.stdout_lock, self.stderr_lock:
            self.__exit_code = proc_enums.exit_code_to_enum(new_val)
            if self.__exit_code != proc_enums.INVALID:
                self.__timestamp = datetime.datetime.utcnow()

    @property
    def started(self):  # type: () -> typing.Optional[datetime.datetime]
        """Timestamp of command start.

        .. versionadded:: 1.11.0
        """
        return self.__started

    def __deserialize(self, fmt):  # type: (typing.Text) -> typing.Any
        """Deserialize stdout as data format.

        :param fmt: format to decode from
        :type fmt: str
        :return: decoded object
        :rtype: typing.Any
        :raises NotImplementedError: fmt deserialization not implemented
        :raises DeserializeValueError: Not valid source format
        """
        try:
            if fmt == "json":
                return json.loads(self.stdout_str, encoding="utf-8")
            if fmt == "yaml":
                if yaml.__with_libyaml__:
                    return yaml.load(self.stdout_str, Loader=yaml.CSafeLoader)  # nosec  # Safe
                return yaml.safe_load(self.stdout_str)
            if fmt == "xml":
                return defusedxml.ElementTree.fromstring(bytes(self.stdout_bin))
            if fmt == "lxml":
                return lxml.etree.fromstring(bytes(self.stdout_bin))  # nosec
        except Exception:
            tmpl = " stdout is not valid {fmt}:\n" "{{stdout!r}}\n".format(fmt=fmt)
            logger.exception(self.cmd + tmpl.format(stdout=self.stdout_str))
            raise exceptions.DeserializeValueError(self.cmd + tmpl.format(stdout=self.stdout_brief))
        msg = "{fmt} deserialize target is not implemented".format(fmt=fmt)
        logger.error(msg)
        raise NotImplementedError(msg)

    @property
    def stdout_json(self):  # type: () -> typing.Any
        """JSON from stdout.

        :rtype: typing.Any
        :raises DeserializeValueError: STDOUT can not be deserialized as JSON
        """
        with self.stdout_lock:
            return self.__deserialize(fmt="json")

    @property
    def stdout_yaml(self):  # type: () -> typing.Any
        """YAML from stdout.

        :rtype: typing.Any
        :raises DeserializeValueError: STDOUT can not be deserialized as YAML
        """
        with self.stdout_lock:
            return self.__deserialize(fmt="yaml")

    @property
    def stdout_xml(self):  # type: () -> xml.etree.ElementTree.Element
        """XML from stdout.

        :rtype: xml.etree.ElementTree.Element
        :raises DeserializeValueError: STDOUT can not be deserialized as XML
        """
        with self.stdout_lock:
            return self.__deserialize(fmt="xml")  # type: ignore

    @property
    def stdout_lxml(self):  # type: () -> "lxml.etree.Element"
        """XML from stdout using lxml.

        :rtype: lxml.etree.Element
        :raises DeserializeValueError: STDOUT can not be deserialized as XML
        :raises AttributeError: lxml is not installed

        .. note:: Can be insecure.
        """
        if lxml is None:
            raise AttributeError("lxml is not installed -> attribute is not functional.")
        with self.stdout_lock:
            return self.__deserialize(fmt="lxml")

    def __dir__(self):  # type: () -> typing.List[typing.Text]
        """Override dir for IDE and as source for getitem checks."""
        content = [
            "cmd",
            "stdout",
            "stderr",
            "exit_code",
            "stdout_bin",
            "stderr_bin",
            "stdout_str",
            "stderr_str",
            "stdout_brief",
            "stderr_brief",
            "stdout_lines",
            "stderr_lines",
            "stdout_json",
            "stdout_yaml",
            "stdout_xml",
            "lock",
        ]
        if lxml is not None:
            content.append("stdout_lxml")
        return content

    def __getitem__(self, item):  # type: (typing.Union[str, typing.Text]) -> typing.Any
        """Dict like get data.

        :param item: key
        :type item: str
        :return: item if attribute exists
        :rtype: typing.Any
        :raises IndexError: no attribute exists or not allowed to get (not in dir())
        """
        if item in dir(self):
            return getattr(self, item)
        raise IndexError('"{item}" not found in {dir}'.format(item=item, dir=dir(self)))

    def __repr__(self):  # type: () -> str
        """Representation for debugging."""
        if self.started:
            started = ", started={self.started},\n".format(self=self)
        else:
            started = ""
        return (
            "{cls}(cmd={self.cmd!r}, stdout={self.stdout}, stderr={self.stderr}, "
            "exit_code={self.exit_code!s}{started},)".format(cls=self.__class__.__name__, self=self, started=started)
        )

    def __str__(self):  # type: () -> str
        """Representation for logging."""
        if self.started:
            started = "\tstarted={started},\n".format(started=self.started.strftime("%Y-%m-%d %H:%M:%S"))
            if self.timestamp:
                _spent = (self.timestamp - self.started).seconds
                spent = "\tspent={hours:02d}:{minutes:02d}:{seconds:02d},\n".format(
                    hours=_spent // (60 * 60), minutes=_spent // 60, seconds=_spent % 60
                )
            else:
                spent = ""
        else:
            started = ""
            spent = ""
        return (
            "{cls}(\n\tcmd={cmd!r},"
            "\n\tstdout=\n'{stdout_brief}',"
            "\n\tstderr=\n'{stderr_brief}',"
            "\n\texit_code={exit_code!s},"
            "\n{started}{spent})".format(
                cls=self.__class__.__name__,
                cmd=self.cmd,
                stdout_brief=self.stdout_brief,
                stderr_brief=self.stderr_brief,
                exit_code=self.exit_code,
                started=started,
                spent=spent,
            )
        )

    def __eq__(self, other):  # type: (typing.Any) -> bool
        """Comparision."""
        return (
            self.__class__ is other.__class__
            or issubclass(self.__class__, other.__class__)
            or issubclass(other.__class__, self.__class__)
        ) and (
            self.cmd == other.cmd
            and self.stdin == other.stdin
            and self.stdout == other.stdout
            and self.stderr == other.stderr
            and self.exit_code == other.exit_code
        )

    def __ne__(self, other):  # type: (typing.Any) -> bool
        """Comparision."""
        return not self.__eq__(other)

    def __hash__(self):  # type: () -> int
        """Hash for usage as dict key and in sets."""
        return hash((self.__class__, self.cmd, self.stdin, self.stdout, self.stderr, self.exit_code))
