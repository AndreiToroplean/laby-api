from collections.abc import Sequence

# Types
SetIndices = Sequence[int, ...] | int
GetIndices = Sequence[int | slice, ...] | int | slice
