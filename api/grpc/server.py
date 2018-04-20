# -*- coding:utf-8 -*-
from multiprocessing import cpu_count
from concurrent import futures
import time

import grpc

from core.config import ledger_config
from . import services_pb2_grpc
from . import pieledger

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def serve(bind_addr='[::]:50051'):
    # TODO: remove the cpu_count call when upgraded to python 3.6
    server = grpc.server(futures.ThreadPoolExecutor(cpu_count()))
    services_pb2_grpc.add_PieLedgerServicer_to_server(
        pieledger.PieLedger(), server)
    config = ledger_config.get('grpc', {})
    bind_addr = config.get('bind_addr') or bind_addr
    server.add_insecure_port(bind_addr)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
