# -*- coding:utf-8 -*-
from concurrent import futures
import time

import grpc

import services_pb2_grpc
import pieledger

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    services_pb2_grpc.add_PieLedgerServicer_to_server(
        pieledger.PieLedger(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
