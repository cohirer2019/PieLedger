# -*- coding:utf-8 -*-
from sqlalchemy import func, distinct
from sqlalchemy.orm import lazyload, contains_eager
from sqlalchemy.orm.util import AliasedClass


class BaseManager(object):

    def __init__(self, book):
        self.book = book
        self.session = book.session

    def find_by_guid(self, guid):
        return self.book.query(self.model).get(guid)

    @staticmethod
    def get_count(q):
        assert len(q._entities) == 1, \
            'only one entity is supported for get_count, got: %s' % q._entities

        entity = q._entities[0]
        if hasattr(entity, 'column'):
            # _ColumnEntity has column attr - on case: query(Model.column)...
            col = entity.column
            count_func = func.count(distinct(col))
        else:
            # _MapperEntity doesn't have column attr - on case: query(Model)...
            count_func = func.count(distinct(*q._group_by)) if q._group_by \
                else func.count()

        count_q = q.options(lazyload('*')).statement.with_only_columns(
            [count_func]).order_by(None).group_by(None)
        return q.session.execute(count_q).scalar()

    @staticmethod
    def eager_load(query, entity, *columns):
        if entity not in (j.entity for j in query._join_entities):
            query = query.outerjoin(entity, columns[-1])
        kw = {}
        if isinstance(entity, AliasedClass):
            kw['alias'] = entity
        return query.options(contains_eager(*columns, **kw))
