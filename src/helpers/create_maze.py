import random

"""
only used when creating the maze. returns a list of unvisited neighbors
"""
def check_neighbors(maze, curr_cell):
    available_neighbors = []
    if (curr_cell[1] > 1):                  # check that it CAN have a left neighbor, then check if it has an unvisited left neighbor
        if (maze[curr_cell[0]][curr_cell[1]-2] != 'v'):
            available_neighbors += [(curr_cell[0], curr_cell[1]-2)]
            
    if (curr_cell[1] < len(maze[0]) - 2):     # if CAN have right neighbor, check that the right neighbor is unvisited
        if (maze[curr_cell[0]][curr_cell[1]+2] != 'v'):
            available_neighbors += [(curr_cell[0], curr_cell[1]+2)]
            
    if (curr_cell[0] > 1):                  # if CAN have upper neighbor, check that the upper neighbor is unvisited
        if (maze[curr_cell[0]-2][curr_cell[1]] != 'v'):
            available_neighbors += [(curr_cell[0]-2, curr_cell[1])]
            
    if (curr_cell[0] < len(maze) - 2):     # if CAN have below neighbor, check that the below neighbor is unvisited
        if (maze[curr_cell[0]+2][curr_cell[1]] != 'v'):
            available_neighbors += [(curr_cell[0]+2, curr_cell[1])]
            
    return available_neighbors

"""
creates a maze of the specified dimensions using the backtracking algorithm
"""
def create_maze(num_rows, num_cols):
    # create grid. erase walls as maze is created
    maze = []
    for i in range(0, num_rows*2+1):
        row = []
        for j in range(0, num_cols*2+1):
            if (i % 2 == 0):
                row += ['w']
            else:
                if (j % 2 == 0):
                    row += ['w']
                else:
                    row += ['c']
        maze.append(row)
    
    cells_to_go = (num_rows*num_cols)-1 # when this gets to 0, it's done
    
    stack = []
    stack.append((1,1))
    maze[1][1] = 'v'
    
    while (cells_to_go > 0):
        curr_cell = stack.pop()
        stack.append(curr_cell)
        
        neighbors = check_neighbors(maze, curr_cell)
        
        if (len(neighbors) > 0):
            chosen = random.choice(neighbors)
            
            # remove the wall in between the current cell and its chosen neighbor
            if (chosen[0] == curr_cell[0]):         # same row
                if (chosen[1] > curr_cell[1]):      # neighbor is on the right
                    maze[curr_cell[0]][curr_cell[1]+1] = 'o'
                else:
                    maze[curr_cell[0]][curr_cell[1]-1] = 'o'
                    
            else:                                   # same column
                if (chosen[0] > curr_cell[0]):      # neighbor is below
                    maze[curr_cell[0]+1][curr_cell[1]] = 'o'
                else:
                    maze[curr_cell[0]-1][curr_cell[1]] = 'o'

            maze[chosen[0]][chosen[1]] = 'v'
            cells_to_go -= 1
            if (cells_to_go == 0):
                endpoint = chosen
            stack.append(chosen)
            
        else:
            stack.pop()

    return { "maze": maze, "endpoint": endpoint }