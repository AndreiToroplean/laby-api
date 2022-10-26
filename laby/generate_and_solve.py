from __future__ import annotations

from collections.abc import Sequence

from laby.dirs import Dirs
from laby.laby import Laby
from laby.router import Router, Route


def main():
    """Generate a random laby, then solve it. Display both the problem and the solution."""
    laby = generate((12, 16))
    print(laby)
    print()

    route = solve(laby)
    laby.write(route, do_walls=False)
    print(laby)


def generate(shape: Sequence[int]) -> Laby:
    """Generate a random laby of the given shape."""
    laby = generate_empty(shape)
    with laby.reversed():
        router = Router(pos=laby.start)
        while True:
            try:
                router = _find_route(laby, router)
            except RouteNotFoundError:
                break

            router.branch_routes()

    laby.write_all_nodes(Dirs.NONE)
    for route in router:
        laby.write(route)

    return laby


def generate_empty(shape: Sequence[int]) -> Laby:
    """Generate an empty laby of the given shape."""
    laby = Laby.ones(shape)
    laby.start = (0, 0)
    laby.finish = (index - 1 for index in shape)
    return laby


def solve(laby: Laby) -> Route:
    """Solve the given laby and return the route."""
    router = _find_route(laby)
    return router.head


def _find_route(laby: Laby, router: Router = None) -> Router:
    """Find a route through the given laby, using the router's current head.

    :param laby: Laby to use as an environment.
    :param router: Router to use. No routes are added or removed, the head is only advanced / backtracked.
    :return: The router containing the found route.
    """
    if router is None:
        router = Router(pos=laby.start)

    has_advanced = False
    while router.head.pos != laby.finish:
        initial_dirs_choices = laby[router.head.pos].dirs
        dirs_choices = router.get_dirs_choices(initial_dirs_choices)
        if not dirs_choices:
            if router.head.pos == laby.start:
                raise RouteNotFoundError('No route could be found.')

            if not router.is_head_main and has_advanced:
                return router

            router.backtrack(recreate=not has_advanced)
            continue

        has_advanced = True
        dir_ = dirs_choices.choice()
        router.advance(dir_)

    return router


class RouteNotFoundError(Exception):
    """Exception raised when the whole environment was explored and no further route could be found."""
    pass


if __name__ == '__main__':
    main()
