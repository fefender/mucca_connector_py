"""MuccaChunckRecvfrom."""
import sys
import os
import json
from collections import OrderedDict


class muccaChunckRecvfrom:
    """Mucca Chunck recvfrom."""

    @staticmethod
    def run(socketServer, chunckSize, logging):
        """Run recvfrom mucca."""
        try:
            logging.log_info(
                'Wait [preflight]...',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )

            dataString, address = socketServer.recvfrom(chunckSize)

            dataPreFlight = json.loads(
                dataString.decode(),
                object_pairs_hook=OrderedDict
            )

            logging.log_info(
                'Received total size msg {}:{} {} Byte'.format(
                    address[0],
                    address[1],
                    int(dataPreFlight["size"])
                ),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            totalsize = int(dataPreFlight["size"])
            numberOfChunk = int(dataPreFlight["size"])/chunckSize
            plusChunk = int(dataPreFlight["size"]) % chunckSize
            numberOfChunkRecived = 0

            if plusChunk > 0:
                numberOfChunk = int(numberOfChunk + 1.0)

            cp = round(numberOfChunk)
            numberOfChunkInt = round(numberOfChunk)

            completeMsg = ""
            while numberOfChunkInt != 0:
                numberOfChunkInt = numberOfChunkInt-1
                numberOfChunkRecived = numberOfChunkRecived+1

                if numberOfChunkInt == 0:
                    chunckSize = totalsize-((cp-1)*chunckSize)

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
                    'FROM {}:{} Chunk [{} of {}]: {} Byte'.format(
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
            controlMd5 = hashlib.md5(completeMsg.encode())
            if dataPreFlight["md5"] != controlMd5.hexdigest():
                return {
                        "data": None,
                        "address": None,
                        "status": -1
                        }
        except Exception:
            return {
                    "data": None,
                    "address": None,
                    "status": -1
                    }

        return {
                "data": completeMsg.encode(),
                "address": address,
                "status": 1
                }
