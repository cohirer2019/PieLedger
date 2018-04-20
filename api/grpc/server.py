# -*- coding:utf-8 -*-
from concurrent import futures
import time

import grpc

from . import services_pb2_grpc
from . import pieledger

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    services_pb2_grpc.add_PieLedgerServicer_to_server(
        pieledger.PieLedger(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
