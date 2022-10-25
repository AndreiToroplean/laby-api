from __future__ import annotations

from collections.abc import Iterable
from functools import cache, cached_property

from laby.dirs import Dirs, Pos


class Route:
    def __init__(self, pos: Pos):
        self.pos: Pos = pos
        """Current position."""
        self.dirs: list[Dirs] = []
        """The directions taken from there."""
        self.old_dirs: list[Dirs] = []
        """The directions taken from there that we have backtracked from."""
        self.prev: Route | None = None
        """The route that took us there."""

    @cache
    def __len__(self) -> int:
        return len(list(iter(self)))

    @cached_property
    def all_poss(self) -> set[Pos]:
        all_poss = {self.pos}
        if self.prev is None:
            return all_poss

        return all_poss.union(self.prev.all_poss)

    @cached_property
    def start(self) -> Route:
        if self.prev is None:
            return self

        return self.prev.start

    def __str__(self) -> str:
        from laby.laby import Laby

        rows, cols = zip(*self.all_poss)
        shape = (max(rows)+1, max(cols)+1)
        laby = Laby.ones(shape)
        laby.write(self, do_walls=False)
        return str(laby)

    def __iter__(self) -> Iterable[Route]:
        route = self
        while route is not None:
            yield route
            route = route.prev

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.pos}, {self.dirs})'


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
        self.head.dirs.append(next_dir)

        self.head = next_head
        self.head.prev = current_head

    def backtrack(self, *, update_info=False):
        self.head = self.head.prev
        if update_info:
            self.head.old_dirs.append(self.head.dirs.pop())

    def get_dirs_choices(self, initial_dirs_choices: Dirs) -> Dirs:
        dirs_choices = initial_dirs_choices
        for already_chosen_dir in self.head.dirs + self.head.old_dirs:
            dirs_choices &= ~already_chosen_dir
        for dir_ in dirs_choices:
            if self.head.pos + dir_ in self.all_poss:
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
