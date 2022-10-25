from __future__ import annotations

from collections.abc import Sequence, Iterable
import enum
import random


class Dirs(enum.Flag):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()

    NONE = 0
    ALL = LEFT | RIGHT | UP | DOWN

    @classmethod
    def from_letters(cls, letters: str) -> Dirs:
        dirs = cls.NONE
        for letter in letters:
            try:
                dirs |= _LETTERS_TO_DIRS[letter]
            except KeyError:
                raise DirsError(f'Wrong letter for {cls.__name__}: {letter !r}. '
                                f'Possible choices are: {list(_LETTERS_TO_DIRS.keys())}.') from None
        return dirs

    @classmethod
    def seq(cls) -> Sequence[Dirs, Dirs, Dirs, Dirs]:
        return cls.LEFT, cls.RIGHT, cls.UP, cls.DOWN

    def opposite(self) -> Dirs:
        try:
            return _DIR_OPPOSITES[self]
        except KeyError:
            raise DirsError(f"Arbitrary {self.__class__.__name__} compositions don't have opposites.") from None

    def normal(self) -> Dirs:
        if self | Dirs.H == Dirs.H:
            return Dirs.V

        if self | Dirs.V == Dirs.V:
            return Dirs.H

        raise DirsError(f"{self} doesn't have a normal.")

    def choice(self) -> Dirs:
        members = list(self)
        if not members:
            return Dirs.NONE

        return random.choice(members)

    def delta(self) -> Sequence[int, int]:
        try:
            return _DIR_DELTAS[self]
        except KeyError:
            raise DirsError(f'Cannot get delta for an arbitrary {self.__class__.__name__} composition.') from None

    def __iter__(self) -> Iterable[Dirs]:
        for dir_ in self.seq():
            if not self & dir_:
                continue

            yield dir_


# Additional regular class attributes
Dirs.H = Dirs.LEFT | Dirs.RIGHT
Dirs.V = Dirs.UP | Dirs.DOWN


class DirsError(Exception):
    pass


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


class Pos(tuple):
    def __new__(cls, indices: Sequence[int, int]):
        return ().__new__(cls, indices)

    def __add__(self, dir_: Dirs) -> Pos:
        delta = dir_.delta()
        return self.__class__([self[0] + delta[0], self[1] + delta[1]])

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({super().__repr__()})'