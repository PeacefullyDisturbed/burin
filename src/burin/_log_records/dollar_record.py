"""
Burin Brace Log Record

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
from string import Template

# Burin imports
from .log_record import BurinLogRecord


class BurinDollarLogRecord(BurinLogRecord):
    """
    A log record that will be formatted in :class:`string.Template` ($ style).

    This allows for deferred formatting using keyword arguments that are passed
    in during log record creation.

    This is derived from :class:`BurinLogRecord`.
    """

    def get_message(self):
        """
        This formats the log message.

        All additional *kwargs* that were part of the log record creation are
        used for the formatting of the log message.

        :meth:`string.Template.safe_substitute` so no exceptions are raised
        if keys and format placeholders don't all match.

        :returns: The formatted log message.
        :rtype: str
        """

        msg = str(self.msg)
        if self.kwargs:
            msg = Template(msg).safe_substitute(self.kwargs)
        return msg

    # Aliases for better compatibility to replace standard library logging
    getMessage = get_message
