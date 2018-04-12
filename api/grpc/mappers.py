# -*- coding:utf-8 -*-
from google.protobuf.message import Message as PBMessage
from mapperpy import OneWayMapper as _OneWayMapper, one_way_mapper
from mapperpy.attributes_util import get_attributes as _get_attributes, \
    AttributesCache as _AttributesCache
from piecash import core

import ledger_pb2


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


account_model_mapper = OneWayMapper(
    dict, {k: None for k in core.Account.__table__.columns.keys()})
account_model_mapper = account_model_mapper.target_initializers({
    'account_type': lambda obj: ledger_pb2.AccountType.Name(obj.type),
    'parent_guid': lambda obj: obj.parent.guid
})
