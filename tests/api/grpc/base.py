# -*- coding:utf-8 -*-
from collections import namedtuple

import grpc_testing

from api.grpc import services_pb2
from api.grpc.pieledger import PieLedger
from ...core.base import BaseTestCase

RPCResult = namedtuple('RPCResult', ['metadata', 'code', 'detail'])
RPCStreamResult = namedtuple(
    'RPCStreamResult',
    ['intinal_metadata', 'trailing_metadata', 'code', 'detail'])


class GrpcTestCase(BaseTestCase):

    descriptors_to_servicers = {}

    def setUp(self):
        super(GrpcTestCase, self).setUp()
        self._real_time = grpc_testing.strict_real_time()
        self._real_time_server = grpc_testing.server_from_dictionary(
            self.descriptors_to_servicers, self._real_time)

    @staticmethod
    def _stream_responses(rpc):
        try:
            while True:
                yield rpc.take_response()
        except ValueError as e:
            if e.args[0] != 'No more responses!':
                raise

    def _unary_unary(self, service, method, request, meta=(), deadline=None):
        rpc = self._real_time_server.invoke_unary_unary(
            service.methods_by_name[method], meta, request, deadline)
        rv = list(rpc.termination())
        return rv[0], RPCResult(*rv[1:])

    def _unary_stream(self, service, method, request, meta=(), deadline=None):
        rpc = self._real_time_server.invoke_unary_stream(
            service.methods_by_name[method], meta, request, deadline)
        initial_metadata = rpc.initial_metadata()
        return self._stream_responses(rpc), RPCStreamResult(
            *list((initial_metadata, ) + rpc.termination()))


_LEDGER_SERVICE = services_pb2.DESCRIPTOR.services_by_name['PieLedger']


class PieLedgerGrpcTest(GrpcTestCase):

    descriptors_to_servicers = {
        _LEDGER_SERVICE: PieLedger()
    }

    def unary_unary(self, *args, **kw):
        return self._unary_unary(_LEDGER_SERVICE, *args, **kw)

    def unary_stream(self, *args, **kw):
        return self._unary_stream(_LEDGER_SERVICE, *args, **kw)
