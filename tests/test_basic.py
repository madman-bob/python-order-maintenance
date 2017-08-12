from unittest import TestCase

from ordering import Ordering


class TestOrderingBasic(TestCase):
    def test_empty_insert_start(self) -> None:
        ordering = Ordering[int]()
        ordering.insert_start(0)

        self.assertIn(0, ordering)
        self.assertNotIn(1, ordering)

    def test_empty_insert_end(self) -> None:
        ordering = Ordering[int]()
        ordering.insert_end(0)

        self.assertIn(0, ordering)
        self.assertNotIn(1, ordering)

    def test_remove(self) -> None:
        ordering = Ordering[int]()

        self.assertNotIn(0, ordering)
        ordering.insert_start(0)
        self.assertIn(0, ordering)
        ordering.remove(0)
        self.assertNotIn(0, ordering)

    def test_basic_insert_after(self) -> None:
        ordering = Ordering[int]()
        ordering.insert_start(0)
        ordering.insert_after(0, 1)

        self.assertIn(0, ordering)
        self.assertIn(1, ordering)
        self.assertNotIn(2, ordering)

    def test_basic_insert_before(self) -> None:
        ordering = Ordering[int]()
        ordering.insert_start(0)
        ordering.insert_before(0, 1)

        self.assertIn(0, ordering)
        self.assertIn(1, ordering)
        self.assertNotIn(2, ordering)

    def test_basic_compare(self) -> None:
        ordering = Ordering[int]()
        ordering.insert_start(0)

        ordering.insert_after(0, 1)
        ordering.insert_before(0, 2)

        self.assertTrue(ordering.compare(0, 1))
        self.assertFalse(ordering.compare(1, 0))

        self.assertTrue(ordering.compare(2, 0))
        self.assertFalse(ordering.compare(0, 2))

    def test_iterator_initialization(self) -> None:
        ordering = Ordering[int]([2, 0, 1])

        self.assertTrue(ordering.compare(2, 0))
        self.assertTrue(ordering.compare(2, 1))
        self.assertTrue(ordering.compare(0, 1))

    def test_reverse_iter(self) -> None:
        items: list
        for items in [], [0], [0, 1], [2, 0, 1]:  # type: ignore # https://github.com/python/mypy/issues/2255
            with self.subTest(items=items):
                ordering = Ordering[int](items)
                ordering.reverse()
                self.assertListEqual(list(ordering), items[::-1])

    def test_reverse_compare(self) -> None:
        for items in [0, 1], [2, 0, 1], [2, 0, 1, 3]:
            ordering = Ordering[int](items)
            ordering.reverse()
            for greater, lesser in zip(items, items[1:]):
                with self.subTest(items=items, lesser=lesser, greater=greater):
                    self.assertLess(ordering[lesser], ordering[greater])
