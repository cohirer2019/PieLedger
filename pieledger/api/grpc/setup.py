from setuptools import setup

setup(
    name='PieLedger-Grpc',
    version='1.0.1',
    namespace_packages=['pieledger', 'pieledger.api', 'pieledger.api.grpc'],
    py_modules=[
        'pieledger.api.grpc.ledger_pb2',
        'pieledger.api.grpc.services_pb2',
        'pieledger.api.grpc.services_pb2_grpc'
    ],
    package_dir={'pieledger.api.grpc': ''},
    install_requires=[
        'grpcio==1.12.0',
        'protobuf>=3.5.2'
    ],
    url='http://dev.smart4e.com/cohirer/pieledger',
    license='Apache License 2.0',
    author='CoHirer Inc.',
    author_email='info@cohirer.com',
    description='Grpc sub files for PieLedger'
)
