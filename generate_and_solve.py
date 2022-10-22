from laby import Laby
from routing import Router


def generate(shape):
    laby = generate_empty(shape)
    router = Router(pos=laby.start)
    while True:
        try:
            router = _find_route(laby, router)
        except RouteNotFoundError:
            break

        router.add_route()

    _mark_route(laby, router)

    return laby


def generate_empty(shape):
    laby = Laby.ones(shape)
    laby.start = (0, 0)
    laby.finish = (index - 1 for index in shape)
    return laby


def solve(laby):
    router = _find_route(laby)
    _mark_route(laby, router)


def _find_route(laby: Laby, router: Router = None) -> Router:
    if router is None:
        router = Router(pos=laby.start)

    while router.pos != laby.finish:
        initial_dirs_choices = laby[router.pos].dirs
        dirs_choices = router.get_dirs_choices(initial_dirs_choices)
        if not dirs_choices:
            if router.pos == laby.start:
                raise RouteNotFoundError('No route could be found.')

            router.backtrack()
            continue

        next_dir = dirs_choices.choice()
        router.advance(next_dir)

    return router


class RouteNotFoundError(Exception):
    pass


def _mark_route(laby, router):
    for route in router.multi_route:
        laby.write_route(route)
