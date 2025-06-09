"""
Burin PyTest Fixtures and Hooks

Copyright (c) 2025 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
import inspect

# PyTest imports
import pytest

# Burin import
import burin


# Basic testing values
recordArgs = ()
recordLevel = burin.INFO
recordLineNumber = 10
recordMessage = "This is a log message"
recordName = "TestRecord"
recordPathname = "/test/path"


class LineIncrementFilter(burin.BurinFilter):
    """
    Returns a new record instance with an incremented line number.

    This is purely for testing modification filters within a filterer.
    """

    def filter(self, record):
        """
        Creates a new record instance with an incremented line number.

        :param record: The record to alter.
        :type record: BurinLogRecord
        :returns: A new record instance with an incremented line number.
        :rtype: BurinLogRecord
        """

        return burin.BurinLogRecord(record.name, record.levelno, record.pathname, record.lineno + 1,
                                    record.msg, record.args,record.exc_info, record.funcName,
                                    record.stack_info, **record.kwargs)


@pytest.fixture(scope="session")
def basic_file_handler():
    """
    Creates a factory for a basic file handler.
    """

    handlerSig = inspect.signature(burin.BurinFileHandler)
    handlerParams = handlerSig.parameters

    def _basic_file_handler(filename, mode=handlerParams["mode"].default,
                            encoding=handlerParams["encoding"].default,
                            delay=handlerParams["delay"].default,
                            errors=handlerParams["errors"].default,
                            level=handlerParams["level"].default):
        """
        Factory for creating a file handler.
        """

        return burin.BurinFileHandler(filename, mode, encoding, delay, errors,
                                      level)

    return _basic_file_handler

@pytest.fixture(scope="session")
def basic_filterer():
    """
    Creates a factory for a basic filterer instance.
    """

    def _basic_filterer():
        """
        Factory for creating a filterer.
        """

        return burin.BurinFilterer()

    return _basic_filterer

@pytest.fixture(scope="session")
def basic_handler():
    """
    Creates a factory for a basic handler.
    """

    handlerSig = inspect.signature(burin.BurinHandler)
    handlerParams = handlerSig.parameters

    def _basic_handler(level=handlerParams["level"].default):
        """
        Factory for creating a handler.
        """

        return burin.BurinHandler(level)

    return _basic_handler

@pytest.fixture(scope="session")
def basic_record():
    """
    Creates a factory for a basic log record.
    """

    def _basic_record(name=recordName, level=recordLevel,
                      pathname=recordPathname, lineno=recordLineNumber,
                      msg=recordMessage, args=recordArgs,
                      exc_info=None, func=None, sinfo=None, **kwargs):
        """
        Factory for creating a log record.
        """

        return burin.BurinLogRecord(name, level, pathname, lineno, msg, args,
                                    exc_info, func, sinfo, **kwargs)

    return _basic_record

@pytest.fixture(scope="session")
def basic_stream_handler():
    """
    Creates a factory for a basic stream handler.
    """

    handlerSig = inspect.signature(burin.BurinStreamHandler)
    handlerParams = handlerSig.parameters

    def _basic_stream_handler(stream=handlerParams["stream"].default,
                              level=handlerParams["level"].default):
        """
        Factory for creating a stream handler.
        """

        return burin.BurinStreamHandler(stream, level)

    return _basic_stream_handler

@pytest.fixture(scope="session")
def line_increment_filter():
    """
    Creates a factory for a filter that increments a record's line number.
    """

    def _line_increment_filter():
        """
        Factory for creating a filter that increments a record's line number.
        """

        return LineIncrementFilter()

    return _line_increment_filter
