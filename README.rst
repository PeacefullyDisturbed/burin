|version-badge| |license-badge| |py-versions-badge| |github-check-badge| |coverage-badge| |docs-build-badge|

.. |version-badge| image:: https://img.shields.io/pypi/v/burin?color=007EC6
    :target: https://pypi.org/project/burin/
    :alt: PyPI - Release

.. |license-badge| image:: https://img.shields.io/pypi/l/burin
    :target: https://github.com/PeacefullyDisturbed/burin/blob/main/LICENSE
    :alt: License

.. |py-versions-badge| image:: https://img.shields.io/pypi/pyversions/burin?color=blue
    :target: https://pypi.org/project/burin/
    :alt: Python Versions

.. |github-check-badge| image:: https://img.shields.io/github/check-runs/PeacefullyDisturbed/burin/main?logo=github&label=main
    :target: https://github.com/PeacefullyDisturbed/burin/actions/workflows/push_check.yaml
    :alt: GitHub Actions Workflow Status

.. |coverage-badge| image:: https://codecov.io/gh/PeacefullyDisturbed/burin/graph/badge.svg?token=E76T93FQ5F
    :target: https://codecov.io/gh/PeacefullyDisturbed/burin
    :alt: Codecov Coverage Percentage

.. |docs-build-badge| image:: https://img.shields.io/readthedocs/burin
    :target: https://burin.readthedocs.io/en/latest/?badge=latest
    :alt: Read the Docs - Documentation Status

=====================
Burin Logging Utility
=====================

Burin (/ˈbyʊər ɪn, ˈbɜr-/byoor-in, bur-/) is a logging library that is meant to
add features and simplify usage compared to the Python standard library
``logging`` package.  It can be used as a direct replacement in most cases.

Full Burin documentation is available at `Read the Docs
<https://burin.readthedocs.io/>`_.

Currently Python 3.7, 3.8, 3.9, 3.10, 3.11, and 3.12 are all supported.  There
are no dependencies or additional requirements for Burin and it should work on
any platform that Python does.

.. warning::

    Python 3.7 support is deprecated and will be removed in a future release.

An important aspect of Burin is an easy migration that allows changing from the
``logging`` package to Burin without anything breaking in most use cases.
While class names may need to be changed this generally should work well.
Although some situations may require other small changes due to the added
features of Burin.

Using Burin to replace ``logging`` use in a program can be done gradually or
all at once.  Burin should not intefere with ``logging`` usage as its
internal references are all managed independently.  However; it's best to
ensure that they are not trying to log to the same file as this may cause
issues.

.. note::

    While some classes in Burin inherit from classes in the Python standard
    ``logging`` package they cannot be used interchangeably.

    Using classes from ``logging`` in Burin or vice-versa may cause
    exceptions or other issues.

.. note::

    Burin is still in early development and may change in backwards
    incompatible ways between minor release versions.  This should be rare as
    general compatibility with ``logging`` is desired to ease switching, but
    it is a good idea check the release notes when upgrading between minor
    (0.X.0) releases.

==========================
What's Different in Burin?
==========================

The following make up the current major differences compared to the Python
standard ``logging`` module.

* Extra arguments and changes to ``basic_config`` allow it to be used in
  more situations and when setting up common logging configurations.
* Built-in support for deferred formatting of ``str.format`` and
  ``string.Template`` style logging messages.
* Library level logging calls (eg. ``burin.log``) can specify a logger to
  use other than the root logger, so calling ``get_logger`` isn't necessary
  first.
* Logging features from newer versions of Python (eg. ``logAsyncioTasks`` in
  3.12) are implemented in Burin and
  available in all supported Python versions.
* Everything that should be needed is available at the top level of the
  library; no more extra imports of ``logging.handlers`` and
  ``logging.config``.
* Multiple log record factory classes are supported at the same time, and which
  is used can be set per logger instance to allow for greater customisation.
* ``BurinLoggerAdapter`` instances will merge *extra* values from logging
  calls with the pre-set values from instantiation; nesting built-in adapters
  can actually be useful now.
* All handlers within Burin support a *level* parameter during initialization
  so an extra call ``BurinHandler.set_level`` isn't needed.
* ``BurinSocketHandler`` and ``BurinDatagramHandler`` by default will use
  pickling protocol version **4** instead of **1**.  This can be set to a
  different protocol version when creating the handler.
* ``BurinTimedRotatingFileHandler`` treats midnight as the start of a day
  rather than the end of a day.
* ``BurinSMTPHandler`` supports ``ssl.SSLContext`` objects for its
  *secure* parameter, and will also use *secure* to established an encrypted
  connection even if no credentials are specified.
* All methods and functions are *underscore_separated*, but *camelCase* aliases
  are available for an easier transition from the standard library.
* Logging configuration attributes ``logMultiproccessing``, ``logProcesses``,
  ``logThreads``, and ``raiseExceptions`` are on a ``burin.config`` object
  instead of directly on the module.
* Deprecated methods such as ``fatal`` and ``warn`` are not implemented.

There are several other differences which are more minor or are internal to
Burin and not documented in this list.  If you are going to create subclasses
or use internal classes and methods, then just make sure to read the
documentation or docstrings within the code.

====================
What Can't Burin Do?
====================

