from __future__ import annotations

from collections.abc import Iterable
from functools import cache, cached_property

from laby.dirs import Dirs, Pos


class Route:
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
        new_route = self.__class__(self.pos)
        new_route.ahead_poss = self.ahead_poss.copy()
        new_route.dir = self.dir
        new_route.old_dirs = self.old_dirs
        new_route.prev = self.prev
        return new_route

    @cache
    def __len__(self) -> int:
        return len(list(iter(self)))

    @cached_property
    def start(self) -> Route:
        if self.prev is None:
            return self

        return self.prev.start

    def __str__(self) -> str:
        laby = self.write_on_laby()
        return str(laby)

    def write_on_laby(self, laby: 'Laby' = None) -> 'Laby':
        if laby is None:
            from laby.laby import Laby
            laby = Laby.ones(self.shape)
        laby.write(self, do_walls=False)
        return laby

    @cached_property
    def shape(self) -> Pos:
        if not self.all_poss:
            return Pos((0, 0))
        rows, cols = zip(*self.all_poss)
        return Pos((max(rows) + 1, max(cols) + 1))

    def __iter__(self) -> Iterable[Route]:
        route = self
        while route is not None:
            yield route
            route = route.prev

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.pos}, {self.dir})'

    @cached_property
    def all_poss(self) -> set[Pos]:
        all_poss = {self.pos}
        if self.prev is None:
            return all_poss

        return all_poss.union(self.prev.all_poss)


class Router:
    def __init__(self, pos: Pos):
        route = Route(pos)
        self._routes: list[Route] = [route]

    def add_route(self, route: Route):
        self._routes.append(route)

    def __iter__(self) -> Iterable[Route]:
        return self._routes.__iter__()

    def advance(self, next_dir: Dirs):
        current_head = self.head
        next_head = Route(current_head.pos + next_dir)
        self.head.dir = next_dir

        self.head = next_head
        self.head.prev = current_head

    def backtrack(self, *, recreate: bool):
        current_head = self.head
        prev_head = current_head.prev
        if recreate:
            prev_head = prev_head.copy()
        self.head = prev_head
        self.head.ahead_poss.update(current_head.ahead_poss.union((current_head.pos, )))
        self.head.old_dirs |= self.head.dir
        self.head.dir = Dirs.NONE

    def get_dirs_choices(self, initial_dirs_choices: Dirs) -> Dirs:
        dirs_choices = initial_dirs_choices
        dirs_choices &= ~(self.head.dir | self.head.old_dirs)
        for dir_ in dirs_choices:
            next_potential_pos = self.head.pos + dir_
            if next_potential_pos in self.all_poss or next_potential_pos in self.head.ahead_poss:
                dirs_choices &= ~dir_
        return dirs_choices

    @property
    def head(self) -> Route:
        return self._routes[-1]

    @head.setter
    def head(self, route: Route):
        self._routes[-1] = route

    @property
    def is_head_main(self) -> bool:
        return self.head is self._routes[0]

    def __str__(self):
        from laby.laby import Laby
        laby = Laby.ones(self.shape)
        for route in self._routes:
            laby = route.write_on_laby(laby)
        return str(laby)

    @property
    def shape(self):
        route_shapes = [route.shape for route in self._routes]
        rows, cols = zip(*route_shapes)
        return Pos((max(rows), max(cols)))

    def __len__(self) -> int:
        len_ = 0
        for route in self._routes:
            len_ += len(route)
        return len_

    @property
    def all_poss(self) -> set[Pos]:
        all_poss = set()
        for route in self._routes:
            all_poss = all_poss.union(route.all_poss)
        return all_poss
