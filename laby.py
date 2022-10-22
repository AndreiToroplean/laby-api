from __future__ import annotations

from collections.abc import Sequence, Callable, Iterable
from functools import cache, cached_property
from typing import Any

from char import Char
from grid import Grid
from node import Node
from routing import Route
from utils import SetIndices
from dirs import Dirs, Pos


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

    @classmethod
    def from_letters(cls, letters_grid: str):
        grid = Grid([[Node(Dirs.from_letters(letters.strip().lower())) for letters in row_letters.split(',')]
                     for row_letters in letters_grid.splitlines()])
        return cls(grid)

    @classmethod
    def from_dirs(cls, dirs: Sequence[Sequence[Dirs]]):
        grid = Grid([[Node(dir_) for dir_ in dirs_row] for dirs_row in dirs])
        return cls(grid)

    def __init__(self, grid: Grid[Grid[Node]]):
        self._grid = grid
        self._enforce_walls()

        self._start = None
        self._finish = None

    @property
    def start(self) -> Pos:
        return self._start

    @start.setter
    def start(self, indices: Sequence[int, int]):
        self._start = Pos(indices)
        self._grid[self._start].label = Char.START

    @property
    def finish(self) -> Pos:
        return self._finish

    @finish.setter
    def finish(self, indices: Sequence[int, int]):
        self._finish = Pos(indices)
        self._grid[self._finish].label = Char.FINISH

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

    def write_route(self, route: Route):
        for route_point in route:
            node = self._grid[route_point.pos]
            if not route_point.dirs:
                continue

            node.route_dirs |= route_point.dirs[-1]

    def __str__(self) -> str:
        return '\n'.join(self.strs)

    @property
    def strs(self) -> Iterable[str]:
        for i, row in enumerate(self._display_grid):
            for strs in zip(*self._get_row_node_strs(i, row)):
                yield ''.join(strs)

    def _get_row_node_strs(self, i, row):
        for j, node in enumerate(row):
            indices = i, j
            neighbors = self._get_neighbors(indices)
            self._check_neighbors(self._display_grid[indices], neighbors)
            yield node.strs(neighbors)

    @staticmethod
    def _check_neighbors(node, neighbors: dict[Dirs, Node]):
        def check_neighbor(neighbor_dir: Dirs) -> bool:
            return (
                (node.dirs & neighbor_dir or not neighbors[neighbor_dir].dirs & neighbor_dir.opposite())
                and (not node.dirs & neighbor_dir or neighbors[neighbor_dir].dirs & neighbor_dir.opposite())
            )

        if node._is_virtual:
            return

        for dir_ in Dirs.seq():
            if not check_neighbor(dir_):
                raise Exception("Incompatible neighboring nodes.")

    @property
    def _display_grid(self) -> Grid[Grid[Node]]:
        display_grid = self._grid + [[Node.virtual(Dirs.UP) for _ in range(self._shape[1])]]
        display_grid = Grid([row + [Node.virtual(Dirs.LEFT)] for row in display_grid])
        display_grid[self._shape].dirs |= Dirs.ALL
        return display_grid

    @cache
    def _get_neighbors(self, indices: Sequence[int, int]) -> dict[Dirs, Node]:
        def get_neighbor(indices_: Pos) -> Node:
            i_, j_ = indices_
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
                return Node.virtual(wall_dirs)

            return self._grid[i_, j_]

        indices = Pos(indices)
        max_i, max_j = self._shape
        return {
            Dirs.LEFT: get_neighbor(indices + Dirs.LEFT),
            Dirs.RIGHT: get_neighbor(indices + Dirs.RIGHT),
            Dirs.UP: get_neighbor(indices + Dirs.UP),
            Dirs.DOWN: get_neighbor(indices + Dirs.DOWN),
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
        return f'{self.__class__.__name__}({self._grid})'


example_laby = Laby.from_letters(
    'r, ld, r, lr, ld, d\n'
    'd, ud, rd, lr, lru, lud\n'
    'ud, ud, ud, rd, lr, lu\n'
    'ud, ru, lud, rud, lr, l\n'
    'ur, lr, lu, ur, lr, l'
)
example_laby.start = (0, 0)
example_laby.finish = (4, 5)
