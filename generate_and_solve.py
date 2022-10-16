from collections import namedtuple

from laby import Laby
from route import Route


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
        dirs_choices = _get_dirs_choices(laby, route)
        if not dirs_choices:
            if route.pos == laby.start:
                raise Exception('No solution!')

            route = route.prev
            continue

        choice = dirs_choices.choice()
        next_route = Route(route.pos + choice)
        route.next.append(_Next(choice, next_route))

        prev_route = route
        route = next_route
        route.prev = prev_route
    return route


def _get_dirs_choices(laby, route):
    node = laby[route.pos]
    dirs_choices = node.dirs.copy()
    for prev_next in route.next:
        dirs_choices &= ~prev_next.dir
    for dir_ in dirs_choices.copy():
        if route.pos + dir_ in route.all_poss:
            dirs_choices &= ~dir_
    return dirs_choices


def _mark_route(laby, route):
    while True:
        route = route.prev
        if route is route.start:
            break

        laby[route.pos].label = route.next[-1].dir.arrow()


_Next = namedtuple('Next', ('dir', 'route'))
