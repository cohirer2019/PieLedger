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


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ledger.proto',
  package='pieledger',
  syntax='proto3',
  serialized_pb=_b('\n\x0cledger.proto\x12\tpieledger\x1a\x1fgoogle/protobuf/timestamp.proto\"@\n\x0eMonetaryAmount\x12\x13\n\tas_string\x18\x01 \x01(\tH\x00\x12\x10\n\x06\x61s_int\x18\x02 \x01(\x12H\x00\x42\x07\n\x05value\"\xc2\x01\n\x07\x41\x63\x63ount\x12\x0c\n\x04guid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12$\n\x04type\x18\x03 \x01(\x0e\x32\x16.pieledger.AccountType\x12\"\n\x06parent\x18\x04 \x01(\x0b\x32\x12.pieledger.Account\x12\x13\n\x0bplaceholder\x18\x05 \x01(\x08\x12*\n\x07\x62\x61lance\x18\x06 \x01(\x0b\x32\x19.pieledger.MonetaryAmount\x12\x10\n\x08\x63urrency\x18\x07 \x01(\t\"\xda\x02\n\x05Split\x12\x0c\n\x04guid\x18\x01 \x01(\t\x12#\n\x07\x61\x63\x63ount\x18\x02 \x01(\x0b\x32\x12.pieledger.Account\x12\x31\n\x0fstandard_action\x18\n \x01(\x0e\x32\x16.pieledger.SplitActionH\x00\x12\x17\n\rcustom_action\x18\x0b \x01(\tH\x00\x12)\n\x06\x61mount\x18\x04 \x01(\x0b\x32\x19.pieledger.MonetaryAmount\x12\x32\n\x0frunning_balance\x18\x05 \x01(\x0b\x32\x19.pieledger.MonetaryAmount\x12\x0c\n\x04memo\x18\x06 \x01(\t\x12+\n\x0btransaction\x18\x07 \x01(\x0b\x32\x16.pieledger.Transaction\x12.\n\nenter_date\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x08\n\x06\x61\x63tion\"w\n\x0bTransaction\x12\x0c\n\x04guid\x18\x01 \x01(\t\x12\x11\n\treference\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x10\n\x08\x63urrency\x18\x04 \x01(\t\x12 \n\x06splits\x18\x05 \x03(\x0b\x32\x10.pieledger.Split*\xb7\x01\n\x0b\x41\x63\x63ountType\x12\x08\n\x04ROOT\x10\x00\x12\x0e\n\nRECEIVABLE\x10\x01\x12\n\n\x06MUTUAL\x10\x02\x12\x08\n\x04\x43\x41SH\x10\x03\x12\t\n\x05\x41SSET\x10\x04\x12\x08\n\x04\x42\x41NK\x10\x05\x12\t\n\x05STOCK\x10\x06\x12\n\n\x06\x43REDIT\x10\x07\x12\r\n\tLIABILITY\x10\x08\x12\x0b\n\x07PAYABLE\x10\t\x12\n\n\x06INCOME\x10\n\x12\x0b\n\x07\x45XPENSE\x10\x0b\x12\x0b\n\x07TRADING\x10\x0c\x12\n\n\x06\x45QUITY\x10\r*\xa9\x01\n\x0bSplitAction\x12\x05\n\x01_\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x05\n\x01\x42\x10\x01\x12\x07\n\x03\x42UY\x10\x01\x12\x05\n\x01S\x10\x02\x12\x08\n\x04SELL\x10\x02\x12\x05\n\x01\x44\x10\x03\x12\x0b\n\x07\x44\x45POSIT\x10\x03\x12\x05\n\x01I\x10\x04\x12\n\n\x06\x43\x41SHIN\x10\x04\x12\x05\n\x01W\x10\x05\x12\x0c\n\x08WITHDRAW\x10\x05\x12\x05\n\x01O\x10\x06\x12\x0b\n\x07\x43\x41SHOUT\x10\x06\x12\x05\n\x01R\x10\x07\x12\n\n\x06REFUND\x10\x07\x1a\x02\x10\x01\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])

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
  serialized_start=794,
  serialized_end=977,
)
_sym_db.RegisterEnumDescriptor(_ACCOUNTTYPE)

AccountType = enum_type_wrapper.EnumTypeWrapper(_ACCOUNTTYPE)
_SPLITACTION = _descriptor.EnumDescriptor(
  name='SplitAction',
  full_name='pieledger.SplitAction',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='_', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=1, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='B', index=2, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BUY', index=3, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S', index=4, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SELL', index=5, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='D', index=6, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEPOSIT', index=7, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='I', index=8, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CASHIN', index=9, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='W', index=10, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHDRAW', index=11, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O', index=12, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CASHOUT', index=13, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='R', index=14, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REFUND', index=15, number=7,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=_descriptor._ParseOptions(descriptor_pb2.EnumOptions(), _b('\020\001')),
  serialized_start=980,
  serialized_end=1149,
)
_sym_db.RegisterEnumDescriptor(_SPLITACTION)

