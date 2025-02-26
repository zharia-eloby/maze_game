import pytest
from app.src.general.maze import Cell

def test_cell_init():
    cell = Cell(2, 5)
    assert cell.row_index == 2
    assert cell.col_index == 5
    assert cell.walls == { "left": True, "right": True, "up": True, "down": True }
    assert cell.visited == False
    assert cell.rect == None

@pytest.mark.parametrize("walls, expected_blocked_walls", [
    pytest.param(
        { "left": True, "right": False, "up": True, "down": False },
        ["left", "up"],
        id="when cell has blocked walls"
    ),
    pytest.param(
        { "left": False, "right": False, "up": False, "down": False },
        [],
        id="when cell does not have blocked walls"
    )
])
def test_get_blocked_walls(walls, expected_blocked_walls):
    cell = Cell(0, 0)
    cell.walls = walls

    assert cell.get_blocked_walls() == expected_blocked_walls

@pytest.mark.parametrize("walls, expected_open_walls", [
    pytest.param(
        { "left": True, "right": False, "up": True, "down": False },
        ["right", "down"],
        id="when cell has open walls"
    ),
    pytest.param(
        { "left": True, "right": True, "up": True, "down": True },
        [],
        id="when cell does not have open walls"
    )
])
def test_get_open_walls(walls, expected_open_walls):
    cell = Cell(0, 0)
    cell.walls = walls

    assert cell.get_open_walls() == expected_open_walls

@pytest.mark.parametrize("cell, neighbor, expected_direction_to_neighbor", [
    pytest.param(
        Cell(1, 1),
        Cell(1, 2),
        "right",
        id="when neighbor is right of cell"
    ),
    pytest.param(
        Cell(1, 1),
        Cell(1, 0),
        "left",
        id="when neighbor is left of cell"
    ),
    pytest.param(
        Cell(1, 1),
        Cell(0, 1),
        "up",
        id="when neighbor is above cell"
    ),
    pytest.param(
        Cell(1, 1),
        Cell(2, 1),
        "down",
        id="when neighbor is below cell"
    )
])
def test_get_direction_to_neighbor(cell, neighbor, expected_direction_to_neighbor):
    assert cell.get_direction_to_neighbor(neighbor) == expected_direction_to_neighbor
