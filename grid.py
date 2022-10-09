from __future__ import annotations

from typing import Any, Sequence, Union

_GridValue = Sequence[Union[Any, '_GridValue']]


class Grid(list):
    def __init__(self, value: _GridValue):
        try:
            value = [self.__class__(sub_value) for sub_value in value]
        except TypeError:
            pass

        super().__init__(value)

    def __repr__(self):
        return f'{self.__class__.__name__}({super().__repr__()})'

    def __setitem__(self, key: Sequence[int, ...] | int, value: _GridValue | Any):
        try:
            index, *indices = key
        except TypeError:
            if isinstance(value, Sequence):
                value = self.__class__(value)
            super().__setitem__(key, value)
            return

        if not indices:
            super().__setitem__(index, value)
            return

        self.__getitem__(index).__setitem__(indices, value)

    def __getitem__(self, key: Sequence[int | slice, ...] | int | slice) -> _GridValue | Any:
        try:
            index, *indices = key
        except TypeError:
            item = super().__getitem__(key)
            if isinstance(key, slice):
                item = self.__class__(item)
            return item

        item = self.__getitem__(index)
        if not indices:
            return item

        return item.__getitem__(indices)

    append = None

    def __add__(self, other):
        return self.__class__(super().__add__(other))
