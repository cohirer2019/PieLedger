# -*- coding:utf-8 -*-
from multiprocessing import cpu_count
from concurrent import futures
import time

import grpc

from core.config import ledger_config
from . import services_pb2_grpc
from . import servicer

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def _setup_logging():
    sentry_dsn = ledger_config.get('sentry_dsn')
    if sentry_dsn:
        import logging
        from raven.handlers.logging import SentryHandler
        from raven.conf import setup_logging
        handler = SentryHandler(sentry_dsn, level=logging.WARNING)
        setup_logging(handler)


def serve(bind_addr='[::]:50051'):
    _setup_logging()

    # TODO: remove the cpu_count call when upgraded to python 3.6
    server = grpc.server(futures.ThreadPoolExecutor(cpu_count()))
    services_pb2_grpc.add_PieLedgerServicer_to_server(
        servicer.PieLedger(), server)
    config = ledger_config.get('grpc', {})
    bind_addr = config.get('bind_addr') or bind_addr
    server.add_insecure_port(bind_addr)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
