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

    def serverHandler(self, ports, buffersize, ptr=None):
        """ServerHandler."""
        for port in ports:
            with socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM,
                socket.IPPROTO_UDP
            ) as ss:
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
                #while True:
                pid = os.fork()
                if pid == 0:
                    while True:
                        pid_rec = os.fork()
                        if pid_rec == 0:
                            result = muccaChunckRecvfrom.run(ss, buffersize, logging)
                            # if result["status"] == 1:
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
                            # os.waitpid(0, 0)
                            print("paret-req")
                            os.waitpid(0, 0)
                else:
                    print("paret")
                    # os.waitpid(0, 0)
        os.waitpid(0, 0)
        return 0

    def clientUdp(self, ports, ip, message, response_flag, buffersize):
        """ClientUdp."""
        print('******** --- Test ports scale {}'.format(ports))
        if os.getenv("MUCCACONNECTORLASTPORT") == None:
            lastPortIndex = 0
            os.environ["MUCCACONNECTORLASTPORT"]=str(lastPortIndex)
            print('******** --- Test env pos after put {}'.format(os.getenv("MUCCACONNECTORLASTPORT")))
            port = ports[lastPortIndex]
        else:
            lastPortIndex = int(os.getenv("MUCCACONNECTORLASTPORT"))
            try:
                lastPortIndex = lastPortIndex + 1
                os.environ["MUCCACONNECTORLASTPORT"]=str(lastPortIndex)
                port = ports[lastPortIndex]
            except Exception:
                lastPortIndex = 0
                os.environ["MUCCACONNECTORLASTPORT"]=str(lastPortIndex)
                port = ports[lastPortIndex]
        print('******** Test port scale {}'.format(port))
        response_rec = None
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
            socket.IPPROTO_UDP
        ) as cs:
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
                    print("---------------", result['address'])
                    print("---------------", result['status'])
                    if int(result['status']) == -1:
                        cs.close()
                        test=0
                        while test <= 3:
                            with socket.socket(
                                socket.AF_INET,
                                socket.SOCK_DGRAM,
                                socket.IPPROTO_UDP
                            ) as cs:
                                server_address = (ip, port)
                                c_message = bytes(message.encode())
                                muccaChunckSendTo.run(
                                    cs,
                                    buffersize,
                                    str(c_message, "utf-8"),
                                    server_address,
                                    logging
                                )
                                # cs.settimeout(10.0)
                                result = muccaChunckRecvfrom.run(cs, buffersize, logging)
                                cs.close()
                                if result["status"] == 1:
                                    return result["data"]
                                else:
                                    test=test+1
                    response_rec = result["data"]
                except socket.timeout as emsg:
                    cs.close()
                    test=0
                    while test <= 3:
                        with socket.socket(
                            socket.AF_INET,
                            socket.SOCK_DGRAM,
                            socket.IPPROTO_UDP
                        ) as cs:
                            server_address = (ip, port)
                            c_message = bytes(message.encode())
                            muccaChunckSendTo.run(
                                cs,
                                buffersize,
                                str(c_message, "utf-8"),
                                server_address,
                                logging
                            )
                            # cs.settimeout(10.0)
                            result = muccaChunckRecvfrom.run(cs, buffersize, logging)
                            cs.close()
                            if result["status"] == 1:
                                return result["data"]
                            else:
                                test=test+1
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
        cs.close()
        return response_rec
