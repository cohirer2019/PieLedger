# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: services.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import ledger_pb2 as ledger__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='services.proto',
  package='pieledger',
  syntax='proto3',
  serialized_pb=_b('\n\x0eservices.proto\x12\tpieledger\x1a\x0cledger.proto\"{\n\x17TransactionQueryRequest\x12\x13\n\x0bpage_number\x18\x01 \x01(\x05\x12\x17\n\x0fresult_per_page\x18\x02 \x01(\x05\x12\r\n\x05guids\x18\x03 \x03(\t\x12#\n\x07\x61\x63\x63ount\x18\x04 \x01(\x0b\x32\x12.pieledger.Account\"\x8e\x01\n\x11SplitQueryRequest\x12\x13\n\x0bpage_number\x18\x01 \x01(\x05\x12\x17\n\x0fresult_per_page\x18\x02 \x01(\x05\x12#\n\x07\x61\x63\x63ount\x18\x03 \x01(\x0b\x32\x12.pieledger.Account\x12&\n\x06\x61\x63tion\x18\x04 \x01(\x0e\x32\x16.pieledger.SplitAction2\xdd\x02\n\tPieLedger\x12=\n\x13\x46indOrCreateAccount\x12\x12.pieledger.Account\x1a\x12.pieledger.Account\x12\x36\n\x0c\x41lterAccount\x12\x12.pieledger.Account\x1a\x12.pieledger.Account\x12\x43\n\x11\x43reateTransaction\x12\x16.pieledger.Transaction\x1a\x16.pieledger.Transaction\x12P\n\x10\x46indTransactions\x12\".pieledger.TransactionQueryRequest\x1a\x16.pieledger.Transaction0\x01\x12\x42\n\x10\x41lterTransaction\x12\x16.pieledger.Transaction\x1a\x16.pieledger.Transactionb\x06proto3')
  ,
  dependencies=[ledger__pb2.DESCRIPTOR,])




_TRANSACTIONQUERYREQUEST = _descriptor.Descriptor(
  name='TransactionQueryRequest',
  full_name='pieledger.TransactionQueryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='page_number', full_name='pieledger.TransactionQueryRequest.page_number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result_per_page', full_name='pieledger.TransactionQueryRequest.result_per_page', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='guids', full_name='pieledger.TransactionQueryRequest.guids', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account', full_name='pieledger.TransactionQueryRequest.account', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=43,
  serialized_end=166,
)


_SPLITQUERYREQUEST = _descriptor.Descriptor(
  name='SplitQueryRequest',
  full_name='pieledger.SplitQueryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='page_number', full_name='pieledger.SplitQueryRequest.page_number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result_per_page', full_name='pieledger.SplitQueryRequest.result_per_page', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account', full_name='pieledger.SplitQueryRequest.account', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='action', full_name='pieledger.SplitQueryRequest.action', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=169,
  serialized_end=311,
)

_TRANSACTIONQUERYREQUEST.fields_by_name['account'].message_type = ledger__pb2._ACCOUNT
_SPLITQUERYREQUEST.fields_by_name['account'].message_type = ledger__pb2._ACCOUNT
_SPLITQUERYREQUEST.fields_by_name['action'].enum_type = ledger__pb2._SPLITACTION
DESCRIPTOR.message_types_by_name['TransactionQueryRequest'] = _TRANSACTIONQUERYREQUEST
DESCRIPTOR.message_types_by_name['SplitQueryRequest'] = _SPLITQUERYREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TransactionQueryRequest = _reflection.GeneratedProtocolMessageType('TransactionQueryRequest', (_message.Message,), dict(
  DESCRIPTOR = _TRANSACTIONQUERYREQUEST,
  __module__ = 'services_pb2'
  # @@protoc_insertion_point(class_scope:pieledger.TransactionQueryRequest)
  ))
_sym_db.RegisterMessage(TransactionQueryRequest)

SplitQueryRequest = _reflection.GeneratedProtocolMessageType('SplitQueryRequest', (_message.Message,), dict(
  DESCRIPTOR = _SPLITQUERYREQUEST,
  __module__ = 'services_pb2'
  # @@protoc_insertion_point(class_scope:pieledger.SplitQueryRequest)
  ))
_sym_db.RegisterMessage(SplitQueryRequest)



_PIELEDGER = _descriptor.ServiceDescriptor(
  name='PieLedger',
  full_name='pieledger.PieLedger',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=314,
  serialized_end=663,
  methods=[
  _descriptor.MethodDescriptor(
    name='FindOrCreateAccount',
    full_name='pieledger.PieLedger.FindOrCreateAccount',
    index=0,
    containing_service=None,
    input_type=ledger__pb2._ACCOUNT,
    output_type=ledger__pb2._ACCOUNT,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='AlterAccount',
    full_name='pieledger.PieLedger.AlterAccount',
    index=1,
    containing_service=None,
    input_type=ledger__pb2._ACCOUNT,
    output_type=ledger__pb2._ACCOUNT,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='CreateTransaction',
    full_name='pieledger.PieLedger.CreateTransaction',
    index=2,
    containing_service=None,
    input_type=ledger__pb2._TRANSACTION,
    output_type=ledger__pb2._TRANSACTION,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='FindTransactions',
    full_name='pieledger.PieLedger.FindTransactions',
    index=3,
    containing_service=None,
    input_type=_TRANSACTIONQUERYREQUEST,
    output_type=ledger__pb2._TRANSACTION,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='AlterTransaction',
    full_name='pieledger.PieLedger.AlterTransaction',
    index=4,
    containing_service=None,
    input_type=ledger__pb2._TRANSACTION,
    output_type=ledger__pb2._TRANSACTION,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PIELEDGER)

DESCRIPTOR.services_by_name['PieLedger'] = _PIELEDGER

# @@protoc_insertion_point(module_scope)
