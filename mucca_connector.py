import socket
import sys

class mucca_connector:
    def __init__(self):
        pass
    def serverHandler(self, port, blen, ptr = None):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as ss:
            host = ''
            server_address = (host, port)
            print('Starting on {} : {}'.format(*server_address))
            try:
                ss.bind(server_address)
            except OSError as emsg:
                print('Socket Bind Error{}'.format(emsg))
                ss.close()
                sys.exit(1)
            while True:
                print('wait...')
                # data, address = ss.recvfrom(socket.CMSG_SPACE(blen)) per il client in realtà mi serve, qui no
                data, address = ss.recvfrom(4096)
                print('Received {} bytes from {}'.format(
                    len(data), address))
                print(data)
                try:
                    response = ptr(data)
                    sent = ss.sendto(bytes(response.encode()), address)
                    print('Sent {} bytes back to {}'.format(
                                sent, address))
                except OSError as emsg:
                    print('Data sending error {}'.format(emsg))
                    ss.close()
                    sys.exit(1)
        return 0

    def clientUdp(self, port, ip, message, response_flag, buffersize):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as cs:
            server_address = (ip, port)
            c_message = bytes(message.encode())
            try:
                print('Sending {!r}'.format(c_message))
                sent = cs.sendto(c_message, server_address)
                print('Sent {} bytes back to {} from {}'.format(
                        sent, server_address, ip))
            except InterruptedError as emsg:
                print('Interrupted signal error, sendto fail')
            if response_flag !=0:
                try:
                    print('waiting for response...')
                    cs.settimeout(5.0)
                    response_rec, server = cs.recvfrom(4096)
                    print('Received response from server: {!r}'.format(response_rec))
                except socket.timeout as emsg:
                    print('clientUdp recvfrom timed out (socket.timeout except: {})'.format(emsg))
                    response_rec = '{"service": { "status": "500", "serviceName": "connector", "action": "NULL" }, "head": { "Content-Type": "application/json; charset=utf-8", "Mucca-Service": "NULL" }, "body": { "msg": "generic error" }}'
            print('Closing socket')
            cs.close()
        return response_rec
