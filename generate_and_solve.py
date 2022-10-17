from laby import Laby
from route import MultiRoute


def generate(shape):
    laby = generate_empty(shape)
    route = None
    while True:
        try:
            route = _find_route(laby, route)
        except RouteNotFoundError:
            break

        route.routes.append(route.prev)

    for sub_route in route.routes:
        _mark_route(laby, sub_route)

    return laby


def generate_empty(shape):
    laby = Laby.ones(shape)
    laby.start = (0, 0)
    laby.finish = (index - 1 for index in shape)
    return laby


def solve(laby):
    route = _find_route(laby)
    _mark_route(laby, route)


def _find_route(laby, route=None):
    route = route if route is not None else MultiRoute(laby.start)
    while route.pos != laby.finish:
        dirs_choices = _get_dirs_choices(laby, route)
        if not dirs_choices:
            if route.pos == laby.start:
                raise RouteNotFoundError('No route could be found.')

            route = route.prev
            continue

        next_dir = dirs_choices.choice()
        next_route = MultiRoute(route.pos + next_dir)
        route.next.append(next_route)
        route.next_dirs.append(next_dir)

        prev_route = route
        route = next_route
        route.prev = prev_route
    return route


class RouteNotFoundError(Exception):
    pass


def _get_dirs_choices(laby, route):
    node = laby[route.pos]
    dirs_choices = node.dirs.copy()
    for old_next_dir in route.next_dirs:
        dirs_choices &= ~old_next_dir
    for dir_ in dirs_choices.copy():
        if route.pos + dir_ in route.all_poss:
            dirs_choices &= ~dir_
    return dirs_choices


def _mark_route(laby, route):
    while True:
        route = route.prev
        if route is route.start:
            break

        laby[route.pos].label = route.next_dirs[-1].arrow()
