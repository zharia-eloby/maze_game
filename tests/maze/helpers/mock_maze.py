from app.src.general.maze import Cell

cell_walls = [
    [
        {'left': True, 'right': False, 'up': True, 'down': True},
        {'left': False, 'right': False, 'up': True, 'down': True},
        {'left': False, 'right': False, 'up': True, 'down': True},
        {'left': False, 'right': False, 'up': True, 'down': False},
        {'left': False, 'right': True, 'up': True, 'down': False}
    ],
    [
        {'left': True, 'right': False, 'up': True, 'down': False},
        {'left': False, 'right': False, 'up': True, 'down': True},
        {'left': False, 'right': True, 'up': True, 'down': False},
        {'left': True, 'right': True, 'up': False, 'down': False},
        {'left': True, 'right': True, 'up': False, 'down': False}
    ],
    [
        {'left': True, 'right': True, 'up': False, 'down': False},
        {'left': True, 'right': True, 'up': True, 'down': False},
        {'left': True, 'right': True, 'up': False, 'down': False},
        {'left': True, 'right': True, 'up': False, 'down': False},
        {'left': True, 'right': True, 'up': False, 'down': False}
    ],
    [
        {'left': True, 'right': True, 'up': False, 'down': True},
        {'left': True, 'right': True, 'up': False, 'down': False},
        {'left': True, 'right': False, 'up': False, 'down': True},
        {'left': False, 'right': True, 'up': False, 'down': True},
        {'left': True, 'right': True, 'up': False, 'down': False}
    ],
    [
        {'left': True, 'right': False, 'up': True, 'down': True},
        {'left': False, 'right': False, 'up': False, 'down': True},
        {'left': False, 'right': False, 'up': True, 'down': True},
        {'left': False, 'right': False, 'up': True, 'down': True},
        {'left': False, 'right': True, 'up': False, 'down': True}
    ]
]

"""
creates a 5x5 maze
"""
def get_example_maze():
    rows = len(cell_walls)
    columns = len(cell_walls[0])
    maze = [ [ Cell(j, i) for i in range(rows) ] for j in range(columns) ]
    for i in range(rows):
        for j in range(columns):
            maze[i][j].walls = cell_walls[i][j]
    return maze