Burin is still in early development and does not yet support some use cases
that are supported by Python ``logging``.  These features are planned to
be implemented before Burin reaches its first stable major (1.0.0) release.

* Advanced configuration functions like those from ``logging.config``
  (``dictConfig``, ``fileConfig``, and ``listen``) are not yet implemented.
* Custom log levels are not yet supported.

===========
Using Burin
===========

Below are a few examples of using the features of Burin.  Read through the rest
of the documentation to see the full information on the functionality of Burin.

.. note::

    All Burin functions and methods are *underscore_separated*, however to ease
    changing from the standard library they all also have *camelCase* aliases.

    Throughout this documentation the *underscore_separated* names are used,
    but everytime you see a function or method call in Burin just remember that
    the *camelCase* name (like what is in ``logging``) will also work.

Burin can be imported and used similar to the ``logging`` standard libary
package.

.. code-block:: python

    import burin
    burin.basic_config()
    logger = burin.get_logger()
    logger.info("I am a log message.")

What is above would do the exact same thing with both Burin and ``logging``.

-----------------------
A Not So "Basic" Config
-----------------------

However compared to the standard ``logging`` package; using Burin can be
much simpler for certain things, or even allow some functionality that would
otherwise require custom wrapper utilities or overridding logging subclasses.

For example a common logging setup may be to output info level logs to a
rotating file with a specific format, and also output warning level logs to
``sys.stderr`` in a different format.

With Burin setting this up can be accomplished with 2 imports and 1 call to
``basic_config``.

.. code-block:: python

    import sys
    import burin
    burin.basic_config(filename="prog.log", filelevel="INFO", filerotate=True,
                       fileformat="{asctime} - {levelname} :{name}: {message}",
                       filerotatesize=1048576, filerotatecount=9, level="INFO",
                       stream=sys.stderr, streamlevel="WARNING",
                       streamformat="{levelname}: {message}", style="{")

Whereas with ``logging`` this takes 3 imports and 12 lines.

.. code-block:: python

    import sys
    import logging
    from logging.handlers import RotatingFileHandler
    fileForm = logging.Formatter("{asctime} - {levelname} :{name}: {message}",
                                 style="{")
    fileHand = RotatingFileHandler("prog.log", maxBytes=1048576, backupCount=9)
    fileHand.setFormatter(fileForm)
    fileHand.setLevel("INFO")
    streamForm = logging.Formatter("{levelname}: {message}", style="{")
    streamHand = logging.StreamHandler(sys.stderr)
    streamHand.setFormatter(streamForm)
    streamHand.setLevel("WARNING")
    rootLogger = logging.getLogger()
    rootLogger.addHandler(fileHand)
    rootLogger.addHandler(streamHand)
    rootLogger.setLevel("INFO")

--------------------------
Deferred Formatting Styles
--------------------------

Burin also supports deferred formatting with log messages using
``str.format`` and ``string.Template`` style strings, as well as the
'%' style formatting that the standard library does.  Which formatting is used
is set by the ``msgStyle`` property on a logger which can also be specified
when calling ``get_logger``.

.. code-block:: python

    formatLogger = burin.get_logger("formatLogger", "{")
    formatLogger.debug("This is a {} event in {}", "DEBUG", "Burin")
    templateLogger = burin.get_logger("templateLogger", msgStyle="$")
    templateLogger.debug("This is a ${lvl} event in ${prog}", lvl="DEBUG",
                         prog="Burin")

Setting this on the root logger will set the default style for new loggers as
well.

.. code-block:: python

    rootLogger = burin.get_logger(msgStyle="{")
    newLogger = burin.get_logger("new")
    newLogger.debug("This is a {lvl} event in {prog}", lvl="DEBUG",
                    prog="Burin")

Deferred formatting means that all of the extra formatting is only done if a
message will be logged, so this can be more efficient than doing the formatting
on the string beforehand.

For a bit more information about the deferred logging see
``BurinLogger.log``.

------------------------
Customisable Log Records
------------------------

Setting the ``msgStyle`` of a logger actually sets the log record factory that
is used.  While the default built-in factories are focused on formatting, you
can actually add any other custom factories that may be useful in your program.
These factories can then just be used where needed instead of for all log
messages as in the standard library.

This can be incredibly useful when you need a log to display values in a
specific way, but only want that extra processing to run if the log
message will actually be output.

To add your own factory simply create a subclass of ``BurinLogRecord`` and
then set it to a *msgStyle* with ``set_log_record_factory``.

.. code-block:: python

    class HexRecord(burin.BurinLogRecord):
        """
        Converts all int values to hex strings for log output.
        """

        def get_message(self):
            msg = str(self.msg)
            if self.args or self.kwargs:
                hexArgs = []
                hexKwargs = {}

                for eachArg in self.args:
                    if isinstance(eachArg, int):
                        eachArg = hex(eachArg)
                    hexArgs.append(eachArg)

                for eachKey, eachValue in self.kwargs.items():
                    if isinstance(eachValue, int):
                        eachValue = hex(eachValue)
                    hexKwargs[eachKey] = eachValue

                msg = msg.format(*hexArgs, **hexKwargs)
            return msg

    burin.set_log_record_factory(HexRecord, "hex")

In this example you would now be able to use ``hex`` as a *msgStyle* for any
loggers where you want int *args* and *kwargs* converted to a hexadecimal
string when the log message is output.
