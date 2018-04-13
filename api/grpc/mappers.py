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

    def __apply_mapping(self, source_obj, attr_name_mapping):

        mapped_params_dict = {}

        for attr_name_from, attr_name_to in attr_name_mapping.items():
            # skip since mapping is suppressed by user (attribute_name = None)
            if not (attr_name_from and attr_name_to):
                continue

            source_attr_value = self.__get_attribute_value(source_obj, attr_name_from)
            if self.__do_apply_mapping(attr_name_from, attr_name_to, source_attr_value):
                mapped_params_dict[attr_name_to] = self.__do_apply_mapping(attr_name_from, attr_name_to, source_attr_value)

        return mapped_params_dict


account_mapper = OneWayMapper(ledger_pb2.Account)
account_mapper = account_mapper.nested_mapper(account_mapper, core.Account)


account_model_mapper = OneWayMapper(
    dict, {k: None for k in core.Account.__table__.columns.keys()})
account_model_mapper = account_model_mapper.target_initializers({
    'type': lambda obj: ledger_pb2.AccountType.Name(obj.type),
    'parent_guid': lambda obj: obj.parent.guid
})


transaction_mapper = OneWayMapper(ledger_pb2.Transaction)
split_mapper = OneWayMapper(ledger_pb2.Split)
split_mapper = split_mapper.nested_mapper(account_mapper, core.Account)
split_mapper = split_mapper.target_initializers({
    'value': lambda obj: int(obj.value),
})


transaction_mapper = transaction_mapper.target_initializers({
    'splits': lambda obj: [split_mapper.map(split) for split in obj.splits]})

transaction_model_mapper = OneWayMapper(
    dict, {k: None for k in core.Transaction.__table__.columns.keys()})
transaction_model_mapper = transaction_model_mapper.target_initializers({
    'guids': lambda obj: obj.guids,
    'account': lambda obj: obj.account,
    'page_number': lambda obj: obj.page_number,
    'result_per_page': lambda obj: obj.result_per_page
})
