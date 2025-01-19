from app.src.general.maze import Cell, Maze

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

def test_update_maze_size():
    maze = Maze((5, 5))

    maze.update_maze_size((7, 9))
    assert maze.dimensions == (7, 9)
    assert len(maze.maze) == 7
    for row in maze.maze:
        assert len(row) == 9
        for cell in row:
            assert len(cell.get_blocked_walls()) == 4

def test_get_neighbor_cell():
    maze = Maze((5, 5))
    cell = maze.maze[2][2]

    assert maze.get_neighbor_cell(cell, "left") == maze.maze[2][1]
    assert maze.get_neighbor_cell(cell, "right") == maze.maze[2][3]
    assert maze.get_neighbor_cell(cell, "up") == maze.maze[1][2]
    assert maze.get_neighbor_cell(cell, "down") == maze.maze[3][2]

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

def test_solve_maze():
    rows = 5
    columns = 5
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
