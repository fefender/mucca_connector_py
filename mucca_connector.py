"""Mucca Connector."""
import socket
import sys
import os
from vendor.mucca_logging.mucca_logging import logging


class mucca_connector:
    """Mucca_connector class."""

    def __init__(self):
        """Init."""
        pass

    def serverHandler(self, port, blen, ptr=None):
        """ServerHandler."""
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
            socket.IPPROTO_UDP
        ) as ss:
            host = ''
            server_address = (host, port)
            logging.log_info(
                'Starting on {} : {}'.format(*server_address),
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
                logging.log_info(
                    'Wait...',
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
                data, address = ss.recvfrom(4096)
                logging.log_info(
                    'Received {} bytes from {}'.format(
                        len(data),
                        address
                        ),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                logging.log_info(
                    data,
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                try:
                    response = ptr(data)
                    sent = ss.sendto(bytes(response.encode()), address)
                    logging.log_info(
                        'Sent {} bytes back to {}'.format(sent, address),
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                    )
                except OSError as emsg:
                    logging.log_error(
                        'Data sending error {}'.format(emsg),
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                    )
                    ss.close()
                    sys.exit(1)
        return 0

    def clientUdp(self, port, ip, message, response_flag, buffersize):
        """ClientUdp."""
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
            socket.IPPROTO_UDP
        ) as cs:
            server_address = (ip, port)
            c_message = bytes(message.encode())
            try:
                logging.log_info(
                    'Sending {!r}'.format(c_message),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                sent = cs.sendto(c_message, server_address)
                logging.log_info(
                    'Sent {} bytes back to {} from {}'.format(
                        sent,
                        server_address,
                        ip
                    ),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
            except InterruptedError as emsg:
                logging.log_error(
                    'Interrupted signal error, sendto fail',
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
            if response_flag != 0:
                try:
                    logging.log_info(
                        'waiting for response...',
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                    )
                    cs.settimeout(5.0)
                    response_rec, server = cs.recvfrom(4096)
                    logging.log_info(
                        'Received response from server: {!r}'.format(
                            response_rec
                        ),
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                    )
                except socket.timeout as emsg:
                    logging.log_error(
                        'clientUdp recvfrom timed out: {})'.format(
                            emsg
                        ),
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                    )
                    response_rec = '{"service": { "status": "500", "serviceName": "connector", "action": "NULL" }, "head": { "Content-Type": "application/json; charset=utf-8", "Mucca-Service": "NULL" }, "body": { "msg": "generic error" }}'
            logging.log_info(
                'Closing socket',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            cs.close()
        return response_rec
