from __future__ import annotations

from collections.abc import Iterable
from functools import cache, cached_property

from laby.dirs import Dirs, Pos


class Route:
    """Represents a route through a laby. Each instance is a route point, connected to the previous
    one, they form the whole route.
    """
    def __init__(self, pos: Pos):
        self.pos: Pos = pos
        """Current position."""
        self.ahead_poss = set()
        """Visited positions from there, that we have backtracked from."""
        self.dir: Dirs = Dirs.NONE
        """The directions taken from there."""
        self.old_dirs: Dirs = Dirs.NONE
        """The directions taken from there that we have backtracked from."""
        self.prev: Route | None = None
        """The route that took us there."""

    def copy(self):
        """Create a copy of this route point, still connected to the same previous point."""
        new_route = self.__class__(self.pos)
        new_route.ahead_poss = self.ahead_poss.copy()
        new_route.dir = self.dir
        new_route.old_dirs = self.old_dirs
        new_route.prev = self.prev
        return new_route

    @cache
    def __len__(self) -> int:
        """The number of points in the whole route."""
        return len(list(iter(self)))

    @cached_property
    def start(self) -> Route:
        """The start point of this route."""
        if self.prev is None:
            return self

        return self.prev.start

    def __str__(self) -> str:
        """Get the visual str of this route as applied to a laby.

        This is mainly for debugging.
        """
        laby = self.write_on_laby()
        return str(laby)

    def write_on_laby(self, laby: 'Laby' = None) -> 'Laby':
        """Write this route on the given laby (or a new one if none is given) and return it."""
        if laby is None:
            from laby.laby import Laby
            laby = Laby.ones(self.shape)
        laby.write(self, do_walls=False)
        return laby

    @cached_property
    def shape(self) -> Pos:
        """Shape of this route, meaning the dimensions of the smallest laby able to contain all its positions."""
        if not self.all_poss:
            return Pos((0, 0))
        rows, cols = zip(*self.all_poss)
        return Pos((max(rows) + 1, max(cols) + 1))

    def __iter__(self) -> Iterable[Route]:
        """Iterate through all the points in this route, starting by this one (a.k.a. the end)."""
        route = self
        while route is not None:
            yield route
            route = route.prev

    def __repr__(self) -> str:
        """Small representation of the main attributes of this route point."""
        return f'{self.__class__.__name__}({self.pos}, {self.dir})'

    @cached_property
    def all_poss(self) -> set[Pos]:
        """All positions visited by this route until this point."""
        all_poss = {self.pos}
        if self.prev is None:
            return all_poss

        return all_poss.union(self.prev.all_poss)


class Router:
    """Manager of routes. Able to advance and backtrack a head route, give the directions in which
    it can go next, and branch it into a new head. Can represent all the possible routes in a laby.
    """
    def __init__(self, pos: Pos):
        route = Route(pos)
        self._routes: list[Route] = [route]

    def branch_routes(self):
        """Create a new head by copying this head's previous point."""
        self._routes.append(self.head.prev.copy())
        self.head.ahead_poss.clear()

    def __iter__(self) -> Iterable[Route]:
        """Iterate through all the routes in this router."""
        return self._routes.__iter__()

    def advance(self, dir_: Dirs):
        """Advance the head route in the given direction."""
        current_head = self.head
        next_head = Route(current_head.pos + dir_)
        self.head.dir = dir_

        self.head = next_head
        self.head.prev = current_head

    def backtrack(self, *, recreate: bool):
        """Backtrack head.

        :param recreate: Re-instantiate the point we get to, and forget where we came from.
        """
        current_head = self.head
        prev_head = current_head.prev
        if recreate:
            prev_head = prev_head.copy()
            prev_head.ahead_poss.clear()
        self.head = prev_head
        self.head.ahead_poss.update(current_head.ahead_poss.union((current_head.pos, )))
        self.head.old_dirs |= self.head.dir
        self.head.dir = Dirs.NONE

    def get_dirs_choices(self, initial_dirs_choices: Dirs) -> Dirs:
        """Get the choices we have for new directions to advance to.

        :param initial_dirs_choices: The direction choices dictated by the environment, to filter from.
        """
        dirs_choices = initial_dirs_choices
        dirs_choices &= ~(self.head.dir | self.head.old_dirs)
        for dir_ in dirs_choices:
            next_potential_pos = self.head.pos + dir_
            if next_potential_pos in self.all_poss or next_potential_pos in self.head.ahead_poss:
                dirs_choices &= ~dir_
        return dirs_choices

    @property
    def head(self) -> Route:
        """The head route, the one being presently manipulated."""
        return self._routes[-1]

    @head.setter
    def head(self, route: Route):
        """The head route, the one being presently manipulated."""
        self._routes[-1] = route

    @property
    def is_head_main(self) -> bool:
        """Whether the current head route is the main (or first) route."""
        return self.head is self._routes[0]

    def __str__(self) -> str:
        """Get the visual str of all the routes in this router as applied to a laby.

        This is mainly for debugging.
        """
        from laby.laby import Laby
        laby = Laby.ones(self.shape)
        for route in self._routes:
            laby = route.write_on_laby(laby)
        return str(laby)

    @property
    def shape(self) -> Pos:
        """Shape of this router, meaning the dimensions of the smallest laby able to contain all its routes."""
        route_shapes = [route.shape for route in self._routes]
        rows, cols = zip(*route_shapes)
        return Pos((max(rows), max(cols)))

    def __len__(self) -> int:
        """The total number of points in all the routes of this router.

        Warning: Some points may be counted more than once.
        """
        len_ = 0
        for route in self._routes:
            len_ += len(route)
        return len_

    @property
    def all_poss(self) -> set[Pos]:
        """All positions visited by all this router's routes until this point."""
        all_poss = set()
        for route in self._routes:
            all_poss = all_poss.union(route.all_poss)
        return all_poss
