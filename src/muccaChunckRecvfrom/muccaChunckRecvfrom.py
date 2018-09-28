"""MuccaChunckRecvfrom."""
import sys
import os


class muccaChunckRecvfrom:
    """Mucca Chunck recvfrom."""

    @staticmethod
    def run(socketServer, chunckSize, logging):
        """Run recvfrom mucca."""
        logging.log_info(
            'Wait [preflight]...',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
            )

        data, address = socketServer.recvfrom(chunckSize)

        logging.log_info(
            'Received total size msg {}:{} {} Byte'.format(
                address[0],
                address[1],
                int(data)
            ),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
            )

        numberOfChunk = int(data)/chunckSize
        plusChunk = int(data) % chunckSize
        numberOfChunkRecived = 0

        if plusChunk > 0:
            numberOfChunk = int(numberOfChunk + 1.0)

        cp = numberOfChunk
        completeMsg = ""
        while numberOfChunk is not 0:
            numberOfChunk = numberOfChunk-1
            numberOfChunkRecived = numberOfChunkRecived+1

            if numberOfChunk == 0:
                chunckSize = plusChunk

            logging.log_info(
                'WAIT FROM {}:{} [{} of {}]...'.format(
                    address[0],
                    address[1],
                    numberOfChunkRecived,
                    cp
                ),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            data, address = socketServer.recvfrom(chunckSize)

            logging.log_info(
                '"FROM {}:{} Chunk [{} of {}]: {} Byte'.format(
                    address[0],
                    address[1],
                    numberOfChunkRecived,
                    cp,
                    len(data)
                ),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            completeMsg = "{}{}".format(completeMsg, data.decode('utf-8'))
        return {
                "data": completeMsg.encode(),
                "address": address
                }
