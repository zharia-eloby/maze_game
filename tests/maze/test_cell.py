import pytest
from app.src.general.maze import Cell

def test_cell_init():
    cell = Cell(2, 5)
    
    assert cell.row_index == 2
    assert cell.col_index == 5
    assert cell.walls == { "left": True, "right": True, "up": True, "down": True }
    assert cell.visited == False
    assert cell.rect == None

def test_get_blocked_walls():
    cell = Cell(0, 0)

    cell.walls = { "left": True, "right": False, "up": True, "down": False }
    assert cell.get_blocked_walls() == ["left", "up"]

    cell.walls = { "left": False, "right": False, "up": False, "down": False }
    assert cell.get_blocked_walls() == []

def test_get_open_walls():
    cell = Cell(0, 0)

    cell.walls = { "left": True, "right": False, "up": True, "down": False }
    assert cell.get_open_walls() == ["right", "down"]

    cell.walls = { "left": True, "right": True, "up": True, "down": True }
    assert cell.get_open_walls() == []

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
