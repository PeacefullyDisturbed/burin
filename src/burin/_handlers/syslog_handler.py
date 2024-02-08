"""
Burin Syslog Handler

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import SysLogHandler, SYSLOG_UDP_PORT
import socket

# Burin imports
from .handler import BurinHandler


class BurinSyslogHandler(BurinHandler, SysLogHandler):
    """
    A handler that supports sending log records to a local or remote syslog.

    .. note::

        This is a subclass of :class:`logging.handlers.SysLogHandler` and
        functions identically to it in normal use cases.

        Unlike the standard library handler the 'l' in 'Syslog' of the class
        name is not capitalized so this class better matches the actual
        'Syslog' name.
    """

    def __init__(self, address=("localhost", SYSLOG_UDP_PORT),
                 facility=SysLogHandler.LOG_USER, socktype=None):
        """
        This initializes the handler and sets it for sending to syslog.

        By default the handler will try to use a local syslog through UDP port
        514; to change this *address* must be set as a tuple in the form
        *(host, port)*.

        By default a UDP connection is created; if TCP is needed ensure
        *socktype* is set to :const:`socket.SOCK_STREAM`.

        :param address: The address to connect to syslog at.  This should be a
                        tuple in the form of *(host, port)*.  (Default =
                        ('localhost', 514))
        :type address: tuple(str, int)
        :param facility: The syslog facility to use.  These are available as
                         class attributes on the handler to simplify usage.
                         (Default = 1 (LOG_USER))
        :type facility: int
        :param socktype: The socket type to use for the connection to syslog.
                         By default a :const:`socket.SOCK_DGRAM` socket is
                         used if this is **None**; for TCP connections specify
                         :const:`socket.SOCK_STREAM`.
        :type socktype: int
        """

        BurinHandler.__init__(self)

        self.address = address
        self.facility = facility
        self.socktype = socktype
        self.socket = None

    # Alias methods from the standard library handler
    encode_priority = SysLogHandler.encodePriority
    map_priority = SysLogHandler.mapPriority

    def close(self):
        """
        Closes the handler and the syslog socket.
        """

        with self.lock:
            if self.socket:
                socket = self.socket
                self.socket = None
                socket.close()
            BurinHandler.close(self)

    def create_socket(self):
        """
        Try to create a socket and, if not datagram, connect to the other end.

        This will be called automatically during initialization of the handler.
        If it fails to connect at this point it is not considered an error.
        The method will be called again when emitting an event if there is
        still no socket connected.

        .. note::

            In Python 3.11 :meth:`logging.handlers.SysLogHandler.createSocket`
            was added to the standard library; it is supported here for all
            versions of Python compatible with Burin (including versions below
            3.11).
        """
        address = self.address
        socktype = self.socktype

        if isinstance(address, str):
            self.unixsocket = True

            # The syslog server may be unavailable during handler
            # initialization which can be ignored
            try:
                self._connect_unixsocket(address)
            except OSError:
                pass
        else:
            self.unixsocket = False

            if socktype is None:
                socktype = socket.SOCK_DGRAM

            host, port = address
            addrInfo = socket.getaddrinfo(host, port, 0, socktype)

            if not addrInfo:
                raise OSError("getaddrinfo returned an empty list")

            for addr in addrInfo:
                addrFam, socktype, addrProto, addrCanon, addrSock = addr
                err = sock = None

                try:
                    sock = socket.socket(addrFam, socktype, addrProto)

                    if socktype == socket.SOCK_STREAM:
                        sock.connect(addrSock)
                    break
                except OSError as exc:
                    err = exc

                    if sock is not None:
                        sock.close()

            if err is not None:
                raise err

            self.socket = sock
            self.socktype = socktype

    def emit(self, record):
        """
        Emits a log record to the Syslog socket.

        The log record will be formatted and sent to the Syslog server.  If
        exception information is present in the log record it will *NOT* be
        sent along to the server.

        .. note::

            If a socket connection was not established earlier this will
            attempt to complete it again before emitting the record.  This
            functionality was added in the Python 3.11 standard library and is
            supported here for all versions of Python compatible with Burin
            (including versions below 3.11)

        :param record: The log record to emit.
        :type record: BurinLogRecord
        """

        try:
            msg = self.format(record)
            if self.ident:
                msg = self.ident + msg
            if self.append_nul:
                msg += "\000"

            # Convert the level to lowercase for Syslog
            priority = f"{self.encodePriority(self.facility, self.map_priority(record.levelname))}"

            # Convert the message to bytes are required by RFX 5424
            priority = priority.encode("utf-8")
            msg = msg.encode("utf-8")
            msg = priority + msg

            if not self.socket:
                self.create_socket()

            if self.unixsocket:
                try:
                    self.socket.send(msg)
                except OSError:
                    self.socket.close()
                    self._connect_unixsocket(self.address)
                    self.socket.send(msg)
            elif self.socktype == socket.SOCK_DGRAM:
                self.socket.sendto(msg, self.address)
            else:
                self.socket.sendall(msg)
        except Exception:
            self.handle_error(record)

    # Aliases for better compatibility to replace standard library logging
    createSocket = create_socket
