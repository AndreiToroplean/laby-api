from collections.abc import Sequence

from laby import Laby
from routing import Router, Route


def generate(shape: Sequence[int]) -> Laby:
    laby = generate_empty(shape)
    router = Router(pos=laby.start)
    while True:
        try:
            router = _find_route(laby, router)
        except RouteNotFoundError:
            break

        laby.write_route(router.route)
        router.branch_routes()

    return laby


def generate_empty(shape: Sequence[int]) -> Laby:
    laby = Laby.ones(shape)
    laby.start = (0, 0)
    laby.finish = (index - 1 for index in shape)
    return laby


def solve(laby: Laby) -> Route:
    router = _find_route(laby)
    return router.route


def _find_route(laby: Laby, router: Router = None) -> Router:
    if router is None:
        router = Router(pos=laby.start)

    has_advanced = False
    while router.pos != laby.finish:
        initial_dirs_choices = laby[router.pos].dirs
        dirs_choices = router.get_dirs_choices(initial_dirs_choices)
        if not dirs_choices:
            if router.pos == laby.start:
                raise RouteNotFoundError('No route could be found.')

            if not router.is_on_main and has_advanced:
                return router

            router.backtrack()
            continue

        has_advanced = True
        next_dir = dirs_choices.choice()
        router.advance(next_dir)

    return router


class RouteNotFoundError(Exception):
    pass
