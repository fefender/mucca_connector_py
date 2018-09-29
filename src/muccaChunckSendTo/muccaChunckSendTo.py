"""MuccaChunckSendTo."""
import sys
import os


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

        sent = socketClient.sendto(bytes(str(msgSize).encode()), address)

        numberOfChunk = int(msgSize)/chunckSize
        plusChunk = int(msgSize) % chunckSize

        if plusChunk > 0:
            numberOfChunk = int(numberOfChunk + 1.0)

        i = 0
        for i in range(0, int(numberOfChunk)):
            chunkedMsg = ""
            if i is numberOfChunk-1 and plusChunk > 0:
                chunkedMsg = message[len(message)-plusChunk:]
            else:
                chunkedMsg = message[
                    (chunckSize)*i: -len(message[int(chunckSize):])
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
