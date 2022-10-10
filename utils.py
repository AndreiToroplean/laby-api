import enum
from collections.abc import Sequence


class Dirs(enum.Flag):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()

    H = LEFT | RIGHT
    V = UP | DOWN

    ALL = H | V
    NONE = 0

    @classmethod
    def from_letters(cls, letters: str):
        dirs = cls.NONE
        for letter in letters:
            try:
                dirs |= _LETTERS_TO_DIRS[letter]
            except KeyError:
                raise Exception(f'Wrong letter for {cls.__name__}: {letter !r}. '
                                f'Possible choices are: {list(_LETTERS_TO_DIRS.keys())}.') from None
        return dirs

    @classmethod
    def seq(cls):
        return cls.LEFT, cls.RIGHT, cls.UP, cls.DOWN

    def opposite(self):
        try:
            return _DIR_OPPOSITES[self]
        except KeyError:
            raise Exception(f"Arbitrary {self.__class__.__name__} compositions don't have opposites.") from None

    def delta(self):
        try:
            return _DIR_DELTAS[self]
        except KeyError:
            raise Exception(f'Cannot get delta for an arbitrary {self.__class__.__name__} composition.') from None


class SymmetricDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update({v: k for k, v in self.items()})


_DIR_OPPOSITES = SymmetricDict({
    Dirs.LEFT: Dirs.RIGHT,
    Dirs.UP: Dirs.DOWN,
})

_DIR_DELTAS = {
    Dirs.LEFT: (0, -1),
    Dirs.RIGHT: (0, 1),
    Dirs.UP: (-1, 0),
    Dirs.DOWN: (1, 0),
}

_LETTERS_TO_DIRS = {
    'l': Dirs.LEFT,
    'r': Dirs.RIGHT,
    'u': Dirs.UP,
    'd': Dirs.DOWN,
}


class Char:
    _H_LEN = 4

    H_SPACE = ' ' * _H_LEN
    H_WALL = '─' * _H_LEN
    V_SPACE = ' '
    V_WALL = '│'

    NONE_CORNER = ' '
    L_CORNER = '╴'
    R_CORNER = '╶'
    U_CORNER = '╵'
    D_CORNER = '╷'
    LR_CORNER = '─'
    UD_CORNER = '│'
    RD_CORNER = '┌'
    LD_CORNER = '┐'
    RU_CORNER = '└'
    LU_CORNER = '┘'
    LRU_CORNER = '┴'
    LRD_CORNER = '┬'
    RUD_CORNER = '├'
    LUD_CORNER = '┤'
    LRUD_CORNER = '┼'

    CORNER = {
        Dirs.NONE: NONE_CORNER,
        Dirs.LEFT: L_CORNER,
        Dirs.RIGHT: R_CORNER,
        Dirs.UP: U_CORNER,
        Dirs.DOWN: D_CORNER,
        Dirs.LEFT | Dirs.RIGHT: LR_CORNER,
        Dirs.UP | Dirs.DOWN: UD_CORNER,
        Dirs.RIGHT | Dirs.DOWN: RD_CORNER,
        Dirs.LEFT | Dirs.DOWN: LD_CORNER,
        Dirs.RIGHT | Dirs.UP: RU_CORNER,
        Dirs.LEFT | Dirs.UP: LU_CORNER,
        Dirs.LEFT | Dirs.RIGHT | Dirs.UP: LRU_CORNER,
        Dirs.LEFT | Dirs.RIGHT | Dirs.DOWN: LRD_CORNER,
        Dirs.RIGHT | Dirs.UP | Dirs.DOWN: RUD_CORNER,
        Dirs.LEFT | Dirs.UP | Dirs.DOWN: LUD_CORNER,
        Dirs.LEFT | Dirs.RIGHT | Dirs.UP | Dirs.DOWN: LRUD_CORNER,
    }


# Types
SetIndices = Sequence[int, ...] | int
GetIndices = Sequence[int | slice, ...] | int | slice
