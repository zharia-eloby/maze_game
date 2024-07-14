import random

"""
only used for solving a maze. checks available paths for the current cell
"""
def check_paths(maze, curr_cell):
    available_paths = []

    # can go right from curr_cell, and hasn't visited the right neighbor
    if (maze[curr_cell[0]+1][curr_cell[1]] != 'w' and maze[curr_cell[0]+2][curr_cell[1]] != 'x'):
        available_paths += [(curr_cell[0]+2, curr_cell[1])]

    # can go left from curr_cell, and hasn't visited the left neighbor
    if (maze[curr_cell[0]-1][curr_cell[1]] != 'w' and maze[curr_cell[0]-2][curr_cell[1]] != 'x'):
        available_paths += [(curr_cell[0]-2, curr_cell[1])]

    # can go down from curr_cell, and hasn't visited the neighbor below
    if (maze[curr_cell[0]][curr_cell[1]+1] != 'w' and maze[curr_cell[0]][curr_cell[1]+2] != 'x'):
        available_paths += [(curr_cell[0], curr_cell[1]+2)]

    # can go up from curr_cell, and hasn't visited the neighbor above
    if (maze[curr_cell[0]][curr_cell[1]-1] != 'w' and maze[curr_cell[0]][curr_cell[1]-2] != 'x'):
        available_paths += [(curr_cell[0], curr_cell[1]-2)]

    return available_paths

"""
solves the maze by picking a random path and backtracking until the end is found
"""
def solve_maze(maze, start, end):
    solution_path = [start]
    curr_cell = start
    
    # mark the cell with 'x' in the maze array when visited
    maze[curr_cell[0]][curr_cell[1]] = 'x' 

    available_paths = []
    while (curr_cell != end):
        available_paths = check_paths(maze, curr_cell)

        # if all available neighbors have been visited, 
        # remove cells from the stack until there is an available neighbor
        while not available_paths:
            solution_path.pop()
            curr_cell = solution_path[len(solution_path)-1]
            available_paths = check_paths(maze, curr_cell)

        curr_cell = random.choice(available_paths)
        solution_path += [curr_cell]
        maze[curr_cell[0]][curr_cell[1]] = 'x'

    return solution_path