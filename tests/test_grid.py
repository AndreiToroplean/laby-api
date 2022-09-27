import pytest

from grid import Grid


class TestGrid:
    @pytest.fixture
    def grid(self):
        return Grid([[0, 1], [2, 3]])

    def test_sub_value_type(self, grid):
        assert isinstance(grid[0], Grid)

    def test_get_item_unique(self, grid):
        assert grid[0, 0] == 0
        assert grid[0, 1] == 1
        assert grid[1, 0] == 2
        assert grid[1, 1] == 3

    def test_get_item_sub_grid(self, grid):
        assert grid[0] == [0, 1]
        assert grid[1] == [2, 3]

    def test_get_item_negative(self, grid):
        assert grid[-1] == [2, 3]

    def test_get_item_slice(self, grid):
        assert grid[:1] == [[0, 1]]

    def test_get_item_slice_type(self, grid):
        assert isinstance(grid[:1], Grid)

    def test_get_item_slice_tuple(self, grid):
        assert grid[0, :1] == [0]

    def test_get_item_raises_index_error(self, grid):
        with pytest.raises(IndexError):
            grid[0, 2]

    def test_set_item_unique(self, grid):
        grid[1, 1] = 30
        assert grid == [[0, 1], [2, 30]]

    def test_set_item_list(self, grid):
        grid[1] = [20, 30]
        assert grid == [[0, 1], [20, 30]]

    def test_set_item_list_type(self, grid):
        grid[1] = [20, 30]
        assert isinstance(grid[1], Grid)
