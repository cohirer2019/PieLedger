# -*- coding:utf-8 -*-
import services_pb2_grpc
import ledger_pb2


class PieLedger(services_pb2_grpc.PieLedgerServicer):
    def FindOrCreateAccount(self, request, context):
        return ledger_pb2.Account(name='%s' % request.name)
