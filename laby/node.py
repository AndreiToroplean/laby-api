from __future__ import annotations

from collections.abc import Sequence, Iterable

from laby.char import Char
from laby.dirs import Dirs


class Node:
    """Represents a node in a laby, with its allowed directions, its route directions, and its label."""
    @classmethod
    def zero(cls, *args, **kwargs):
        """Get a zero-node, i.e. one that is completely closed up."""
        return cls(Dirs.NONE, *args, **kwargs)

    @classmethod
    def one(cls, *args, **kwargs):
        """Get a one-node, i.e. one that is completely open."""
        return cls(Dirs.ALL, *args, **kwargs)

    @classmethod
    def virtual(cls, wall_dirs, *args, **kwargs):
        """Get a virtual node, intended for display only.

        :param wall_dirs: Directions in which there is a wall.
        """
        node = cls(~wall_dirs, *args, **kwargs)
        node._is_virtual = True
        return node

    def __init__(self, dirs: Dirs):
        self.dirs = dirs
        """The allowed directions from this node."""
        self.route_dirs = Dirs.NONE
        """The directions in which a route is traced."""
        self.label = ''
        """A label for a special node, representing for instance the start or finish of the laby."""
        self._is_virtual = False
        """Whether this is a virtual node, i.e. only intended for display."""

    def __str__(self) -> str:
        """Get the str visually representing this node."""
        return '\n'.join(self.strs())

    def strs(self, neighbors: dict[Dirs, Node] | None = None) -> Iterable[str]:
        """Get the strs visually representing this node, one per visual row.

        :param neighbors: Neighboring nodes, indexed by direction. If not given, the representation
        returned will be more basic.
        """
        if neighbors is None:
            return self._basic_strs()

        return (''.join(strs[:-1]) for strs in self._strs_seqs(neighbors)[:-1])

    def _strs_seqs(self, neighbors: dict[Dirs, Node]) -> Sequence[Sequence[str]]:
        """Get the sequences of strs visually representing this node, one sequence per visual row.

        :param neighbors: Neighboring nodes, indexed by direction.
        """
        bias = 0.1

        def embedded(orig: str, label: str = None) -> str:
            """Get the original str with the label embedded inside it, centered.

            :param orig: Original string.
            :param label: String to embed.
            """
            if len(label) > len(orig):
                raise Exception("Can't embed label in shorter string.")

            pos = round(len(orig) / 2 - len(label) / 2 - bias)
            return f'{orig[:pos]}{label}{orig[pos+len(label):]}'

        def get_corner_char(corner_dir: Dirs) -> str:
            """Get the char (or chars) representing the requested corner.

            :param corner_dir: The direction of the corner requested.
            """
            h_dir = corner_dir & Dirs.H
            v_dir = corner_dir & Dirs.V

            # Assert good use of this function.
            assert not corner_dir & Dirs.LEFT or not corner_dir & Dirs.RIGHT
            assert not corner_dir & Dirs.UP or not corner_dir & Dirs.DOWN
            assert h_dir and v_dir

            char = Char.CORNER[
                (Dirs.NONE if neighbors[h_dir].dirs & v_dir else h_dir)
                | (Dirs.NONE if neighbors[v_dir].dirs & v_dir.opposite() else h_dir.opposite())
                | (Dirs.NONE if neighbors[v_dir].dirs & h_dir else v_dir)
                | (Dirs.NONE if neighbors[h_dir].dirs & h_dir.opposite() else v_dir.opposite())
            ].bold
            return char

        def get_edge_char(edge_dir: Dirs) -> str:
            """Get the char (or chars) representing the requested edge.

            :param edge_dir: The direction of the edge requested.
            """
            is_empty = self.dirs & edge_dir
            is_h = Dirs.H & edge_dir
            if not is_empty:
                char = (Char.V_WALL if is_h else Char.H_WALL).bold
                return char

            char = Char.V_SPACE if is_h else Char.H_SPACE

            edge_route_dirs = Dirs.NONE
            neighbor_route_dirs = neighbors[edge_dir].route_dirs
            if self.route_dirs & edge_dir or neighbor_route_dirs & edge_dir.opposite():
                edge_route_dirs |= edge_dir | edge_dir.opposite()
            if edge_route_dirs == Dirs.H or edge_route_dirs == Dirs.V:
                arrow_dir = edge_dir if self.route_dirs & edge_dir else edge_dir.opposite()
                label = Char.ARROW[arrow_dir]
            else:
                label = Char.CORNER[edge_route_dirs]
            return embedded(char, label)

        def get_center_char() -> str:
            """Get the char (or chars) representing the center."""
            center_dirs = self.route_dirs
            for dir_ in Dirs.seq():
                if neighbors[dir_].route_dirs & dir_.opposite():
                    center_dirs |= dir_

            label = self.label if self.label else Char.CORNER[center_dirs]

            char_left = Char.H_WALL if center_dirs & Dirs.LEFT else Char.H_SPACE
            char_right = Char.H_WALL if center_dirs & Dirs.RIGHT else Char.H_SPACE
            pos = round(len(Char.H_SPACE)/2 - bias)
            char = f'{char_left[:pos]}{char_right[pos:]}'

            return embedded(char, label)

        strs_seqs = [
            [
                get_corner_char(Dirs.LEFT | Dirs.UP),
                get_edge_char(Dirs.UP),
                get_corner_char(Dirs.RIGHT | Dirs.UP),
            ],
            [
                get_edge_char(Dirs.LEFT),
                get_center_char(),
                get_edge_char(Dirs.RIGHT),
            ],
            [
                get_corner_char(Dirs.LEFT | Dirs.DOWN),
                get_edge_char(Dirs.DOWN),
                get_corner_char(Dirs.RIGHT | Dirs.DOWN),
            ],
        ]
        return strs_seqs

    def _basic_strs(self) -> Iterable[str]:
        """Get a basic visual representation of the node (mostly for debugging)."""
        yield f'{Char.CORNER[Dirs.ALL]}{Char.H_SPACE if Dirs.UP in self.dirs else Char.H_WALL}'
        yield f'{Char.V_SPACE if Dirs.LEFT in self.dirs else Char.V_WALL}{Char.H_SPACE}'

    def __repr__(self):
        """Get an abstract representation of the Node for debugging."""
        return f'{self.__class__.__name__}({self.dirs})'

    def check_neighbors(self, neighbors: dict[Dirs, Node]):
        """Check that the directions for neighboring nodes make sense, that they are symmetrical for each pair.

        :param neighbors: Neighboring nodes, indexed by direction.
        """
        def check_neighbor(neighbor_dir: Dirs) -> bool:
            """Check the allowed directions of this node compared to the neighbor at the requested direction.

            :param neighbor_dir: The direction of the neighbor to check.
            """
            return (
                (self.dirs & neighbor_dir or not neighbors[neighbor_dir].dirs & neighbor_dir.opposite())
                and (not self.dirs & neighbor_dir or neighbors[neighbor_dir].dirs & neighbor_dir.opposite())
            )

        if self._is_virtual:
            return

        for dir_ in Dirs.seq():
            if not check_neighbor(dir_):
                raise Exception("Incompatible neighboring nodes.")
