from collections import namedtuple

from laby import Laby
from route import Route
from utils import Dirs


def generate_empty(shape):
    laby = Laby.ones(shape)
    laby.start = (0, 0)
    laby.finish = (index - 1 for index in shape)
    return laby


def solve(laby):
    route = _find_route(laby)
    _mark_route(laby, route)


def _find_route(laby):
    route = Route(laby.start)
    while route.pos != laby.finish:
        node = laby[route.pos]
        possible_dirs = node.dirs.copy()
        for prev_next in route.next:
            possible_dirs &= ~prev_next.dir
        possible_unvisited_dirs = Dirs.NONE
        for dir_ in possible_dirs:
            if route.pos + dir_ not in route.all_poss:
                possible_unvisited_dirs |= dir_
        possible_dirs = possible_unvisited_dirs
        if not possible_dirs:
            if route.pos == laby.start:
                raise Exception('No solution!')

            route = route.prev
            continue

        choice = possible_dirs.choice()
        next_route = Route(route.pos + choice)
        route.next.append(_Next(choice, next_route))

        prev_route = route
        route = next_route
        route.prev = prev_route
    return route


def _mark_route(laby, route):
    while True:
        route = route.prev
        if route.pos == laby.start:
            break

        laby[route.pos].label = route.next[-1].dir.arrow()


_Next = namedtuple('Next', ('dir', 'route'))
