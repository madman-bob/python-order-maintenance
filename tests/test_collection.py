from unittest import TestCase

from ordering import Ordering


class TestOrderingAsCollection(TestCase):
    def setUp(self) -> None:
        self.ordering = Ordering[int]()
        self.ordering.insert_start(0)
        for n in range(10):
            self.ordering.insert_after(n, n + 1)

    def test_length(self) -> None:
        self.assertEqual(len(self.ordering), 11)

    def test_iterates_over_correct_elements(self) -> None:
        self.assertListEqual(
            list(self.ordering),
            list(range(11))
        )

    def test_contains_correct_elements(self) -> None:
        for n in range(11):
            self.assertIn(n, self.ordering)

        for n in range(11, 20):
            self.assertNotIn(n, self.ordering)

        for n in range(-10, 0):
            self.assertNotIn(n, self.ordering)