SplitAction = enum_type_wrapper.EnumTypeWrapper(_SPLITACTION)
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
_ = 0
UNKNOWN = 0
B = 1
BUY = 1
S = 2
SELL = 2
D = 3
DEPOSIT = 3
I = 4
CASHIN = 4
W = 5
WITHDRAW = 5
O = 6
CASHOUT = 6
R = 7
REFUND = 7



_MONETARYAMOUNT = _descriptor.Descriptor(
  name='MonetaryAmount',
  full_name='pieledger.MonetaryAmount',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='as_string', full_name='pieledger.MonetaryAmount.as_string', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='as_int', full_name='pieledger.MonetaryAmount.as_int', index=1,
      number=2, type=18, cpp_type=2, label=1,
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
    _descriptor.OneofDescriptor(
      name='value', full_name='pieledger.MonetaryAmount.value',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=60,
  serialized_end=124,
)


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
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='currency', full_name='pieledger.Account.currency', index=6,
      number=7, type=9, cpp_type=9, label=1,
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
  serialized_start=127,
  serialized_end=321,
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
      name='standard_action', full_name='pieledger.Split.standard_action', index=2,
      number=10, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='custom_action', full_name='pieledger.Split.custom_action', index=3,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='amount', full_name='pieledger.Split.amount', index=4,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='running_balance', full_name='pieledger.Split.running_balance', index=5,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='memo', full_name='pieledger.Split.memo', index=6,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='transaction', full_name='pieledger.Split.transaction', index=7,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enter_date', full_name='pieledger.Split.enter_date', index=8,
      number=8, type=11, cpp_type=10, label=1,
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
    _descriptor.OneofDescriptor(
      name='action', full_name='pieledger.Split.action',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=324,
  serialized_end=670,
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
      name='currency', full_name='pieledger.Transaction.currency', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='splits', full_name='pieledger.Transaction.splits', index=4,
      number=5, type=11, cpp_type=10, label=3,
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
  serialized_start=672,
  serialized_end=791,
)

_MONETARYAMOUNT.oneofs_by_name['value'].fields.append(
  _MONETARYAMOUNT.fields_by_name['as_string'])
_MONETARYAMOUNT.fields_by_name['as_string'].containing_oneof = _MONETARYAMOUNT.oneofs_by_name['value']
_MONETARYAMOUNT.oneofs_by_name['value'].fields.append(
  _MONETARYAMOUNT.fields_by_name['as_int'])
_MONETARYAMOUNT.fields_by_name['as_int'].containing_oneof = _MONETARYAMOUNT.oneofs_by_name['value']
_ACCOUNT.fields_by_name['type'].enum_type = _ACCOUNTTYPE
_ACCOUNT.fields_by_name['parent'].message_type = _ACCOUNT
_ACCOUNT.fields_by_name['balance'].message_type = _MONETARYAMOUNT
_SPLIT.fields_by_name['account'].message_type = _ACCOUNT
_SPLIT.fields_by_name['standard_action'].enum_type = _SPLITACTION
_SPLIT.fields_by_name['amount'].message_type = _MONETARYAMOUNT
_SPLIT.fields_by_name['running_balance'].message_type = _MONETARYAMOUNT
_SPLIT.fields_by_name['transaction'].message_type = _TRANSACTION
_SPLIT.fields_by_name['enter_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_SPLIT.oneofs_by_name['action'].fields.append(
  _SPLIT.fields_by_name['standard_action'])
_SPLIT.fields_by_name['standard_action'].containing_oneof = _SPLIT.oneofs_by_name['action']
_SPLIT.oneofs_by_name['action'].fields.append(
  _SPLIT.fields_by_name['custom_action'])
_SPLIT.fields_by_name['custom_action'].containing_oneof = _SPLIT.oneofs_by_name['action']
_TRANSACTION.fields_by_name['splits'].message_type = _SPLIT
DESCRIPTOR.message_types_by_name['MonetaryAmount'] = _MONETARYAMOUNT
DESCRIPTOR.message_types_by_name['Account'] = _ACCOUNT
DESCRIPTOR.message_types_by_name['Split'] = _SPLIT
DESCRIPTOR.message_types_by_name['Transaction'] = _TRANSACTION
DESCRIPTOR.enum_types_by_name['AccountType'] = _ACCOUNTTYPE
DESCRIPTOR.enum_types_by_name['SplitAction'] = _SPLITACTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MonetaryAmount = _reflection.GeneratedProtocolMessageType('MonetaryAmount', (_message.Message,), dict(
  DESCRIPTOR = _MONETARYAMOUNT,
  __module__ = 'ledger_pb2'
  # @@protoc_insertion_point(class_scope:pieledger.MonetaryAmount)
  ))
_sym_db.RegisterMessage(MonetaryAmount)

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


_SPLITACTION.has_options = True
_SPLITACTION._options = _descriptor._ParseOptions(descriptor_pb2.EnumOptions(), _b('\020\001'))
# @@protoc_insertion_point(module_scope)
