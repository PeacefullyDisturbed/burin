"""
Burin Stream Handler

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
from logging import StreamHandler
import sys

# Burin imports
from .._log_levels import get_level_name
from .handler import BurinHandler


class BurinStreamHandler(BurinHandler, StreamHandler):
    """
    A handler that writes log records to a stream.

    .. note::

        This is a subclass of :class:`logging.StreamHandler` and
        functions identically to it in normal use cases.

    .. note::

        This handler will not close the stream it is writing to as
        :obj:`sys.stdout` and :obj:`sys.stderr` are commonly used.
    """

    terminator = "\n"

    def __init__(self, stream=None):
        """
        This initializes the handler and sets the *stream* to use.

        If *stream* is **None** then :obj:`sys.stderr` is used by default.

        :param stream: The stream to log to.  If this is **None** then
                       :obj:`sys.stderr` is used.
        :type stream: io.TextIOBase
        """

        BurinHandler.__init__(self)
        if stream is None:
            stream = sys.stderr
        self.stream = stream

    # Alias method from the standard library handler
    set_stream = StreamHandler.setStream

    def __repr__(self):
        level = get_level_name(self.level)
        name = getattr(self.stream, "name", "")

        # Name could be an int
        name = str(name)
        if name:
            name += " "

        return f"<{self.__class__.__name__} {name}({level})>"
