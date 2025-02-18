import pytest
from app.src.general.maze import Cell, Maze
from helpers.mock_maze import get_example_maze

@pytest.fixture
def mock_maze():
    return get_example_maze()

def test_maze_init():
    rows = 10
    columns = 6
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

def test_update_maze_size(mock_maze):
    mock_maze.update_maze_size((7, 9))
    assert mock_maze.dimensions == (7, 9)
    assert len(mock_maze.maze) == 7
    for row in mock_maze.maze:
        assert len(row) == 9
        for cell in row:
            assert len(cell.get_blocked_walls()) == 4

@pytest.mark.parametrize("direction, expected_row_col", [
    pytest.param(
        "left",
        (2, 1),
        id="when neighbor is left of the current cell"
    ),
    pytest.param(
        "right",
        (2, 3),
        id="when neighbor is right of the current cell"
    ),
    pytest.param(
        "up",
        (1, 2),
        id="when neighbor is above the current cell"
    ),
    pytest.param(
        "down",
        (3, 2),
        id="when neighbor is below the current cell"
    )
])
def test_get_neighbor_cell(mock_maze, direction, expected_row_col):
    cell = mock_maze.maze[2][2]
    row = expected_row_col[0]
    col = expected_row_col[1]
    assert mock_maze.get_neighbor_cell(cell, direction) == mock_maze.maze[row][col]

def test_get_unvisited_neighbors():
    maze = Maze((5, 5))
    cell = maze.maze[2][2]

    unvisited_neighbors = maze.get_unvisited_neighbors(cell, False)
    assert len(unvisited_neighbors) == 4
    assert maze.maze[2][1] in unvisited_neighbors
    assert maze.maze[2][3] in unvisited_neighbors
    assert maze.maze[1][2] in unvisited_neighbors
    assert maze.maze[3][2] in unvisited_neighbors

    unvisited_neighbors = maze.get_unvisited_neighbors(cell, True)
    assert len(unvisited_neighbors) == 0

    maze.maze[2][1].visited = True
    maze.maze[3][2].visited = True
    cell.walls["left"] = False
    cell.walls["up"] = False

    unvisited_neighbors = maze.get_unvisited_neighbors(cell, False)
    assert len(unvisited_neighbors) == 2
    assert maze.maze[2][3] in unvisited_neighbors
    assert maze.maze[1][2] in unvisited_neighbors

    unvisited_neighbors = maze.get_unvisited_neighbors(cell, True)
    assert len(unvisited_neighbors) == 1
    assert maze.maze[1][2] in unvisited_neighbors

def test_set_startpoint_endpoint():
    maze = Maze((5, 5))
    maze.set_startpoint_endpoint()

    assert type(maze.startpoint) == Cell
    assert type(maze.endpoint) == Cell

    assert maze.startpoint.row_index >= 0
    assert maze.startpoint.row_index < 5
    assert maze.endpoint.row_index >= 0
    assert maze.endpoint.row_index < 5

    assert maze.startpoint.col_index >= 0
    assert maze.startpoint.col_index < 5
    assert maze.endpoint.col_index >= 0
    assert maze.endpoint.col_index < 5

def test_reset_visited():
    maze = Maze((5, 5))
    for row in maze.maze:
        for cell in row:
            cell.visited == True

    maze.reset_visited()
    for row in maze.maze:
        for cell in row:
            assert cell.visited == False

@pytest.mark.parametrize("cell, neighbor, expected_cell_walls, expected_neighbor_walls", [
    pytest.param(
        Cell(4, 5),
        Cell(5, 5),
        {
            'left': True,
            'right': True,
            'up': True,
            'down': False
        },
        {
            'left': True,
            'right': True,
            'up': False,
            'down': True
        },
        id="when removing the wall between the 'down' neighbor"
    ),
    pytest.param(
        Cell(4, 5),
        Cell(3, 5),
        {
            'left': True,
            'right': True,
            'up': False,
            'down': True
        },
        {
            'left': True,
            'right': True,
            'up': True,
            'down': False
        },
        id="when removing the wall between the 'up' neighbor"
    ),
    pytest.param(
        Cell(4, 5),
        Cell(4, 4),
        {
            'left': False,
            'right': True,
            'up': True,
            'down': True
        },
        {
            'left': True,
            'right': False,
            'up': True,
            'down': True
        },
        id="when removing the wall between the 'left' neighbor"
    ),
    pytest.param(
        Cell(4, 5),
        Cell(4, 6),
        {
            'left': True,
            'right': False,
            'up': True,
            'down': True
        },
        {
            'left': False,
            'right': True,
            'up': True,
            'down': True
        },
        id="when removing the wall between the 'right' neighbor"
    )
])
def test_remove_wall_between_cells(cell, neighbor, expected_cell_walls, expected_neighbor_walls):
    maze = Maze((10, 10))
    maze.remove_wall_between_cells(cell, neighbor)
    assert cell.walls == expected_cell_walls
    assert neighbor.walls == expected_neighbor_walls
    
def test_create_maze():
    rows = 5
    columns = 5
    maze = Maze((rows, columns))
    maze.create_maze()

    # assert all cells have at least one open path
    for row in maze.maze:
        for cell in row:
            assert len(cell.get_blocked_walls()) < 4

    assert maze.startpoint != None
    assert maze.endpoint != None
    assert maze.startpoint != maze.endpoint

def test_solve_maze(mock_maze):
    expected_solution = mock_maze.solution

    maze = Maze((5, 5))
    maze.maze = mock_maze.maze
    maze.startpoint = mock_maze.startpoint
    maze.endpoint = mock_maze.endpoint
    maze.solve_maze()

    assert maze.solution == expected_solution
