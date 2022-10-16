from functools import cache, cached_property


class Route:
    def __init__(self, pos):
        self.pos = pos
        self.next = []
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
