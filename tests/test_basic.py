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

    def test_basic_clear(self) -> None:
        ordering = Ordering[int]([2, 0, 1])
        ordering.clear()

        with self.subTest('items not in ordering'):
            self.assertNotIn(0, ordering)
            self.assertNotIn(1, ordering)
            self.assertNotIn(2, ordering)

        with self.subTest('len(ordering) == 0'):
            self.assertEqual(len(ordering), 0)

        with self.subTest('list(ordering) == []'):
            self.assertListEqual(list(ordering), [])

    def test_ordering_empty_repr(self) -> None:
        self.assertEqual(repr(Ordering()), 'Ordering([])')

    def test_ordering_int_repr(self) -> None:
        with self.subTest(items=(0,)):
            self.assertEqual(repr(Ordering[int]((0,))), 'Ordering([0])')
        with self.subTest(items=(0, 1)):
            self.assertEqual(repr(Ordering[int]((0, 1))), 'Ordering([0, 1])')

    def test_ordering_str_repr(self) -> None:
        with self.subTest(items='a'):
            self.assertEqual(repr(Ordering[str]('a')), "Ordering(['a'])")
        with self.subTest(items='AaBb'):
            self.assertEqual(repr(Ordering[str]('AaBb')), "Ordering(['A', 'a', 'B', 'b'])")

    def test_ordering_item_repr_int(self) -> None:
        ordering_item = Ordering[int]((2, 0, 1))[1]
        self.assertEqual(repr(ordering_item), '<OrderingItem: 1>')

    def test_ordering_item_repr_str(self) -> None:
        ordering_item = Ordering[str]('cab')['a']
        self.assertEqual(repr(ordering_item), "<OrderingItem: 'a'>")
