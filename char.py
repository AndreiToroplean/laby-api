from __future__ import annotations

from collections.abc import Callable

from dirs import Dirs


_H_LEN = 5


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
    START = _CharVariants('←┼→')
    FINISH = _CharVariants('→┼←')

    ARROW = {
        Dirs.LEFT: '←',
        Dirs.RIGHT: '→',
        Dirs.UP: '↑',
        Dirs.DOWN: '↓',
    }

    CORNER = {
        Dirs.NONE: _CharVariants(' ', ' '),
        Dirs.LEFT: _CharVariants('╴', '╸'),
        Dirs.RIGHT: _CharVariants('╶', '╺'),
        Dirs.UP: _CharVariants('╵', '╹'),
        Dirs.DOWN: _CharVariants('╷', '╻'),
        Dirs.LEFT | Dirs.RIGHT: _CharVariants('─', '━'),
        Dirs.UP | Dirs.DOWN: _CharVariants('│', '┃'),
        Dirs.RIGHT | Dirs.DOWN: _CharVariants('┌', '┏'),
        Dirs.LEFT | Dirs.DOWN: _CharVariants('┐', '┓'),
        Dirs.RIGHT | Dirs.UP: _CharVariants('└', '┗'),
        Dirs.LEFT | Dirs.UP: _CharVariants('┘', '┛'),
        Dirs.LEFT | Dirs.RIGHT | Dirs.UP: _CharVariants('┴', '┻'),
        Dirs.LEFT | Dirs.RIGHT | Dirs.DOWN: _CharVariants('┬', '┳'),
        Dirs.RIGHT | Dirs.UP | Dirs.DOWN: _CharVariants('├', '┣'),
        Dirs.LEFT | Dirs.UP | Dirs.DOWN: _CharVariants('┤', '┫'),
        Dirs.LEFT | Dirs.RIGHT | Dirs.UP | Dirs.DOWN: _CharVariants('┼', '╋'),
    }

    H_SPACE = CORNER[Dirs.NONE].transform(lambda s: s * _H_LEN)
    H_WALL = CORNER[Dirs.H].transform(lambda s: s * _H_LEN)
    V_SPACE = CORNER[Dirs.NONE]
    V_WALL = CORNER[Dirs.V]
