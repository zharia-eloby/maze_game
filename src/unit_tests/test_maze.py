import random
from src.general.maze import Maze

rows_min = 5
rows_max = 50
cols_min  = 5
cols_max = 50
rows = random.randint(rows_min, rows_max)
columns = random.randint(cols_min, cols_max)

def test_maze_init():
    # setup
    maze = Maze(rows, columns)

    # assert maze rows and columns are set. maze array is empty
    assert maze.rows == rows
    assert maze.columns == columns
    assert maze.maze == []

def test_create_maze():
    # setup
    maze = Maze(rows, columns)
    maze.create_maze()

    # assert maze array contains correct content
    assert len(maze.maze) == rows * 2 + 1
    for i in maze.maze:
        assert len(i) == columns * 2 + 1

def test_solve_maze():
    # setup
    maze = Maze(rows, columns)
    maze.create_maze()
    maze.solve_maze()

    # assert maze solution array contains correct content
    assert maze.startpoint == maze.solution[0]
    assert maze.endpoint == maze.solution[-1]

    previous_cell = maze.startpoint
    for i in range(1, len(maze.solution)):
        # assert current cell is 1 spot away from previous cell
        assert (previous_cell[0] == maze.solution[i][0]) ^ (previous_cell[1] == maze.solution[i][1])
        previous_cell = maze.solution[i]
