from itertools import combinations
from unittest import TestCase

from ordering import Ordering


class TestComparisons(TestCase):
    def setUp(self) -> None:
        self.ordering = Ordering[int]()

        self.ordering.insert_start(0)
        self.ordering.insert_after(0, 1)
        self.ordering.insert_before(0, 2)
        self.ordering.insert_end(3)
        self.ordering.insert_start(4)
        self.ordering.insert_after(3, 5)
        self.ordering.insert_before(3, 6)

        self.ordering_list = [4, 2, 0, 1, 6, 3, 5]

    def test_iterate_correct_order(self) -> None:
        self.assertListEqual(
            list(self.ordering),
            self.ordering_list
        )

    def test_comparisons(self) -> None:
        for a, b in combinations(self.ordering_list, 2):
            self.assertTrue(self.ordering.compare(a, b))
            self.assertFalse(self.ordering.compare(b, a))

    def test_sorting(self) -> None:
        self.assertListEqual(
            sorted(range(3), key=self.ordering),  # type:ignore # https://github.com/python/mypy/issues/797
            [2, 0, 1]
        )
