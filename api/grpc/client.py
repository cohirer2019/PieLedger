import grpc

import services_pb2_grpc
import ledger_pb2


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = services_pb2_grpc.PieLedgerStub(channel)
    response = stub.FindOrCreateAccount(ledger_pb2.Account(
        guid=None,
        name='auchan',
        type=0,
        parent=None,
        placeholder=False,
        balance=0
    ))
    print response.name
    print response.type


if __name__ == '__main__':
    run()
