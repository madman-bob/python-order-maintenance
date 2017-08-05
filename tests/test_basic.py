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

    def test_iterator_initialization_duplicates(self) -> None:
        items_list: list = [[1, '1'], [1, 1+1j], ['a', b'a']]
        for items in items_list:
            with self.subTest(items=items):
                self.assertListEqual(list(Ordering(items)), items)

        items_list = [[1, 1], [1, 1.0], [1, 1+0j], [0, 0, 1], [0, 1, 0], [1, 0, 0], 'abracadabra']
        for items in items_list:
            with self.subTest(items=items):
                with self.assertRaisesRegex(ValueError, 'attempt to create Ordering containing duplicate items'):
                    Ordering(items)
