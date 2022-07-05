from maze import *

maze = create_maze(5, 5)
print(maze)
premade_maze = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], 
['w', 'v', 'w', 'v', 'o', 'v', 'o', 'v', 'o', 'v', 'w'], 
['w', 'o', 'w', 'w', 'w', 'o', 'w', 'w', 'w', 'w', 'w'], 
['w', 'v', 'o', 'v', 'w', 'v', 'w', 'v', 'o', 'v', 'w'], 
['w', 'w', 'w', 'o', 'w', 'o', 'w', 'o', 'w', 'o', 'w'], 
['w', 'v', 'w', 'v', 'w', 'v', 'o', 'v', 'w', 'v', 'w'], 
['w', 'o', 'w', 'o', 'w', 'o', 'w', 'w', 'w', 'o', 'w'], 
['w', 'v', 'o', 'v', 'w', 'v', 'w', 'v', 'o', 'v', 'w'], 
['w', 'o', 'w', 'w', 'w', 'w', 'w', 'o', 'w', 'o', 'w'], 
['w', 'v', 'o', 'v', 'o', 'v', 'o', 'v', 'w', 'v', 'w'], 
['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']]

def test_create_maze():
    assert len(maze) == 11 and len(maze[0]) == 11

def test_neighbor_check():
    curr_cell = (3, 3)
    paths = check_paths(premade_maze, curr_cell)
    assert paths == [(5, 3), (3, 1)]