from functools import cache, cached_property


class Route:
    def __init__(self, pos):
        self.pos = pos
        self.next = []
        self.next_dirs = []
        self.prev = None

    @cache
    def __len__(self):
        len_ = 0
        route = self
        while route is not None:
            route = route.prev
            len_ += 1
        return len_

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


class MultiRoute(Route):
    def __init__(self, pos):
        route = Route(pos)
        self.routes = [route]

    @property
    def pos(self):
        return self.routes[-1].pos

    @pos.setter
    def pos(self, pos):
        self.routes[-1].pos = pos

    @property
    def next(self):
        return self.routes[-1].next

    @next.setter
    def next(self, next_):
        self.routes[-1].next = next_

    @property
    def next_dirs(self):
        return self.routes[-1].next_dirs

    @next_dirs.setter
    def next_dirs(self, next_dirs):
        self.routes[-1].next_dirs = next_dirs

    @property
    def prev(self):
        return self.routes[-1].prev

    @prev.setter
    def prev(self, prev):
        self.routes[-1].prev = prev

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
