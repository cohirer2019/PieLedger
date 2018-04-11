# -*- coding:utf-8 -*-
from google.protobuf.message import Message as PBMessage
from mapperpy import OneWayMapper, one_way_mapper
from mapperpy.attributes_util import get_attributes
from piecash import core

import ledger_pb2


def _get_attributes(obj):
    if isinstance(obj, PBMessage):
        return [f.name for f in obj.DESCRIPTOR.fields]
    return get_attributes(obj)


# Monkey patch the get_attributes
one_way_mapper.get_attributes = _get_attributes

account_mapper = OneWayMapper(ledger_pb2.Account)
account_mapper = account_mapper.nested_mapper(account_mapper, core.Account)
