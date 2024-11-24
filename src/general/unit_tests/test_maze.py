import random
from src.general.maze import Cell, Maze

rows_min = 5
rows_max = 50
cols_min  = 5
cols_max = 50

def test_init():
    rows = random.randint(rows_min, rows_max)
    columns = random.randint(cols_min, cols_max)
    maze = Maze((rows, columns))

    assert maze.dimensions == (rows, columns)
    assert maze.startpoint == None
    assert maze.endpoint == None
    assert maze.solution == []
    assert len(maze.maze) == rows
    for row in maze.maze:
        assert len(row) == columns
        for cell in row:
            assert len(cell.get_blocked_walls()) == 4

def test_update_maze_size():
    maze = Maze((5, 5))

    maze.update_maze_size((7, 9))
    assert maze.dimensions == (7, 9)
    assert len(maze.maze) == 7
    for row in maze.maze:
        assert len(row) == 9
        for cell in row:
            assert len(cell.get_blocked_walls()) == 4

def test_remove_wall_between_cells():
    maze = Maze((10, 10))

    cell = Cell(4, 5)
    neighbor = Cell(5, 5)
    maze.remove_wall_between_cells(cell, neighbor)
    assert cell.walls["down"] == False
    assert neighbor.walls["up"] == False
    assert cell.walls["up"] and cell.walls["left"] and cell.walls["right"]
    assert neighbor.walls["down"] and neighbor.walls["left"] and neighbor.walls["right"]

    cell = Cell(4, 5)
    neighbor = Cell(3, 5)
    maze.remove_wall_between_cells(cell, neighbor)
    assert cell.walls["up"] == False
    assert neighbor.walls["down"] == False
    assert cell.walls["down"] and cell.walls["left"] and cell.walls["right"]
    assert neighbor.walls["up"] and neighbor.walls["left"] and neighbor.walls["right"]

    cell = Cell(6, 3)
    neighbor = Cell(6, 2)
    maze.remove_wall_between_cells(cell, neighbor)
    assert cell.walls["left"] == False
    assert neighbor.walls["right"] == False
    assert cell.walls["up"] and cell.walls["down"] and cell.walls["right"]
    assert neighbor.walls["down"] and neighbor.walls["up"] and neighbor.walls["left"]

    cell = Cell(9, 7)
    neighbor = Cell(9, 8)
    maze.remove_wall_between_cells(cell, neighbor)
    assert cell.walls["right"] == False
    assert neighbor.walls["left"] == False
    assert cell.walls["up"] and cell.walls["down"] and cell.walls["left"]
    assert neighbor.walls["down"] and neighbor.walls["up"] and neighbor.walls["right"]
    
def test_create_maze():
    rows = random.randint(rows_min, rows_max)
    columns = random.randint(cols_min, cols_max)
    maze = Maze((rows, columns))
    maze.create_maze()

    # assert all cells have at least one open path
    for row in maze.maze:
        for cell in row:
            assert len(cell.get_blocked_walls()) < 4

    assert maze.startpoint != None
    assert maze.endpoint != None
    assert maze.startpoint != maze.endpoint

def test_solve_maze():
    rows = random.randint(rows_min, rows_max)
    columns = random.randint(cols_min, cols_max)
    maze = Maze((rows, columns))
    maze.create_maze()
    maze.solve_maze()

    # assert maze solution array contains correct content
    assert len(maze.solution) > 0
    assert maze.startpoint == maze.solution[0]
    assert maze.endpoint == maze.solution[-1]

    previous_cell = maze.startpoint
    for i in range(1, len(maze.solution)):
        # assert current cell is 1 spot away from previous cell
        assert (previous_cell.row_index == maze.solution[i].row_index) ^ (previous_cell.col_index == maze.solution[i].col_index)
        previous_cell = maze.solution[i]
