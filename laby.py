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
        return cls.full(shape, Node(Dirs.ALL))

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
            for strs in zip(*(node.strs() for node in row_nodes)):
                yield ''.join(strs)

    def __str__(self) -> str:
        return '\n'.join(self.strs)


class Node:
    @classmethod
    def all(cls):
        return cls(Dirs.ALL)

    def __init__(self, dirs: Dirs | None = None):
        dirs = dirs or Dirs.NONE
        self.dirs = dirs

    def __str__(self) -> str:
        return '\n'.join(self.strs())

    def strs(self, neighbors: dict[Dirs, Node] | None = None) -> Iterable[str]:
        if neighbors is None:
            return self._basic_strs()

        return (''.join(strs[-1]) for strs in self._all_strs(neighbors)[-1])

    def _all_strs(self, neighbors: dict[Dirs, Node]) -> Sequence[Sequence[str]]:

        def corner_char(corner_dir: Dirs) -> str:
            h_dir = corner_dir & Dirs.LEFT
            v_dir = corner_dir & Dirs.UP

            # Assert good use of this function.
            assert not corner_dir & Dirs.LEFT or not corner_dir & Dirs.RIGHT
            assert not corner_dir & Dirs.UP or not corner_dir & Dirs.DOWN
            assert h_dir and v_dir

            return Char.CORNER[
                Dirs.NONE if neighbors[h_dir].dirs & v_dir else h_dir
                | Dirs.NONE if neighbors[v_dir].dirs & ~v_dir else ~h_dir
                | Dirs.NONE if neighbors[v_dir].dirs & h_dir else v_dir
                | Dirs.NONE if neighbors[h_dir].dirs & ~h_dir else ~v_dir
            ]

        self._check_neighbors(neighbors)

        return [
            [
                corner_char(Dirs.LEFT | Dirs.UP),
                Char.H_SPACE if self.dirs & Dirs.UP else Char.H_WALL,
                corner_char(Dirs.RIGHT | Dirs.UP),
            ],
            [
                Char.V_SPACE if self.dirs & Dirs.LEFT else Char.V_WALL,
                Char.H_SPACE,
                Char.V_SPACE if self.dirs & Dirs.RIGHT else Char.V_WALL,
            ],
            [
                corner_char(Dirs.LEFT | Dirs.DOWN),
                Char.H_SPACE if self.dirs & Dirs.DOWN else Char.H_WALL,
                corner_char(Dirs.RIGHT | Dirs.DOWN),
            ],
        ]

    def _check_neighbors(self, neighbors: dict[Dirs, Node]):
        def check_neighbor(neighbor_dir: Dirs) -> bool:
            return self.dirs & neighbor_dir and neighbors[neighbor_dir].dirs & ~neighbor_dir

        for dir_ in Dirs.seq():
            if not check_neighbor(dir_):
                raise Exception("Incompatible neighboring nodes.")

    def _basic_strs(self) -> Iterable[str]:
        yield f'{Char.LRUD_CORNER}{Char.H_SPACE if Dirs.UP in self.dirs else Char.H_WALL}'
        yield f'{Char.V_SPACE if Dirs.LEFT in self.dirs else Char.V_WALL}{Char.H_SPACE}'


class Dirs(enum.Flag):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()

    H = LEFT | RIGHT
    V = UP | DOWN

    ALL = H | V
    NONE = 0

    @staticmethod
    def seq():
        return Dirs.LEFT, Dirs.RIGHT, Dirs.UP, Dirs.DOWN

    def __invert__(self):
        try:
            return DIR_INVERSES[self]
        except KeyError as e:
            raise NotImplementedError(f"Arbitrary Dirs compositions don't always have inverses.") from e


class SymmetricDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update({v: k for k, v in self.items()})


DIR_INVERSES = SymmetricDict({
    Dirs.LEFT: Dirs.RIGHT,
    Dirs.UP: Dirs.DOWN,

    Dirs.H: Dirs.V,

    Dirs.ALL: Dirs.NONE,
})


class Char:
    H_SIZE = 4

    H_SPACE = ' ' * H_SIZE
    H_WALL = '─' * H_SIZE
    V_SPACE = ' '
    V_WALL = '│'

    L_CORNER = '╴'
    R_CORNER = '╶'
    U_CORNER = '╵'
    D_CORNER = '╷'
    RD_CORNER = '┌'
    LD_CORNER = '┐'
    RU_CORNER = '└'
    LU_CORNER = '┘'
    LRU_CORNER = '┴'
    LRD_CORNER = '┬'
    RUD_CORNER = '├'
    LUD_CORNER = '┤'
    LRUD_CORNER = '┼'

    CORNER = {
        Dirs.LEFT: L_CORNER,
        Dirs.RIGHT: R_CORNER,
        Dirs.UP: U_CORNER,
        Dirs.DOWN: D_CORNER,
        Dirs.RIGHT | Dirs.DOWN: RD_CORNER,
        Dirs.LEFT | Dirs.DOWN: LD_CORNER,
        Dirs.RIGHT | Dirs.UP: RU_CORNER,
        Dirs.LEFT | Dirs.UP: LU_CORNER,
        Dirs.LEFT | Dirs.RIGHT | Dirs.UP: LRU_CORNER,
        Dirs.LEFT | Dirs.RIGHT | Dirs.DOWN: LRD_CORNER,
        Dirs.RIGHT | Dirs.UP | Dirs.DOWN: RUD_CORNER,
        Dirs.LEFT | Dirs.UP | Dirs.DOWN: LUD_CORNER,
        Dirs.LEFT | Dirs.RIGHT | Dirs.UP | Dirs.DOWN: LRUD_CORNER,
    }
