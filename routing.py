from functools import cache, cached_property


class Route:
    def __init__(self, pos):
        self.pos = pos
        self.next = []
        self.next_dirs = []
        self.prev = None

    @cache
    def __len__(self):
        return len(list(iter(self)))

    @cached_property
    def all_poss(self):
        all_poss = {self.pos}
        if self.prev is None:
            return all_poss

        return all_poss.union(self.prev.all_poss)

    @cached_property
    def start(self):
        if self.prev is None:
            return self

        return self.prev.start

    def __str__(self):
        from laby import Laby

        rows, cols = zip(*self.all_poss)
        shape = (max(rows)+1, max(cols)+1)
        laby = Laby.ones(shape)
        laby.write_route(self)
        return str(laby)

    def __iter__(self):
        route = self
        while route is not None:
            yield route
            route = route.prev

    def __repr__(self):
        return f'{self.__class__.__name__}({self.pos}, {self.next_dirs})'


class MultiRoute(Route):
    def __init__(self, pos):
        route = Route(pos)
        self._routes = [route]

    def add_route(self, route):
        self._routes.append(route)

    def __iter__(self):
        return self._routes.__iter__()

    @property
    def pos(self):
        return self.head.pos

    @pos.setter
    def pos(self, pos):
        self.head.pos = pos

    @property
    def next(self):
        return self.head.next

    @next.setter
    def next(self, next_):
        self.head.next = next_

    @property
    def next_dirs(self):
        return self.head.next_dirs

    @next_dirs.setter
    def next_dirs(self, next_dirs):
        self.head.next_dirs = next_dirs

    @property
    def prev(self):
        return self.head.prev

    @prev.setter
    def prev(self, prev):
        self.head.prev = prev

    @property
    def head(self):
        return self._routes[-1]

    @head.setter
    def head(self, route):
        self._routes[-1] = route

    def __len__(self):
        len_ = 0
        for route in self._routes:
            len_ += len(route)
        return len_

    @property
    def all_poss(self):
        all_poss = set()
        for route in self._routes:
            all_poss = all_poss.union(route.all_poss)
        return all_poss


class Router:
    def __init__(self, pos):
        self.multi_route = MultiRoute(pos)

    @property
    def pos(self):
        return self.multi_route.head.pos

    def backtrack(self):
        self.multi_route.head = self.multi_route.head.prev

    def advance(self, next_dir):
        current_route = self.multi_route.head
        next_route = Route(current_route.pos + next_dir)
        self.multi_route.head.next.append(next_route)
        self.multi_route.head.next_dirs.append(next_dir)

        self.multi_route.head = next_route
        self.multi_route.head.prev = current_route

    def get_dirs_choices(self, initial_dirs_choices):
        dirs_choices = initial_dirs_choices.copy()
        for old_next_dir in self.multi_route.head.next_dirs:
            dirs_choices &= ~old_next_dir
        for dir_ in dirs_choices.copy():
            if self.pos + dir_ in self.multi_route.all_poss:
                dirs_choices &= ~dir_
        return dirs_choices

    def add_route(self):
        self.multi_route.add_route(self.multi_route.head.prev)
