from __future__ import annotations

from collections.abc import Iterable
from functools import cache, cached_property

from dirs import Dirs, Pos


class Route:
    def __init__(self, pos: Pos):
        self.pos = pos
        self.dirs = []
        self.old_dirs = []
        self.prev = None

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
        from laby import Laby

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


class MultiRoute:
    def __init__(self, pos: Pos):
        route = Route(pos)
        self._routes = [route]

    def add_route(self, route: Route):
        self._routes.append(route)

    def __iter__(self) -> Iterable[Route]:
        return self._routes.__iter__()

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


class Router(MultiRoute):
    def backtrack(self, *, modify_dirs=False):
        self.head = self.head.prev
        if modify_dirs:
            self.head.old_dirs.append(self.head.dirs.pop())

    def advance(self, next_dir: Dirs):
        current_route = self.head
        next_route = Route(current_route.pos + next_dir)
        self.head.dirs.append(next_dir)

        self.head = next_route
        self.head.prev = current_route

    def get_dirs_choices(self, initial_dirs_choices: Dirs) -> Dirs:
        dirs_choices = initial_dirs_choices
        for already_chosen_dir in self.head.dirs + self.head.old_dirs:
            dirs_choices &= ~already_chosen_dir
        for dir_ in dirs_choices:
            if self.head.pos + dir_ in self.all_poss:
                dirs_choices &= ~dir_
        return dirs_choices

    def branch_routes(self):
        self.add_route(self.head.prev)
