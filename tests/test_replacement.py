from unittest import TestCase
from itertools import combinations

from ordering import Ordering


class TestOrderingReplacement(TestCase):
    items_list = [0], [1, 0], [2, 0, 1]
    absent_list = 1, 2, 3

    def test_basic_replace(self) -> None:
        ordering = Ordering[int]((1, 0))

        ordering.replace(0, 42)
        self.assertNotIn(0, ordering)
        self.assertListEqual(list(ordering), [1, 42])
        ordering.replace(42, 0)
        self.assertNotIn(42, ordering)
        self.assertListEqual(list(ordering), [1, 0])

    def test_replace_same(self) -> None:
        for items in self.items_list:
            ordering = Ordering[int](items)
            for item in items:
                with self.subTest(items=items, item=item):
                    ordering.replace(item, item)
                    self.assertListEqual(list(ordering), items)

    def test_replace_len(self) -> None:
        for items, absent in zip(self.items_list, self.absent_list):
            for item in items:
                with self.subTest(items=items, existing=item, new=item):
                    ordering = Ordering[int](items)
                    ordering.replace(item, item)
                    self.assertEqual(len(ordering), len(items))

                with self.subTest(items=items, existing=item, new=absent):
                    ordering = Ordering[int](items)
                    ordering.replace(item, absent)
                    self.assertEqual(len(ordering), len(items))

    def test_replace_raises(self) -> None:
        absent_exc_re = 'does not contain'
        duplicate_exc_re = 'already contains'

        absent = 0
        with self.subTest(items=(), existing=absent, new=absent):
            with self.assertRaises(KeyError):
                ordering = Ordering[int](())
                ordering.replace(absent, absent)

        for items, absent in zip(self.items_list, self.absent_list):
            with self.subTest(items=items, existing=absent, new=absent):
                with self.assertRaisesRegex(KeyError, absent_exc_re):
                    ordering = Ordering[int](items)
                    ordering.replace(absent, absent)

            for a, b in combinations(items, 2):
                with self.subTest(items=items, existing=a, new=b):
                    with self.assertRaisesRegex(KeyError, duplicate_exc_re):
                        ordering = Ordering[int](items)
                        ordering.replace(a, b)

            for item in items:
                with self.subTest(items=items, existing=absent, new=item):
                    with self.assertRaisesRegex(KeyError, absent_exc_re):
                        ordering = Ordering[int](items)
                        ordering.replace(absent, item)
