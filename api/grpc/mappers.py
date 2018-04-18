# -*- coding:utf-8 -*-
from google.protobuf.message import Message as PBMessage
from mapperpy import OneWayMapper as _OneWayMapper, one_way_mapper
from mapperpy.attributes_util import get_attributes as _get_attributes, \
    AttributesCache as _AttributesCache
from piecash import core

from . import ledger_pb2


def get_attributes(obj):
    if isinstance(obj, PBMessage):
        return [f.name for f in obj.DESCRIPTOR.fields]
    return _get_attributes(obj)


# Monkey patch the get_attributes
one_way_mapper.get_attributes = get_attributes


class AttributesCache(_AttributesCache):
    def __init__(self):
        super(AttributesCache, self).__init__(
            get_attributes_func=get_attributes)


class OneWayMapper(_OneWayMapper):
    def __init__(self, *args, **kw):
        super(OneWayMapper, self).__init__(
            attributes_cache_provider=AttributesCache, *args, **kw)


account_mapper = OneWayMapper(ledger_pb2.Account)
account_mapper = account_mapper.nested_mapper(account_mapper, core.Account)


# 把protocol buffer的Account model转换成可以直接被piecash的Account使用的dict
account_model_mapper = OneWayMapper(
    dict, {k: None for k in core.Account.__table__.columns.keys()}
).target_initializers({
    'type': lambda obj: ledger_pb2.AccountType.Name(obj.type),
    'parent_guid': lambda obj: obj.parent.guid
}).custom_mappings({
    'guid': None
})


split_mapper = OneWayMapper(ledger_pb2.Split).nested_mapper(
    account_mapper, core.Account
).target_initializers({
    'amount': lambda obj: ledger_pb2.MonetaryAmount(
        value=str(obj.value), num=obj._value_num, denom=obj._value_denom),
    'action': lambda obj: obj.action or 'UNKNOWN'
}).custom_mappings({
    'transaction': None
})


split_model_mapper = OneWayMapper(
    dict, {k: None for k in core.Split.__table__.columns.keys()}
).target_initializers({
    'value': lambda obj: obj.amount.value and int(obj.amount.value),
    'account': lambda obj: obj.account.guid,
    'action': lambda obj: ledger_pb2.SplitAction.Name(obj.action)
}).custom_mappings({
    'guid': None
})

transaction_mapper = OneWayMapper(
    ledger_pb2.Transaction
).target_initializers({
    'splits': lambda o: [split_mapper.map(s) for s in o.splits]
})

transaction_model_mapper = OneWayMapper(
    dict, {k: None for k in core.Transaction.__table__.columns.keys()}
).custom_mappings({
    'guid': None,
    'reference': 'num'
}).target_initializers({
    'splits': lambda o: [split_model_mapper.map(s) for s in o.splits]
})

transquery_model_mapper = OneWayMapper(
    dict, {k: None for k in core.Transaction.__table__.columns.keys()}
).target_initializers({
    'guids': lambda obj: obj.guids,
    'account': lambda obj: obj.account,
    'page_number': lambda obj: obj.page_number,
    'result_per_page': lambda obj: obj.result_per_page
})
