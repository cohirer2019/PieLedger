# -*- coding:utf-8 -*-


class BaseManager(object):

    def __init__(self, book):
        self.book = book
        self.session = book.session

    def find_by_guid(self, guid):
        return self.book.query(self.model).get(guid)
