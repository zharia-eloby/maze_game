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

def test_get_direction_to_neighbor():
    cell = Cell(1, 1)
    neighbor = Cell(1, 2)
    assert cell.get_direction_to_neighbor(neighbor) == "right"
    assert neighbor.get_direction_to_neighbor(cell) == "left"

    cell = Cell(2, 1)
    neighbor = Cell(1, 1)
    assert cell.get_direction_to_neighbor(neighbor) == "up"
    assert neighbor.get_direction_to_neighbor(cell) == "down"
