from __future__ import annotations

from collections.abc import Sequence, Callable, Iterable
from functools import cache, cached_property
from pprint import pformat
from typing import Any

from grid import Grid
from node import Node
from utils import Dirs, SetIndices


class Laby:
    @classmethod
    def zeros(cls, shape: Sequence[int]):
        return cls.full(shape, lambda: Node.zero())

    @classmethod
    def ones(cls, shape: Sequence[int]):
        return cls.full(shape, lambda: Node.one())

    @classmethod
    def full(cls, shape: Sequence[int], fill_value: Callable[[], Node] | Node | Any):
        def get_grid(shape_, fill_value_):
            if not shape_:
                try:
                    return fill_value_()
                except TypeError:
                    if isinstance(fill_value_, Node):
                        return fill_value_

                    return Node(fill_value)

            dim, *shape_ = shape_
            return [get_grid(shape_, fill_value_) for _ in range(dim)]

        return cls(Grid(get_grid(shape, fill_value)))

    def __init__(self, grid: Grid[Grid[Node]]):
        self._grid = grid
        self._enforce_walls()

        self._start = None
        self._finish = None

    @property
    def start(self) -> tuple[int, int]:
        return self._start

    @start.setter
    def start(self, indices: Sequence[int, int]):
        self._start = tuple(indices)
        self._grid[self._start].label = "|-->"

    @property
    def finish(self) -> tuple[int, int]:
        return self._finish

    @finish.setter
    def finish(self, indices: Sequence[int, int]):
        self._finish = tuple(indices)
        self._grid[self._finish].label = "-->|"

    def __getitem__(self, indices: SetIndices) -> Node:
        node = self._grid[indices]
        if not isinstance(node, Node):
            raise IndexError('Not enough indices to get a specific Node (cannot get sub-grids).')

        return node

    def _enforce_walls(self):
        for i, row in enumerate(self._grid):
            for j, node in enumerate(row):
                if i == 0:
                    node.dirs &= ~Dirs.UP
                if i == self._shape[0] - 1:
                    node.dirs &= ~Dirs.DOWN
                if j == 0:
                    node.dirs &= ~Dirs.LEFT
                if j == self._shape[1] - 1:
                    node.dirs &= ~Dirs.RIGHT

    def __str__(self) -> str:
        return '\n'.join(self.strs)

    @property
    def strs(self) -> Iterable[str]:
        for i, row in enumerate(self._display_grid):
            for strs in zip(*(node.strs(self._get_neighbors(i, j)) for j, node in enumerate(row))):
                yield ''.join(strs)

    @property
    def _display_grid(self) -> Grid[Grid[Node]]:
        display_grid = self._grid + [[Node.wall(Dirs.UP) for _ in range(self._shape[1])]]
        display_grid = Grid([row + [Node.wall(Dirs.LEFT)] for row in display_grid])
        display_grid[self._shape].dirs |= Dirs.ALL
        return display_grid

    @cache
    def _get_neighbors(self, i: int, j: int) -> dict[Dirs, Node]:
        def get_neighbor(i_: int, j_: int) -> Node:
            wall_dirs = Dirs.NONE
            if i_ < 0:
                wall_dirs |= Dirs.DOWN
            elif i_ >= max_i:
                wall_dirs |= Dirs.UP
            if j_ < 0:
                wall_dirs |= Dirs.RIGHT
            elif j_ >= max_j:
                wall_dirs |= Dirs.LEFT

            if wall_dirs:
                if wall_dirs & Dirs.H and wall_dirs & Dirs.V:
                    wall_dirs &= Dirs.NONE
                return Node.wall(wall_dirs)

            return self._grid[i_, j_]

        max_i, max_j = self._shape
        return {
            Dirs.LEFT: get_neighbor(i, j-1),
            Dirs.RIGHT: get_neighbor(i, j+1),
            Dirs.UP: get_neighbor(i-1, j),
            Dirs.DOWN: get_neighbor(i+1, j),
        }

    @cached_property
    def _shape(self) -> tuple[int, ...]:
        def get_shape(grid) -> tuple[int, ...]:
            try:
                sub_grid = grid[0]
            except TypeError:
                return ()

            return len(grid), *get_shape(sub_grid)

        return get_shape(self._grid)

    def __repr__(self) -> str:
        node_repr_lines = pformat(self._grid).splitlines()
        if len(node_repr_lines) == 1:
            nodes_repr, = node_repr_lines
        else:
            nodes_repr = '\n'.join(f'  {line}' for line in node_repr_lines)
            nodes_repr = f'\n{nodes_repr}\n'
        return f'{self.__class__.__name__}({nodes_repr})'
