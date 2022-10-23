from __future__ import annotations

from dirs import Dirs


_H_LEN = 4


class Char:
    START = '←┼→'
    FINISH = '→┼←'

    CORNER = {
        Dirs.NONE: ' ',
        Dirs.LEFT: '╴',
        Dirs.RIGHT: '╶',
        Dirs.UP: '╵',
        Dirs.DOWN: '╷',
        Dirs.LEFT | Dirs.RIGHT: '─',
        Dirs.UP | Dirs.DOWN: '│',
        Dirs.RIGHT | Dirs.DOWN: '┌',
        Dirs.LEFT | Dirs.DOWN: '┐',
        Dirs.RIGHT | Dirs.UP: '└',
        Dirs.LEFT | Dirs.UP: '┘',
        Dirs.LEFT | Dirs.RIGHT | Dirs.UP: '┴',
        Dirs.LEFT | Dirs.RIGHT | Dirs.DOWN: '┬',
        Dirs.RIGHT | Dirs.UP | Dirs.DOWN: '├',
        Dirs.LEFT | Dirs.UP | Dirs.DOWN: '┤',
        Dirs.LEFT | Dirs.RIGHT | Dirs.UP | Dirs.DOWN: '┼',
    }

    H_SPACE = CORNER[Dirs.NONE] * _H_LEN
    H_WALL = CORNER[Dirs.H] * _H_LEN
    V_SPACE = CORNER[Dirs.NONE]
    V_WALL = CORNER[Dirs.V]
