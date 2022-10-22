from __future__ import annotations

from collections.abc import Sequence, Iterable
from char import Char
from dirs import Dirs


class Node:
    @classmethod
    def zero(cls, *args, **kwargs):
        return cls(Dirs.NONE, *args, **kwargs)

    @classmethod
    def one(cls, *args, **kwargs):
        return cls(Dirs.ALL, *args, **kwargs)

    @classmethod
    def virtual(cls, wall_dirs, *args, **kwargs):
        node = cls(~wall_dirs, *args, **kwargs)
        node._is_virtual = True
        return node

    def __init__(self, dirs: Dirs):
        self.dirs = dirs
        self.label = None
        self._is_virtual = False

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

        def get_edge_char(edge_dir: Dirs) -> str:
            is_empty = self.dirs & edge_dir
            is_h = Dirs.H & edge_dir
            if is_empty:
                return Char.V_SPACE if is_h else Char.H_SPACE
            else:
                return Char.V_WALL if is_h else Char.H_WALL

        def get_center_char() -> str:
            if self.label is None:
                return Char.H_SPACE

            h_len = len(Char.H_SPACE)
            return self.label[:h_len] + ' ' * (max(h_len - len(self.label), 0))

        strs_seqs = [
            [
                get_corner_char(Dirs.LEFT | Dirs.UP),
                get_edge_char(Dirs.UP),
                get_corner_char(Dirs.RIGHT | Dirs.UP),
            ],
            [
                get_edge_char(Dirs.LEFT),
                get_center_char(),
                get_edge_char(Dirs.RIGHT),
            ],
            [
                get_corner_char(Dirs.LEFT | Dirs.DOWN),
                get_edge_char(Dirs.DOWN),
                get_corner_char(Dirs.RIGHT | Dirs.DOWN),
            ],
        ]
        return strs_seqs

    def _basic_strs(self) -> Iterable[str]:
        yield f'{Char.LRUD_CORNER}{Char.H_SPACE if Dirs.UP in self.dirs else Char.H_WALL}'
        yield f'{Char.V_SPACE if Dirs.LEFT in self.dirs else Char.V_WALL}{Char.H_SPACE}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.dirs})'
