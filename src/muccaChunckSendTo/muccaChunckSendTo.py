"""MuccaChunckSendTo."""
import sys
import os
import hashlib


class muccaChunckSendTo:
    """MuccaChunckSendTo."""

    @staticmethod
    def run(socketClient, chunckSize, message, address, logging):
        """Run."""
        msgSize = len(message)
        logging.log_info(
            'Sending [prefilight]...',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
            )
        controlMd5 = hashlib.md5(message.encode())
        msgPrefight={"md5":(controlMd5.hexdigest()), "size":str(msgSize)}
        print("\n\n-------------- *********** {}\n\n".format(str(msgPrefight).encode()))
        # sent = socketClient.sendto(bytes(str(msgSize).encode()), address)
        # print("--- sent -> {}".format(bytes(str(msgSize).encode())))
        sent = socketClient.sendto(str(msgPrefight).encode(), address)
        numberOfChunk = int(msgSize)/chunckSize
        plusChunk = int(msgSize) % chunckSize

        if plusChunk > 0:
            numberOfChunk = int(numberOfChunk + 1.0)
        numberOfChunk = round(numberOfChunk)
        i = 0
        for i in range(0, int(numberOfChunk)):
            chunkedMsg = ""
            if i == numberOfChunk-1 and plusChunk > 0:
                chunkedMsg = message[len(message)-plusChunk:]
            else:
                chunkedMsg = message[
                    (chunckSize)*i: ((chunckSize)*i)+chunckSize
                ]
            sent = socketClient.sendto(
                bytes(
                    str(chunkedMsg).encode()
                ),
                address
                )

            logging.log_info(
                "Send to {}:{} Chunk [{} of {}]: {} Byte".format(
                    address[0],
                    address[1],
                    i+1,
                    int(numberOfChunk),
                    sent
                ),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
