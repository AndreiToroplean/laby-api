from functools import cache


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
