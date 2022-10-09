from __future__ import annotations

from typing import Any, Sequence, Union

_GridValue = Sequence[Union[Any, '_GridValue']]


class Grid(list):
    def __init__(self, value: _GridValue):
        try:
            first_item = value[0]
        except IndexError:
            super().__init__(value)
            return

        if not all(type(item) is type(first_item) for item in value):
            raise TypeError('Inconsistent types in given Grid value.')

        if isinstance(first_item, self.__class__) or not isinstance(first_item, Sequence):
            super().__init__(value)
            return

        value = [self.__class__(item) for item in value]
        super().__init__(value)

    def __repr__(self):
        return f'{self.__class__.__name__}({super().__repr__()})'

    def __setitem__(self, index: Sequence[int, ...] | int, item: _GridValue | Any):
        try:
            index, *indices = index
        except TypeError:
            indices = ()

        if isinstance(item, Sequence):
            item = self.__class__(item)

        if not indices:
            super().__setitem__(index, item)
            return

        self.__getitem__(index).__setitem__(indices, item)

    def __getitem__(self, index: Sequence[int | slice, ...] | int | slice) -> _GridValue | Any:
        try:
            index, *indices = index
        except TypeError:
            indices = ()

        item = super().__getitem__(index)
        if isinstance(index, slice):
            item = self.__class__(item)
        if not indices:
            return item

        return item.__getitem__(indices)

    def append(self, item: _GridValue | Any):
        if isinstance(item, Sequence) and not isinstance(item, self.__class__):
            item = self.__class__(item)
        super().append(item)

    def __add__(self, other: Grid | Sequence):
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return super().__add__(other)
