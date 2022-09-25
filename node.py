from __future__ import annotations

from collections.abc import Sequence, Iterable
from utils import Dirs, Char


class Node:
    @classmethod
    def zero(cls):
        return cls(Dirs.NONE)

    @classmethod
    def one(cls):
        return cls(Dirs.ALL)

    @classmethod
    def wall(cls, wall_dirs):
        node = cls(~wall_dirs)
        node._is_wall = True
        return node

    def __init__(self, dirs: Dirs):
        self.dirs = dirs
        self._is_wall = False

    def __str__(self) -> str:
        return '\n'.join(self.strs())

    def strs(self, neighbors: dict[Dirs, Node] | None = None) -> Iterable[str]:
        if neighbors is None:
            return self._basic_strs()

        return (''.join(strs[:-1]) for strs in self._strs_seqs(neighbors)[:-1])

    def _strs_seqs(self, neighbors: dict[Dirs, Node]) -> Sequence[Sequence[str]]:
        def get_corner_char(corner_dir: Dirs) -> str:
            h_dir = corner_dir & Dirs.H
            v_dir = corner_dir & Dirs.V

            # Assert good use of this function.
            assert not corner_dir & Dirs.LEFT or not corner_dir & Dirs.RIGHT
            assert not corner_dir & Dirs.UP or not corner_dir & Dirs.DOWN
            assert h_dir and v_dir

            char = Char.CORNER[
                (Dirs.NONE if neighbors[h_dir].dirs & v_dir else h_dir)
                | (Dirs.NONE if neighbors[v_dir].dirs & v_dir.opposite() else h_dir.opposite())
                | (Dirs.NONE if neighbors[v_dir].dirs & h_dir else v_dir)
                | (Dirs.NONE if neighbors[h_dir].dirs & h_dir.opposite() else v_dir.opposite())
            ]
            return char

        self._check_neighbors(neighbors)
        strs_seqs = [
            [
                get_corner_char(Dirs.LEFT | Dirs.UP),
                Char.H_SPACE if self.dirs & Dirs.UP else Char.H_WALL,
                get_corner_char(Dirs.RIGHT | Dirs.UP),
            ],
            [
                Char.V_SPACE if self.dirs & Dirs.LEFT else Char.V_WALL,
                Char.H_SPACE,
                Char.V_SPACE if self.dirs & Dirs.RIGHT else Char.V_WALL,
            ],
            [
                get_corner_char(Dirs.LEFT | Dirs.DOWN),
                Char.H_SPACE if self.dirs & Dirs.DOWN else Char.H_WALL,
                get_corner_char(Dirs.RIGHT | Dirs.DOWN),
            ],
        ]
        return strs_seqs

    def _check_neighbors(self, neighbors: dict[Dirs, Node]):
        def check_neighbor(neighbor_dir: Dirs) -> bool:
            return (
                (self.dirs & neighbor_dir or not neighbors[neighbor_dir].dirs & neighbor_dir.opposite())
                and (not self.dirs & neighbor_dir or neighbors[neighbor_dir].dirs & neighbor_dir.opposite())
            )
        if self._is_wall:
            return

        for dir_ in Dirs.seq():
            if not check_neighbor(dir_):
                raise Exception("Incompatible neighboring nodes.")

    def _basic_strs(self) -> Iterable[str]:
        yield f'{Char.LRUD_CORNER}{Char.H_SPACE if Dirs.UP in self.dirs else Char.H_WALL}'
        yield f'{Char.V_SPACE if Dirs.LEFT in self.dirs else Char.V_WALL}{Char.H_SPACE}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.dirs})'
