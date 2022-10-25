from __future__ import annotations

from collections.abc import Sequence

from laby.dirs import Dirs
from laby.laby import Laby
from laby.router import Router, Route


def main():
    laby = generate((12, 16))
    print(laby)
    print()

    route = solve(laby)
    laby.write(route, do_walls=False)
    print(laby)


def generate(shape: Sequence[int]) -> Laby:
    laby = generate_empty(shape)
    router = Router(pos=laby.start)
    while True:
        try:
            router = _find_route(laby, router)
        except RouteNotFoundError:
            break

        router.add_route(router.head.prev)

    laby.write_all_nodes(Dirs.NONE)
    for route in router:
        laby.write(route)

    return laby


def generate_empty(shape: Sequence[int]) -> Laby:
    laby = Laby.ones(shape)
    laby.start = (0, 0)
    laby.finish = (index - 1 for index in shape)
    return laby


def solve(laby: Laby) -> Route:
    router = _find_route(laby)
    return router.head


def _find_route(laby: Laby, router: Router = None) -> Router:
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

            router.backtrack(update_info=has_advanced)
            continue

        has_advanced = True
        next_dir = dirs_choices.choice()
        router.advance(next_dir)

    return router


class RouteNotFoundError(Exception):
    pass


if __name__ == '__main__':
    main()