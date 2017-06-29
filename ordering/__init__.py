from fractions import Fraction
from functools import total_ordering
from typing import Dict, Generic, TypeVar, Union


class _Sentinel:
    pass


T = TypeVar('T')
_T = Union[T, _Sentinel]


class Ordering(Generic[T]):
    _start = _Sentinel()
    _end = _Sentinel()

    def __init__(self) -> None:
        self._labels = {
            self._start: Fraction(0),
            self._end: Fraction(1)
        }  # type: Dict[_T, Fraction]
        self._successors = {
            self._start: self._end
        }  # type: Dict[_T, _T]
        self._predecessors = {
            self._end: self._start
        }  # type: Dict[_T, _T]

    def insert_after(self, existing_item: _T, new_item: T) -> 'OrderingItem[T]':
        self.assert_contains(existing_item)
        self.assert_new_item(new_item)

        self._labels[new_item] = (self._labels[existing_item] + self._labels[self._successors[existing_item]]) / 2
        self._successors[new_item] = self._successors[existing_item]
        self._predecessors[new_item] = existing_item

        self._predecessors[self._successors[existing_item]] = new_item
        self._successors[existing_item] = new_item

        return OrderingItem(self, new_item)

    def insert_before(self, existing_item: _T, new_item: T) -> 'OrderingItem[T]':
        return self.insert_after(self._predecessors[existing_item], new_item)

    def insert_start(self, new_item: T) -> 'OrderingItem[T]':
        return self.insert_after(self._start, new_item)

    def insert_end(self, new_item: T) -> 'OrderingItem[T]':
        return self.insert_before(self._end, new_item)

    def compare(self, left_item: T, right_item: T) -> bool:
        self.assert_contains(left_item)
        self.assert_contains(right_item)

        return self._labels[left_item] < self._labels[right_item]

    def __contains__(self, item: _T) -> bool:
        if isinstance(item, OrderingItem):
            return item.item in self._labels

        return item in self._labels

    def assert_contains(self, item: _T) -> None:
        if item not in self:
            raise KeyError("Ordering {} does not contain {}".format(self, item))

    def assert_new_item(self, item: T) -> None:
        if item in self:
            raise KeyError("Ordering {} already contains {}".format(self, item))


@total_ordering
class OrderingItem(Generic[T]):
    def __init__(self, ordering: Ordering[T], item: T) -> None:
        ordering.assert_contains(item)

        self.ordering = ordering
        self.item = item

    def __lt__(self, other: 'OrderingItem[T]') -> bool:
        return self.ordering.compare(self.item, other.item)

    def insert_before(self, item: T) -> 'OrderingItem[T]':
        return self.ordering.insert_before(self.item, item)

    def insert_after(self, item: T) -> 'OrderingItem[T]':
        return self.ordering.insert_after(self.item, item)
