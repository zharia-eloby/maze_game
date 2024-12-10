from src.general.maze import Cell

def test_get_blocked_walls():
    cell = Cell(0, 0)
    cell.walls = { "left": True, "right": False, "up": True, "down": False }
    assert cell.get_blocked_walls() == ["left", "up"]

def test_get_open_walls():
    cell = Cell(0, 0)
    cell.walls = { "left": True, "right": False, "up": True, "down": False }
    assert cell.get_open_walls() == ["right", "down"]
