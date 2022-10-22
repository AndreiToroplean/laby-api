from collections.abc import Iterable
from functools import cache, cached_property

from dirs import Dirs, Pos


class Route:
    def __init__(self, pos: Pos):
        self.pos = pos
        self.next_dirs = []
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
    def start(self) -> 'Route':
        if self.prev is None:
            return self

        return self.prev.start

    def __str__(self) -> str:
        from laby import Laby

        rows, cols = zip(*self.all_poss)
        shape = (max(rows)+1, max(cols)+1)
        laby = Laby.ones(shape)
        laby.write_route(self)
        return str(laby)

    def __iter__(self) -> Iterable['Route']:
        route = self
        while route is not None:
            yield route
            route = route.prev

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.pos}, {self.next_dirs})'


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


class Router:
    def __init__(self, pos: Pos):
        self.multi_route = MultiRoute(pos)

    @property
    def pos(self) -> Pos:
        return self.multi_route.head.pos

    @property
    def route(self) -> Route:
        return self.multi_route.head

    def backtrack(self):
        self.multi_route.head = self.multi_route.head.prev

    def advance(self, next_dir: Dirs):
        current_route = self.multi_route.head
        next_route = Route(current_route.pos + next_dir)
        self.multi_route.head.next_dirs.append(next_dir)

        self.multi_route.head = next_route
        self.multi_route.head.prev = current_route

    @property
    def is_on_main(self) -> bool:
        return self.multi_route.is_head_main

    def get_dirs_choices(self, initial_dirs_choices: Dirs) -> Dirs:
        dirs_choices = initial_dirs_choices.copy()
        for old_next_dir in self.multi_route.head.next_dirs:
            dirs_choices &= ~old_next_dir
        for dir_ in dirs_choices.copy():
            if self.pos + dir_ in self.multi_route.all_poss:
                dirs_choices &= ~dir_
        return dirs_choices

    def branch_routes(self):
        self.multi_route.add_route(self.multi_route.head.prev)
