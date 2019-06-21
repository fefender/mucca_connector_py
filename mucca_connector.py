# Copyright 2018 Federica Cricchio
# fefender@gmail.com
#
# This file is part of mucca_connector_py.
#
# mucca_connector_py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mucca_connector_py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mucca_connector_py.  If not, see <http://www.gnu.org/licenses/>.
"""Mucca Connector."""
import socket
import sys
import os
from vendor.mucca_logging.mucca_logging import logging
from vendor.mucca_connector_py.src.muccaChunckRecvfrom.muccaChunckRecvfrom import muccaChunckRecvfrom
from vendor.mucca_connector_py.src.muccaChunckSendTo.muccaChunckSendTo import muccaChunckSendTo


class mucca_connector:
    """Mucca_connector class."""

    def __init__(self):
        """Init."""
        pass

    def serverHandler(self, port, buffersize, ptr=None):
        """ServerHandler."""
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
            socket.IPPROTO_UDP
        ) as ss:
            ss.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            host = ''
            server_address = (host, port)
            logging.log_info(
                'PORT : {}'.format(port),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            logging.log_info(
                'BUFFER_SIZE : {}'.format(buffersize),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            logging.log_info(
                'PROTOCOL : UDP',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            try:
                ss.bind(server_address)
            except OSError as emsg:
                logging.log_error(
                    'Socket Bind Error{}'.format(emsg),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                ss.close()
                sys.exit(1)
            while True:
                pid = os.fork()
                if pid == 0:
                    print("******************* child pid -> ", os.getpid())
                    result = muccaChunckRecvfrom.run(ss, buffersize, logging)
                    response = ptr(result["data"])
                    muccaChunckSendTo.run(
                        ss,
                        buffersize,
                        str(response),
                        result["address"],
                        logging
                    )
                    ss.close()
                    os._exit(0)
                else:
                    print("****************** parent pid -> ", os.getpid())
                    os.waitpid(0, 0)
        return 0

    def clientUdp(self, port, ip, message, response_flag, buffersize):
        """ClientUdp."""
        response_rec = None
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
            socket.IPPROTO_UDP
        ) as cs:
            cs.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            server_address = (ip, port)
            c_message = bytes(message.encode())
            try:
                muccaChunckSendTo.run(
                    cs,
                    buffersize,
                    str(c_message, "utf-8"),
                    server_address,
                    logging
                )
            except InterruptedError as emsg:
                logging.log_error(
                    'Interrupted signal error, sendto fail',
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
            if response_flag != 0:
                try:
                    cs.settimeout(10.0)
                    result = muccaChunckRecvfrom.run(cs, buffersize, logging)
                    response_rec = result["data"]
                except socket.timeout as emsg:
                    response_rec = {
                        "service": {
                            "status": "500",
                            "serviceName": "connector",
                            "action": "NULL"
                            },
                        "head": {
                            "Content-Type": "application/json; charset=utf-8",
                            "Mucca-Service": "NULL"
                            },
                        "body": {
                            "msg": "generic error"
                        }
                    }
            else:
                response_rec = {
                    "service": {
                        "status": "202",
                        "serviceName": "connector",
                        "action": "NULL"
                        },
                    "head": {
                        "Content-Type": "application/json; charset=utf-8",
                        "Mucca-Service": "NULL"
                        },
                    "body": {
                        "msg": "Response 202 Accepted"
                    }
                }
        return response_rec
