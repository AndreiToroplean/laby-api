from __future__ import annotations

from dirs import Dirs


class Char:
    _H_LEN = 4

    START = '←┼→'
    FINISH = '→┼←'

    H_SPACE = ' ' * _H_LEN
    H_WALL = '─' * _H_LEN
    V_SPACE = ' '
    V_WALL = '│'

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
