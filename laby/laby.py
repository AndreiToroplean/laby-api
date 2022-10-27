from __future__ import annotations

from collections.abc import Sequence, Callable, Iterable
from contextlib import contextmanager
from functools import cache, cached_property
from typing import Any

from laby.char import Char
from laby.grid import Grid
from laby.node import Node
from laby.router import Route
from laby.dirs import Dirs, Pos


class Laby:
    """Represents a labyrinth, composed of discrete cartesian positions called nodes, forming a grid.
    Although primarily designed to be 2D, some parts work for all (strictly positive) dimensions.
    """
    @classmethod
    def zeros(cls, shape: Sequence[int]):
        """Return a laby of the requested shape made out of zero-nodes, i.e. nodes that are entirely closed up."""
        return cls.full(shape, lambda: Node.zero())

    @classmethod
    def ones(cls, shape: Sequence[int]):
        """Return a laby of the requested shape made out of one-nodes, i.e. nodes that are entirely open."""
        return cls.full(shape, lambda: Node.one())

    @classmethod
    def full(cls, shape: Sequence[int], fill_value: Callable[[], Node] | Node | Any):
        """Return a laby of the requested shape made out of nodes like the one given."""
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
        """Return a laby corresponding to the grid given with the allowed direction letters.

        :param letters_grid: String prescribing the laby. Each line represents a row of nodes,
            separated by commas. Each node is prescribed through the letters representing its
            allowed directions, from the first letters of 'left', 'right', 'up' and 'down'.
        """
        grid = Grid([[Node(Dirs.from_letters(letters.strip().lower())) for letters in row_letters.split(',')]
                     for row_letters in letters_grid.splitlines()])
        return cls(grid)

    @classmethod
    def from_dirs(cls, dirs: Sequence[Sequence[Dirs]]):
        """Return a laby corresponding to the grid given with the allowed directions."""
        grid = Grid([[Node(dir_) for dir_ in dirs_row] for dirs_row in dirs])
        return cls(grid)

    def __init__(self, grid: Grid[Grid[Node]]):
        self._grid = grid
        """The grid of nodes."""
        self._start = None
        """The start position in the laby."""
        self._finish = None
        """The finish position in the laby."""

        self._enforce_walls()

    @property
    def start(self) -> Pos:
        """The start position in the laby."""
        return self._start

    @start.setter
    def start(self, indices: Sequence[int, int]):
        """The start position in the laby."""
        self._start = Pos(indices)
        self._grid[self._start].label = Char.START

    @property
    def finish(self) -> Pos:
        """The finish position in the laby."""
        return self._finish

    @finish.setter
    def finish(self, indices: Sequence[int, int]):
        """The finish position in the laby."""
        self._finish = Pos(indices)
        self._grid[self._finish].label = Char.FINISH

    def __getitem__(self, indices: Sequence[int, ...] | int) -> Node:
        """Get a node in the laby from its position.

        Warning: you cannot get a sub-grid through this method.
        """
        node = self._grid[indices]
        if not isinstance(node, Node):
            raise IndexError('Not enough indices to get a specific Node (cannot get sub-grids).')

        return node

    def _enforce_walls(self):
        """Make the outermost nodes into walls, i.e. remove their outward directions."""
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

    def write_all_nodes(self, dirs: Dirs, *, do_walls=True):
        """Write allowed directions or route directions for all nodes.

        :param dirs: The new directions.
        :param do_walls: Whether to write directions (creating walls), or else route directions.
        """
        for row in self._grid:
            for node in row:
                if do_walls:
                    node.dirs = dirs
                else:
                    node.route_dirs = dirs

    def write(self, route: Route, *, do_walls=True):
        """Write allowed directions or route directions from a route object.

        :param route: Route used to prescribe directions.
        :param do_walls: Whether to write directions (creating walls), or else route directions.
        """
        for route_point in route:
            if not route_point.dir:
                continue

            node = self._grid[route_point.pos]
            neighbors = self._get_neighbors(route_point.pos)
            if do_walls:
                node.dirs |= route_point.dir
                neighbors[route_point.dir].dirs |= route_point.dir.opposite()
            else:
                node.route_dirs |= route_point.dir

    @contextmanager
    def reversed(self):
        """Context manager to reverse the start and finish of this laby."""
        self._start, self._finish = self._finish, self._start
        yield
        self._finish, self._start = self._start, self._finish

    def __str__(self) -> str:
        """Get the str visually representing this laby."""
        return '\n'.join(self.strs)

    @property
    def strs(self) -> Iterable[str]:
        """The strs visually representing this laby, one per visual row."""
        for i, row in enumerate(self._display_grid):
            for strs in zip(*self._get_row_node_strs(i, row)):
                yield ''.join(strs)

    def _get_row_node_strs(self, i: int, row: Grid[Node]) -> Iterable[Iterable[str]]:
        """Get the strs visually representing the given row, one iterable per node."""
        for j, node in enumerate(row):
            indices = Pos((i, j))
            neighbors = self._get_neighbors(indices)
            node.check_neighbors(neighbors)
            yield node.strs(neighbors)

    @property
    def _display_grid(self) -> Grid[Grid[Node]]:
        """A display-specific grid of nodes, with additional ones to properly draw exterior walls."""
        display_grid = self._grid + [[Node.virtual(Dirs.UP) for _ in range(self._shape[1])]]
        display_grid = Grid([row + [Node.virtual(Dirs.LEFT)] for row in display_grid])
        display_grid[self._shape].dirs |= Dirs.ALL
        return display_grid

    @cache
    def _get_neighbors(self, indices: Pos) -> dict[Dirs, Node]:
        """Get the neighbors of the node at the given position, indexed by direction."""

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

        max_i, max_j = self._shape
        return {
            Dirs.LEFT: get_neighbor(indices + Dirs.LEFT),
            Dirs.RIGHT: get_neighbor(indices + Dirs.RIGHT),
            Dirs.UP: get_neighbor(indices + Dirs.UP),
            Dirs.DOWN: get_neighbor(indices + Dirs.DOWN),
        }

    @cached_property
    def _shape(self) -> tuple[int, ...]:
        """The shape of the laby, i.e. its dimensions."""
        def get_shape(grid) -> tuple[int, ...]:
            try:
                sub_grid = grid[0]
            except TypeError:
                return ()

            return len(grid), *get_shape(sub_grid)

        return get_shape(self._grid)

    def __repr__(self) -> str:
        """Get a simple, abstract representation of the laby for debugging."""
        return f'{self.__class__.__name__}({self._grid})'
