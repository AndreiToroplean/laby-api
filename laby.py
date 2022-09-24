from __future__ import annotations

from collections.abc import Sequence, Callable, Iterable
import enum
from typing import Any


class Laby:
    @classmethod
    def zeros(cls, shape: Sequence[int]):
        return cls.full(shape)

    @classmethod
    def ones(cls, shape: Sequence[int]):
        return cls.full(shape, Node(Dir))

    @classmethod
    def full(cls, shape: Sequence[int], fill_value: Callable[[], Any] | Any = None):
        def get_data(shape_, fill_value_):
            if not shape_:
                try:
                    return fill_value_()
                except TypeError:
                    return fill_value_

            dim, *shape_ = shape_
            return [get_data(shape_, fill_value_) for _ in range(dim)]

        fill_value = fill_value or Node()
        return cls(get_data(shape, fill_value))

    def __init__(self, data: Sequence[Sequence]):
        self.data = data

    @property
    def strs(self) -> Iterable[str]:
        for row_nodes in self.data:
            for strs in zip(*(node.strs for node in row_nodes)):
                yield ''.join(strs)

    def __str__(self) -> str:
        return '\n'.join(self.strs)


class Node:
    def __init__(self, dirs: Sequence[Dir] | None = None):
        dirs = dirs or [
            # Dir.LEFT,
            # Dir.RIGHT,
            # Dir.UP,
            # Dir.DOWN,
        ]
        self.dirs = dirs

    @property
    def strs(self) -> Iterable[str]:
        yield f'{Chars.LRUD_CORNER}{Chars.EMPTY if Dir.UP in self.dirs else Chars.H_WALL}'
        yield f'{Chars.EMPTY if Dir.LEFT in self.dirs else Chars.V_WALL}{Chars.EMPTY}'

    def __str__(self) -> str:
        return '\n'.join(self.strs)


class Dir(enum.Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, 1)
    DOWN = (0, -1)


class Chars:
    H_SIZE = 4

    EMPTY = ' ' * H_SIZE
    H_WALL = '─' * H_SIZE
    V_WALL = '│'
    RD_CORNER = '┌'
    LD_CORNER = '┐'
    RU_CORNER = '└'
    LU_CORNER = '┘'
    LRU_CORNER = '┴'
    LRD_CORNER = '┬'
    RUD_CORNER = '├'
    LUD_CORNER = '┤'
    LRUD_CORNER = '┼'
