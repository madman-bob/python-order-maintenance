from fractions import Fraction
from functools import total_ordering


class Ordering:
    _start = object()
    _end = object()

    def __init__(self):
        self._labels = {
            self._start: Fraction(0),
            self._end: Fraction(1)
        }
        self._successors = {
            self._start: self._end
        }
        self._predecessors = {
            self._end: self._start
        }

    def insert_after(self, existing_item, new_item):
        self.assert_contains(existing_item)

        self._labels[new_item] = (self._labels[existing_item] + self._labels[self._successors[existing_item]]) / 2
        self._successors[new_item] = self._successors[existing_item]
        self._predecessors[new_item] = existing_item

        self._predecessors[self._successors[existing_item]] = new_item
        self._successors[existing_item] = new_item

        return OrderingItem(self, new_item)

    def insert_before(self, existing_item, new_item):
        return self.insert_after(self._predecessors[existing_item], new_item)

    def insert_start(self, new_item):
        return self.insert_after(self._start, new_item)

    def insert_end(self, new_item):
        return self.insert_before(self._end, new_item)

    def compare(self, left_item, right_item):
        self.assert_contains(left_item)
        self.assert_contains(right_item)

        return self._labels[left_item] < self._labels[right_item]

    def __contains__(self, item):
        if isinstance(item, OrderingItem):
            return item.item in self._labels

        return item in self._labels

    def assert_contains(self, item):
        if item not in self:
            raise KeyError("Ordering {} does not contain {}".format(self, item))


@total_ordering
class OrderingItem:
    def __init__(self, ordering, item):
        ordering.assert_contains(item)

        self.ordering = ordering
        self.item = item

    def __lt__(self, other):
        return self.ordering.compare(self.item, other.item)
