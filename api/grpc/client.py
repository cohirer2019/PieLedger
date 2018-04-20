import grpc

import services_pb2_grpc
import services_pb2
import ledger_pb2


# def run():
#     channel = grpc.insecure_channel('localhost:50051')
#     stub = services_pb2_grpc.PieLedgerStub(channel)
#     try:
#         response = stub.FindTransactions(
#             services_pb2.TransactionQueryRequest(
#                 guids=['9a7hys', '1qaz', '2wsx'],
#                 account=ledger_pb2.Account(
#                     guid='8b1d8d5e9d6d4e40ae956f3b1943eb92'),
#                 page_number=5,
#                 result_per_page=20)
#         )
def run():
    channel = grpc.insecure_channel('[::]:50052')
    stub = services_pb2_grpc.PieLedgerStub(channel)
    try:
        response = stub.FindOrCreateAccount(ledger_pb2.Account(
            guid=None,
            name='auchan',
            type=ledger_pb2.AccountType.Value('INCOME'),
            parent=ledger_pb2.Account(guid='da5cba81f05a45ffb638f1b14ec22f38'),
            placeholder=False,
            balance=0
        ))
    except grpc.RpcError as e:
        print e.details()
        status_code = e.code()
        print status_code.name
        print status_code.value
    else:
        print response.name
        print response.type


if __name__ == '__main__':
    run()
