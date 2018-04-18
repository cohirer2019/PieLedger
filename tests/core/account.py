# -*- coding:utf-8 -*-
from mock import patch

from .base import BaseTestCase, book_context


class CoreAccountTest(BaseTestCase):

    @book_context
    def test_dup_account_name(self, book):
        """Disallow duplicated account name under same parent.

        The duplicated account name check machenism is patched from piecash
        and is now utilizing db query for efficiency consideration.
        """
        acc1 = self.make_account(book, 'dup_name', 'ASSET')
        acc2 = self.make_account(book, 'dup_name', 'CASH')

        # Duplicated name raises exception
        with self.assertRaises(ValueError):
            book.save()

        # Name could dup if parent is different
        acc2.parent = acc1
        book.save()
        self.assertEqual(acc2.parent_guid, acc1.guid)

    @book_context
    def test_cache_balance(self, book):
        """Account balance is properly cached

        An additional field is added to the account model to cache the
        caculated result.
        """
        acc_from = self.make_account(book, 'from', 'ASSET')
        acc_to = self.make_account(book, 'to', 'CASH')
        self.transfer(acc_from, acc_to, 10)
        book.save()

        with patch.object(
                book.session, 'query',
                wraps=book.session.query) as query:

            # if balance not cached, query is called
            acc_from._cached_balance = None
            self.assertEquals(acc_from.get_balance(), -10)
            self.assertTrue(query.called)

            # if balance is cached, query is not called
            query.reset_mock()
            self.assertEquals(acc_from._cached_balance, -10)
            self.assertEquals(acc_from.get_balance(), -10)
            self.assertFalse(query.called)

    @book_context
    def test_get_balance(self, book):
        """Account balance is properly caculated

        The balance calculation method is patched from piecach for a single sum
        query for all splits to reduce the fetching / calculation overhead for
        large amounts of transactions.
        """
        # Root account is not allowed to get balance
        with self.assertRaises(AssertionError):
            book.root_account.get_balance()

        acc_from = self.make_account(book, 'from', 'ASSET')
        acc_to = self.make_account(book, 'to', 'CASH')
        self.transfer(acc_from, acc_to, 10)
        book.flush()

        # Balance is calculated
        self.assertEqual(acc_from.get_balance(), -10)
        self.assertEqual(acc_to.get_balance(), 10)

        # With child accounts
        acc_to_child = self.make_account(
            book, 'to_child', 'CASH', parent=acc_to)
        self.transfer(acc_to, acc_to_child, 2)
        book.flush()

        # Recusive returns all balance
        self.assertEqual(acc_to.get_balance(), 10)
        # Individual account balance
        self.assertEqual(acc_to.get_balance(recurse=False), 8)
        self.assertEqual(acc_to_child.get_balance(), 2)

        # Rollbackable (to the state before flush occures)
        book.cancel()
        self.assertEqual(acc_from.get_balance(), -10)
        self.assertEqual(acc_to.get_balance(), 10)
