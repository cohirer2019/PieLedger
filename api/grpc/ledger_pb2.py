# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ledger.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ledger.proto',
  package='pieledger',
  syntax='proto3',
  serialized_pb=_b('\n\x0cledger.proto\x12\tpieledger\"\x95\x01\n\x07\x41\x63\x63ount\x12\x0c\n\x04guid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12$\n\x04type\x18\x03 \x01(\x0e\x32\x16.pieledger.AccountType\x12\"\n\x06parent\x18\x04 \x01(\x0b\x32\x12.pieledger.Account\x12\x13\n\x0bplaceholder\x18\x05 \x01(\x08\x12\x0f\n\x07\x62\x61lance\x18\x06 \x01(\x11\"W\n\x05Split\x12\x0c\n\x04guid\x18\x01 \x01(\t\x12#\n\x07\x61\x63\x63ount\x18\x02 \x01(\x0b\x32\x12.pieledger.Account\x12\r\n\x05value\x18\x03 \x01(\x11\x12\x0c\n\x04memo\x18\x04 \x01(\t\"e\n\x0bTransaction\x12\x0c\n\x04guid\x18\x01 \x01(\t\x12\x11\n\treference\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12 \n\x06splits\x18\x04 \x03(\x0b\x32\x10.pieledger.Split*\xb7\x01\n\x0b\x41\x63\x63ountType\x12\x08\n\x04ROOT\x10\x00\x12\x0e\n\nRECEIVABLE\x10\x01\x12\n\n\x06MUTUAL\x10\x02\x12\x08\n\x04\x43\x41SH\x10\x03\x12\t\n\x05\x41SSET\x10\x04\x12\x08\n\x04\x42\x41NK\x10\x05\x12\t\n\x05STOCK\x10\x06\x12\n\n\x06\x43REDIT\x10\x07\x12\r\n\tLIABILITY\x10\x08\x12\x0b\n\x07PAYABLE\x10\t\x12\n\n\x06INCOME\x10\n\x12\x0b\n\x07\x45XPENSE\x10\x0b\x12\x0b\n\x07TRADING\x10\x0c\x12\n\n\x06\x45QUITY\x10\rb\x06proto3')
)

_ACCOUNTTYPE = _descriptor.EnumDescriptor(
  name='AccountType',
  full_name='pieledger.AccountType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ROOT', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECEIVABLE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MUTUAL', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CASH', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ASSET', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BANK', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STOCK', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CREDIT', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LIABILITY', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PAYABLE', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INCOME', index=10, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EXPENSE', index=11, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TRADING', index=12, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EQUITY', index=13, number=13,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=372,
  serialized_end=555,
)
_sym_db.RegisterEnumDescriptor(_ACCOUNTTYPE)

AccountType = enum_type_wrapper.EnumTypeWrapper(_ACCOUNTTYPE)
ROOT = 0
RECEIVABLE = 1
MUTUAL = 2
CASH = 3
ASSET = 4
BANK = 5
STOCK = 6
CREDIT = 7
LIABILITY = 8
PAYABLE = 9
INCOME = 10
EXPENSE = 11
TRADING = 12
EQUITY = 13



_ACCOUNT = _descriptor.Descriptor(
  name='Account',
  full_name='pieledger.Account',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='guid', full_name='pieledger.Account.guid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='pieledger.Account.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='pieledger.Account.type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parent', full_name='pieledger.Account.parent', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='placeholder', full_name='pieledger.Account.placeholder', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='balance', full_name='pieledger.Account.balance', index=5,
      number=6, type=17, cpp_type=1, label=1,
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
  serialized_start=28,
  serialized_end=177,
)


_SPLIT = _descriptor.Descriptor(
  name='Split',
  full_name='pieledger.Split',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='guid', full_name='pieledger.Split.guid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account', full_name='pieledger.Split.account', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='pieledger.Split.value', index=2,
      number=3, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='memo', full_name='pieledger.Split.memo', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=179,
  serialized_end=266,
)


_TRANSACTION = _descriptor.Descriptor(
  name='Transaction',
  full_name='pieledger.Transaction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='guid', full_name='pieledger.Transaction.guid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reference', full_name='pieledger.Transaction.reference', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='pieledger.Transaction.description', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='splits', full_name='pieledger.Transaction.splits', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=268,
  serialized_end=369,
)

_ACCOUNT.fields_by_name['type'].enum_type = _ACCOUNTTYPE
_ACCOUNT.fields_by_name['parent'].message_type = _ACCOUNT
_SPLIT.fields_by_name['account'].message_type = _ACCOUNT
_TRANSACTION.fields_by_name['splits'].message_type = _SPLIT
DESCRIPTOR.message_types_by_name['Account'] = _ACCOUNT
DESCRIPTOR.message_types_by_name['Split'] = _SPLIT
DESCRIPTOR.message_types_by_name['Transaction'] = _TRANSACTION
DESCRIPTOR.enum_types_by_name['AccountType'] = _ACCOUNTTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Account = _reflection.GeneratedProtocolMessageType('Account', (_message.Message,), dict(
  DESCRIPTOR = _ACCOUNT,
  __module__ = 'ledger_pb2'
  # @@protoc_insertion_point(class_scope:pieledger.Account)
  ))
_sym_db.RegisterMessage(Account)

Split = _reflection.GeneratedProtocolMessageType('Split', (_message.Message,), dict(
  DESCRIPTOR = _SPLIT,
  __module__ = 'ledger_pb2'
  # @@protoc_insertion_point(class_scope:pieledger.Split)
  ))
_sym_db.RegisterMessage(Split)

Transaction = _reflection.GeneratedProtocolMessageType('Transaction', (_message.Message,), dict(
  DESCRIPTOR = _TRANSACTION,
  __module__ = 'ledger_pb2'
  # @@protoc_insertion_point(class_scope:pieledger.Transaction)
  ))
_sym_db.RegisterMessage(Transaction)


# @@protoc_insertion_point(module_scope)
