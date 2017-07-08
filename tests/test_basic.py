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
