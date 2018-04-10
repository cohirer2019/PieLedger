# -*- coding:utf-8 -*-
import unittest

import grpc_testing

from api.grpc import services_pb2
from api.grpc.pieledger import PieLedger


class GrpcTestCase(unittest.TestCase):

    _ledger_service = services_pb2.DESCRIPTOR.services_by_name['PieLedger']

    def setUp(self):
        self._real_time = grpc_testing.strict_real_time()
        servicer = PieLedger()
        descriptors_to_servicers = {
            self._ledger_service: servicer
        }
        self._real_time_server = grpc_testing.server_from_dictionary(
            descriptors_to_servicers, self._real_time)
