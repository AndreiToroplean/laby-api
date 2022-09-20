import enum
import functools


class Laby:
    def __init__(self, size=None):
        size = size or [2, 2]
        n_rows, n_cols = size
        self.data = [[Node() for _ in range(n_cols)] for _ in range(n_rows)]

    def __str__(self):
        # TODO: improve var names.
        lines = []
        for row_nodes in self.data:
            for row_nodes_lines in zip(*[node.strs for node in row_nodes]):
                lines_ = [''.join(cell_ls) for cell_ls in row_nodes_lines]
                lines.append(''.join(lines_))
        return '\n'.join(lines)


class Node:
    def __init__(self, dirs=None):
        dirs = dirs or [
            # Dir.LEFT,
            # Dir.RIGHT,
            # Dir.UP,
            # Dir.DOWN,
        ]
        self.dirs = dirs

    @property
    @functools.cache
    def strs(self):
        strs = [[
                Chars.LRUD_CORNER,
                Chars.EMPTY if Dir.UP in self.dirs else Chars.H_WALL,
            ],
            [
                Chars.EMPTY if Dir.LEFT in self.dirs else Chars.V_WALL,
                Chars.EMPTY,
            ],
        ]
        return strs


class Dir(enum.Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, 1)
    DOWN = (0, -1)


class Chars:
    # ┌────┬────┐
    # │    │    │
    # ├────┼────┤
    # │    │    │
    # └────┴────┘

    H_SIZE = 4

    EMPTY = ' ' * H_SIZE
    H_WALL = '─' * H_SIZE
    V_WALL = '│'
    RD_CORNER = '┌'
    LD_CORNER = '┐'
    RU_CORNER = '└'
    LU_CORNER = '┘'
    LRU_CORNER = '┴'
    LRD_CORNER = '┬'
    RUD_CORNER = '├'
    LUD_CORNER = '┤'
    LRUD_CORNER = '┼'
