# -*- coding:utf-8 -*-
import ledger_pb2
import services_pb2_grpc


class PieLedger(services_pb2_grpc.PieLedgerServicer):

    def FindOrCreateAccount(self, request, context):
        return ledger_pb2.Account(name='%s' % request.name)

    def UpdateBalance(self, request, context):
        return ledger_pb2.Account(balance=100)
