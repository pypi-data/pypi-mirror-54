#    Copyright 2018 Alexey Stepanov aka penguinolog.
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

"""Package specific exceptions."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

# Standard Library
import typing

# Exec-Helpers Implementation
from exec_helpers import proc_enums

if typing.TYPE_CHECKING:  # pragma: no cover
    from exec_helpers import exec_result  # noqa: F401  # pylint: disable=cyclic-import, unused-import

__all__ = (
    "ExecHelperError",
    "ExecHelperNoKillError",
    "ExecHelperTimeoutError",
    "ExecCalledProcessError",
    "CalledProcessError",
    "ParallelCallProcessError",
    "ParallelCallExceptions",
)


class ExecHelperError(Exception):
    """Base class for all exceptions raised inside."""

    __slots__ = ()


class DeserializeValueError(ExecHelperError, ValueError):
    """Deserialize impossible."""

    __slots__ = ()


class ExecCalledProcessError(ExecHelperError):
    """Base class for process call errors."""

    __slots__ = ()


class ExecHelperTimeoutProcessError(ExecCalledProcessError):
    """Timeout based errors."""

    __slots__ = ("result", "timeout")

    def __init__(
        self, message, result, timeout
    ):  # type: (typing.Union[str, typing.Text], exec_result.ExecResult, typing.Union[int, float]) -> None
        """Exception for error on process calls.

        :param message: exception message
        :type message: str
        :param result: execution result
        :type result: exec_result.ExecResult
        :param timeout: timeout for command
        :type timeout: typing.Union[int, float]
        """
        super(ExecHelperTimeoutProcessError, self).__init__(message)
        self.result = result
        self.timeout = timeout

    @property
    def cmd(self):  # type: () -> typing.Union[str, typing.Text]
        """Failed command."""
        return self.result.cmd

    @property
    def stdout(self):  # type: () -> typing.Text
        """Command stdout."""
        return self.result.stdout_str

    @property
    def stderr(self):  # type: () -> typing.Text
        """Command stderr."""
        return self.result.stderr_str


class ExecHelperNoKillError(ExecHelperTimeoutProcessError):
    """Impossible to kill process.

    .. versionadded:: 1.10.0
    """

    __slots__ = ()

    def __init__(self, result, timeout):  # type: (exec_result.ExecResult, typing.Union[int, float]) -> None
        """Exception for error on process calls.

        :param result: execution result
        :type result: exec_result.ExecResult
        :param timeout: timeout for command
        :type timeout: typing.Union[int, float]
        """
        stdout_brief = result.stdout_brief.encode(encoding="utf-8", errors="backslashreplace").decode("utf-8")
        stderr_brief = result.stderr_brief.encode(encoding="utf-8", errors="backslashreplace").decode("utf-8")
        message = (
            "Wait for {result.cmd!r} during {timeout!s}s: no return code and no response on SIGTERM + SIGKILL signals!"
            "\n"
            "\tSTDOUT:\n"
            "{stdout_brief}\n"
            "\tSTDERR:\n"
            "{stderr_brief}".format(
                result=result, timeout=timeout, stdout_brief=stdout_brief, stderr_brief=stderr_brief
            )
        )
        super(ExecHelperNoKillError, self).__init__(message, result=result, timeout=timeout)


def make_timeout_error_message(
    result, timeout
):  # type: (exec_result.ExecResult, typing.Union[int, float]) -> typing.Text
    """Make timeout failed message."""
    stdout_brief = result.stdout_brief.encode(encoding="utf-8", errors="backslashreplace").decode("utf-8")
    stderr_brief = result.stderr_brief.encode(encoding="utf-8", errors="backslashreplace").decode("utf-8")
    return (
        "Wait for {result.cmd!r} during {timeout!s}s: no return code!\n"
        "\tSTDOUT:\n"
        "{stdout_brief}\n"
        "\tSTDERR:\n"
        "{stderr_brief}".format(result=result, timeout=timeout, stdout_brief=stdout_brief, stderr_brief=stderr_brief)
    )


class ExecHelperTimeoutError(ExecHelperTimeoutProcessError):
    """Execution timeout.

    .. versionchanged:: 1.3.0 provide full result and timeout inside.
    .. versionchanged:: 1.3.0 subclass ExecCalledProcessError
    """

    __slots__ = ()

    def __init__(self, result, timeout):  # type: (exec_result.ExecResult, typing.Union[int, float]) -> None
        """Exception for error on process calls.

        :param result: execution result
        :type result: exec_result.ExecResult
        :param timeout: timeout for command
        :type timeout: typing.Union[int, float]
        """
        super(ExecHelperTimeoutError, self).__init__(
            make_timeout_error_message(result=result, timeout=timeout), result=result, timeout=timeout
        )


class CalledProcessError(ExecCalledProcessError):
    """Exception for error on process calls."""

    __slots__ = ("result", "expected")

    def __init__(
        self,
        result,  # type: exec_result.ExecResult
        expected=(proc_enums.EXPECTED,),  # type: typing.Iterable[typing.Union[int, proc_enums.ExitCodes]]
    ):  # type: (...) -> None
        """Exception for error on process calls.

        :param result: execution result
        :type result: exec_result.ExecResult
        :param expected: expected return codes
        :type expected: typing.Iterable[typing.Union[int, proc_enums.ExitCodes]]

        .. versionchanged:: 1.1.1 - provide full result
        .. versionchanged:: 1.10.0 Expected is not optional, defaults os dependent
        """
        self.result = result
        self.expected = proc_enums.exit_codes_to_enums(expected)
        stdout_brief = result.stdout_brief.encode(encoding="utf-8", errors="backslashreplace").decode("utf-8")
        stderr_brief = result.stderr_brief.encode(encoding="utf-8", errors="backslashreplace").decode("utf-8")
        message = (
            "Command {result.cmd!r} returned exit code {result.exit_code} "
            "while expected {expected}\n"
            "\tSTDOUT:\n"
            "{stdout_brief}\n"
            "\tSTDERR:\n"
            "{stderr_brief}".format(
                result=self.result, expected=self.expected, stdout_brief=stdout_brief, stderr_brief=stderr_brief
            )
        )
        super(CalledProcessError, self).__init__(message)

    @property
    def returncode(self):  # type: () -> typing.Union[int, proc_enums.ExitCodes]
        """Command return code."""
        return self.result.exit_code

    @property
    def cmd(self):  # type: () -> typing.Union[str, typing.Text]
        """Failed command."""
        return self.result.cmd

    @property
    def stdout(self):  # type: () -> typing.Text
        """Command stdout."""
        return self.result.stdout_str

    @property
    def stderr(self):  # type: () -> typing.Text
        """Command stderr."""
        return self.result.stderr_str


class ParallelCallProcessError(ExecCalledProcessError):
    """Exception during parallel execution."""

    __slots__ = ("cmd", "errors", "results", "expected")

    def __init__(
        self,
        command,  # type: typing.Union[str, typing.Text]
        errors,  # type: typing.Dict[typing.Tuple[typing.Union[str, typing.Text], int], exec_result.ExecResult]
        results,  # type: typing.Dict[typing.Tuple[typing.Union[str, typing.Text], int], exec_result.ExecResult]
        expected=(proc_enums.EXPECTED,),  # type: typing.Iterable[typing.Union[int, proc_enums.ExitCodes]]
        **kwargs  # type: typing.Any
    ):  # type: (...) -> None
        """Exception raised during parallel call as result of exceptions.

        :param command: command
        :type command: str
        :param errors: results with errors
        :type errors: typing.Dict[typing.Tuple[str, int], ExecResult]
        :param results: all results
        :type results: typing.Dict[typing.Tuple[str, int], ExecResult]
        :param expected: expected return codes
        :type expected: typing.Iterable[typing.Union[int, proc_enums.ExitCodes]]
        :param _message: message override
        :type _message: typing.Optional[str]

        .. versionchanged:: 1.10.0 Expected is not optional, defaults os dependent
        """
        prep_expected = proc_enums.exit_codes_to_enums(expected)
        message = kwargs.get("_message", None) or (
            "Command {cmd!r} "
            "returned unexpected exit codes on several hosts\n"
            "Expected: {expected}\n"
            "Got:\n"
            "\t{errors}".format(
                cmd=command,
                expected=prep_expected,
                errors="\n\t".join(
                    "{host}:{port} - {code} ".format(host=host, port=port, code=result.exit_code)
                    for (host, port), result in errors.items()
                ),
            )
        )
        super(ParallelCallProcessError, self).__init__(message)
        self.cmd = command
        self.errors = errors
        self.results = results
        self.expected = prep_expected


class ParallelCallExceptions(ParallelCallProcessError):
    """Exception raised during parallel call as result of exceptions."""

    __slots__ = ("cmd", "exceptions")

    def __init__(
        self,
        command,  # type: typing.Union[str, typing.Text]
        exceptions,  # type: typing.Dict[typing.Tuple[typing.Union[str, typing.Text], int], Exception]
        errors,  # type: typing.Dict[typing.Tuple[typing.Union[str, typing.Text], int], exec_result.ExecResult]
        results,  # type: typing.Dict[typing.Tuple[typing.Union[str, typing.Text], int], exec_result.ExecResult]
        expected=(proc_enums.EXPECTED,),  # type: typing.Tuple[typing.Union[int, proc_enums.ExitCodes], ...]
        **kwargs  # type: typing.Any
    ):  # type: (...) -> None
        """Exception during parallel execution.

        :param command: command
        :type command: str
        :param exceptions: Exceptions on connections
        :type exceptions: typing.Dict[typing.Tuple[str, int], Exception]
        :param errors: results with errors
        :type errors: typing.Dict[typing.Tuple[str, int], ExecResult]
        :param results: all results
        :type results: typing.Dict[typing.Tuple[str, int], ExecResult]
        :param expected: expected return codes
        :type expected: typing.Iterable[typing.Union[int, proc_enums.ExitCodes]]
        :param _message: message override
        :type _message: typing.Optional[str]

        .. versionchanged:: 1.10.0 Expected is not optional, defaults os dependent
        """
        prep_expected = proc_enums.exit_codes_to_enums(expected)
        message = kwargs.get("_message", None) or (
            "Command {cmd!r} "
            "during execution raised exceptions: \n"
            "\t{exceptions}".format(
                cmd=command,
                exceptions="\n\t".join(
                    "{host}:{port} - {exc} ".format(host=host, port=port, exc=exc)
                    for (host, port), exc in exceptions.items()
                ),
            )
        )
        super(ParallelCallExceptions, self).__init__(
            command=command, errors=errors, results=results, expected=prep_expected, _message=message
        )
        self.cmd = command
        self.exceptions = exceptions
