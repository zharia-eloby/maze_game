import pygame
from app.src.general.maze import Maze

cell_walls = [
    [
        {'left': True, 'right': True, 'up': True, 'down': False},
        {'left': True, 'right': False, 'up': True, 'down': False},
        {'left': False, 'right': False, 'up': True, 'down': False},
        {'left': False, 'right': False, 'up': True, 'down': True},
        {'left': False, 'right': True, 'up': True, 'down': False}
    ],
    [
        {'left': True, 'right': False, 'up': False, 'down': False},
        {'left': False, 'right': True, 'up': False, 'down': True},
        {'left': True, 'right': True, 'up': False, 'down': False},
        {'left': True, 'right': False, 'up': True, 'down': False},
        {'left': False, 'right': True, 'up': False, 'down': True}
    ],
    [
        {'left': True, 'right': True, 'up': False, 'down': False},
        {'left': True, 'right': True, 'up': True, 'down': False},
        {'left': True, 'right': True, 'up': False, 'down': False},
        {'left': True, 'right': False, 'up': False, 'down': False},
        {'left': False, 'right': True, 'up': True, 'down': True}
    ],
    [
        {'left': True, 'right': False, 'up': False, 'down': True},
        {'left': False, 'right': True, 'up': False, 'down': False},
        {'left': True, 'right': True, 'up': False, 'down': False},
        {'left': True, 'right': True, 'up': False, 'down': True},
        {'left': True, 'right': True, 'up': True, 'down': False}
    ],
    [
        {'left': True, 'right': False, 'up': True, 'down': True},
        {'left': False, 'right': True, 'up': False, 'down': True},
        {'left': True, 'right': False, 'up': False, 'down': True},
        {'left': False, 'right': False, 'up': True, 'down': True},
        {'left': False, 'right': True, 'up': False, 'down': True}
    ]
]

cell_width = 50
cell_height = 50
cell_rects = [
    [
        pygame.Rect(0, 0, cell_width, cell_height),
        pygame.Rect(50, 0, cell_width, cell_height),
        pygame.Rect(100, 0, cell_width, cell_height),
        pygame.Rect(150, 0, cell_width, cell_height),
        pygame.Rect(200, 0, cell_width, cell_height)
    ],
    [
        pygame.Rect(0, 50, cell_width, cell_height),
        pygame.Rect(50, 50, cell_width, cell_height),
        pygame.Rect(100, 50, cell_width, cell_height),
        pygame.Rect(150, 50, cell_width, cell_height),
        pygame.Rect(200, 50, cell_width, cell_height)
    ],
    [
        pygame.Rect(0, 100, cell_width, cell_height),
        pygame.Rect(50, 100, cell_width, cell_height),
        pygame.Rect(100, 100, cell_width, cell_height),
        pygame.Rect(150, 100, cell_width, cell_height),
        pygame.Rect(200, 100, cell_width, cell_height)
    ],
    [
        pygame.Rect(0, 150, cell_width, cell_height),
        pygame.Rect(50, 150, cell_width, cell_height),
        pygame.Rect(100, 150, cell_width, cell_height),
        pygame.Rect(150, 150, cell_width, cell_height),
        pygame.Rect(200, 150, cell_width, cell_height)
    ],
    [
        pygame.Rect(0, 200, cell_width, cell_height),
        pygame.Rect(50, 200, cell_width, cell_height),
        pygame.Rect(100, 200, cell_width, cell_height),
        pygame.Rect(150, 200, cell_width, cell_height),
        pygame.Rect(200, 200, cell_width, cell_height)
    ]
]

"""
creates a 5x5 maze
"""
def get_example_maze():
    rows = len(cell_walls)
    columns = len(cell_walls[0])
    maze = Maze((rows, columns))
    for i in range(rows):
        for j in range(columns):
            maze.maze[i][j].walls = cell_walls[i][j]
            maze.maze[i][j].rect = cell_rects[i][j]

    maze.startpoint = maze.maze[0][0]
    maze.endpoint = maze.maze[4][4]
    maze.solution = [
        maze.maze[0][0],
        maze.maze[1][0],
        maze.maze[1][1],
        maze.maze[0][1],
        maze.maze[0][2],
        maze.maze[1][2],
        maze.maze[2][2],
        maze.maze[3][2],
        maze.maze[4][2],
        maze.maze[4][3],
        maze.maze[4][4]
    ]
    return maze
