import enum


class Laby:
    def __init__(self):
        self.size = [2, 2]
        self.data = [[Node() for _ in range(self.size[1])] for _ in range(self.size[0])]

    def __str__(self):
        lines = []
        for data_line in self.data:
            strs = [str(node) for node in data_line]
            line = f"|{'|'.join(strs)}|"
            lines.append(line)
            lines.append('-' * len(line))
        lines.insert(0, lines[-1])
        return '\n'.join(lines)


class Node:
    def __str__(self):
        return '  '


class Dir(enum.Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, 1)
    DOWN = (0, -1)
