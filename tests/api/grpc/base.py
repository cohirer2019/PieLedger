# -*- coding:utf-8 -*-
from collections import namedtuple

import grpc_testing

from api.grpc import services_pb2
from api.grpc.pieledger import PieLedger
from ...core.base import BaseTestCase

RPCResult = namedtuple('RPCResult', ['metadata', 'code', 'detail'])


class GrpcTestCase(BaseTestCase):

    descriptors_to_servicers = {}

    def setUp(self):
        super(GrpcTestCase, self).setUp()
        self._real_time = grpc_testing.strict_real_time()
        self._real_time_server = grpc_testing.server_from_dictionary(
            self.descriptors_to_servicers, self._real_time)

    def _unary_unary(self, service, method, request, meta=(), deadline=None):
        rpc = self._real_time_server.invoke_unary_unary(
            service.methods_by_name[method], meta, request, deadline)
        rv = list(rpc.termination())
        return rv[0], RPCResult(*rv[1:])


_LEDGER_SERVICE = services_pb2.DESCRIPTOR.services_by_name['PieLedger']


class PieLedgerGrpcTest(GrpcTestCase):

    descriptors_to_servicers = {
        _LEDGER_SERVICE: PieLedger()
    }

    def unary_unary(self, *args, **kw):
        return self._unary_unary(_LEDGER_SERVICE, *args, **kw)
