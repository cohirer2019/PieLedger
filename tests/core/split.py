# -*- coding:utf-8 -*-
import threading

import backoff
from sqlalchemy.exc import DatabaseError

from core.book import open_book
from .base import BaseTestCase, book_context


class CoreSplitTest(BaseTestCase):

    @book_context
    def test_running_balance(self, book):
        """Running total of splits is caculated correctly"""
        acc1 = self.make_account(book, 'from', 'ASSET')
        acc2 = self.make_account(book, 'to_random', 'CASH')

        # Random order
        for amount in (100, -10, -10):
            self.transfer(acc1, acc2, amount)
        book.flush()

        self.assertEqual(acc2.get_balance(), 80)
        # One of the sequence could be the result sequence
        self.assertIn(
            sorted([s.running_balance for s in acc2.splits]),
            ([80, 90, 100], [-10, 80, 90], [-20, -10, 80]))

        acc2 = self.make_account(book, 'to_ordered', 'CASH')
        book.flush()

        # Strict order
        for amount in (100, -10, -10):
            self.transfer(acc1, acc2, amount)
            book.flush()  # ensure the order

        self.assertCountEqual(
            [s.running_balance for s in acc2.splits], (100, 90, 80))

    @book_context(join_session=False)
    def test_running_balance_concurrent(self, book):
        """Concurrent running total calculation is handled properly

        Account releated to the calculated split is locked. Error hanlding
        machenism need to be applied to ensure the saving.
        """
        CONCURRENCY = 5

        acc1 = self.make_account(book, 'from', 'ASSET')
        acc2 = self.make_account(book, 'to', 'CASH')
        self.transfer(acc1, acc2, 10)
        book.save()
        self.deleteAfter(acc1, acc2)

        # The client is responsable for capturing db exception and retry
        # Here a random jitter with 50ms max interval is used for retrying
        @backoff.on_exception(
            backoff.constant, DatabaseError, jitter=backoff.full_jitter,
            interval=0.05)
        def transfer(acc1, acc2, amount):
            with open_book() as thread_book:
                acc1 = thread_book.session.merge(acc1)
                acc2 = thread_book.session.merge(acc2)
                self.transfer(acc1, acc2, amount)
                thread_book.save()

        threads = [
            threading.Thread(target=transfer, args=[acc1, acc2, 1])
            for _ in range(CONCURRENCY)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertCountEqual(
            range(10, CONCURRENCY+11),
            [s.running_balance for s in acc2.splits])
