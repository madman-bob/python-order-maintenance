from unittest import TestCase
from itertools import combinations, combinations_with_replacement as combinations_w_r

from ordering import Ordering


class TestOrderingSwapping(TestCase):
    items = (2, 0, 1)
    absents = (5, 7)

    def test_swap_two_existing_items(self) -> None:
        for (ai, a), (bi, b) in combinations_w_r(enumerate(self.items), 2):
            with self.subTest(a=a, b=b):
                ordering = Ordering[int](self.items)
                ordering.swap(a, b)
                items_copy = list(self.items)
                items_copy[ai], items_copy[bi] = items_copy[bi], items_copy[ai]
                self.assertListEqual(list(ordering), items_copy)

    def test_swap_commutativity(self) -> None:
        for a, b in combinations(self.items, 2):
            with self.subTest(a=a, b=b):
                ordering_ab = Ordering[int](self.items)
                ordering_ab.swap(a, b)
                ordering_ba = Ordering[int](self.items)
                ordering_ba.swap(b, a)
                self.assertListEqual(list(ordering_ab), list(ordering_ba))

    def test_swap_existing_with_absent_raises(self) -> None:
        absent_exc_re = 'Ordering.+does not contain'

        for item in self.items:
            with self.subTest(item=item, other=self.absents[0]):
                ordering = Ordering[int](self.items)
                with self.assertRaisesRegex(KeyError, absent_exc_re):
                    ordering.swap(item, self.absents[0])
                with self.assertRaisesRegex(KeyError, absent_exc_re):
                    ordering.swap(self.absents[0], item)

    def test_swap_two_absent_items_raises(self) -> None:
        for absent in self.absents:
            with self.subTest(item=absent, other=self.absents[0]):
                ordering = Ordering[int](self.items)
                with self.assertRaisesRegex(KeyError, 'Ordering.+does not contain'):
                    ordering.swap(absent, self.absents[0])
