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
        self.routes = [route]

    @property
    def pos(self):
        return self.route.pos

    @pos.setter
    def pos(self, pos):
        self.route.pos = pos

    @property
    def next(self):
        return self.route.next

    @next.setter
    def next(self, next_):
        self.route.next = next_

    @property
    def next_dirs(self):
        return self.route.next_dirs

    @next_dirs.setter
    def next_dirs(self, next_dirs):
        self.route.next_dirs = next_dirs

    @property
    def prev(self):
        return self.route.prev

    @prev.setter
    def prev(self, prev):
        self.route.prev = prev

    @property
    def route(self):
        return self.routes[-1]

    def __len__(self):
        len_ = 0
        for route in self.routes:
            len_ += len(route)
        return len_

    @property
    def all_poss(self):
        all_poss = set()
        for route in self.routes:
            all_poss = all_poss.union(route.all_poss)
        return all_poss
