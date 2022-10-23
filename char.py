from __future__ import annotations

from collections.abc import Callable

from dirs import Dirs


_H_LEN = 4


class _CharVariants(str):
    def __new__(cls, value: str, bold: str = None):
        instance = super().__new__(cls, value)
        instance._bold = bold
        return instance

    @property
    def bold(self) -> str:
        if self._bold is not None:
            return self._bold

        return self

    def transform(self, transformation: Callable[[str], str]) -> _CharVariants:
        return self.__class__(
            transformation(self),
            transformation(self._bold),
        )


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
