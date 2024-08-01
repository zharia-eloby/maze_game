import math, random, pygame, pygame_gui
from pygame_gui.core import ObjectID

class Maze:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.maze = []
        self.startpoint = None
        self.endpoint = None
        self.player_position = None
    
    def check_neighbors(self, current_position):
        available_neighbors = []
        if current_position[1] > 1:                  # check that it CAN have a left neighbor, then check if it has an unvisited left neighbor
            if self.maze[current_position[0]][current_position[1]-2] != 'v':
                available_neighbors += [(current_position[0], current_position[1]-2)]
                
        if current_position[1] < len(self.maze[0]) - 2:     # if CAN have right neighbor, check that the right neighbor is unvisited
            if self.maze[current_position[0]][current_position[1]+2] != 'v':
                available_neighbors += [(current_position[0], current_position[1]+2)]
                
        if current_position[0] > 1:                  # if CAN have upper neighbor, check that the upper neighbor is unvisited
            if self.maze[current_position[0]-2][current_position[1]] != 'v':
                available_neighbors += [(current_position[0]-2, current_position[1])]
                
        if current_position[0] < len(self.maze) - 2:     # if CAN have below neighbor, check that the below neighbor is unvisited
            if self.maze[current_position[0]+2][current_position[1]] != 'v':
                available_neighbors += [(current_position[0]+2, current_position[1])]
                
        return available_neighbors
    
    """
    use the backtracking algorithm to create a maze
    """
    def create_maze(self):
        # start by creating a grid. walls will be erased later to create the maze
        for i in range(0, self.rows*2+1):
            row = []
            for j in range(0, self.columns*2+1):
                if i % 2 == 0:
                    row += ['w']
                else:
                    if j % 2 == 0:
                        row += ['w']
                    else:
                        row += ['c']
            self.maze.append(row)
        
        cells_to_go = (self.rows*self.columns)-1 # when this gets to 0, all cells have been visited and the maze is finished
        
        stack = []
        stack.append((1,1))
        self.maze[1][1] = 'v'
        
        while (cells_to_go > 0):
            curr_cell = stack.pop()
            stack.append(curr_cell)
            
            neighbors = self.check_neighbors(curr_cell)
            
            if len(neighbors) > 0:
                chosen = random.choice(neighbors)
                
                # remove the wall in between the current cell and its chosen neighbor
                if chosen[0] == curr_cell[0]:         # current cell & chosen neighbor are in the same row
                    if chosen[1] > curr_cell[1]:      # neighbor is on the right
                        self.maze[curr_cell[0]][curr_cell[1]+1] = 'o'
                    else:
                        self.maze[curr_cell[0]][curr_cell[1]-1] = 'o'
                        
                else:                                   # current cell & chosen neighbor are in the same column
                    if chosen[0] > curr_cell[0]:      # neighbor is below
                        self.maze[curr_cell[0]+1][curr_cell[1]] = 'o'
                    else:
                        self.maze[curr_cell[0]-1][curr_cell[1]] = 'o'

                self.maze[chosen[0]][chosen[1]] = 'v'
                cells_to_go -= 1
                if cells_to_go == 0:
                    self.endpoint = chosen
                    while (self.startpoint is None) or (self.endpoint == self.startpoint):
                        self.startpoint = (random.randrange(0, self.rows) * 2 + 1, random.randrange(0, self.columns) * 2 + 1)
                stack.append(chosen)
            else:
                stack.pop()

    """
    only used for solving a maze. checks available paths for the current cell
    """
    def check_paths(self, curr_cell):
        available_paths = []

        # can go right from curr_cell, and hasn't visited the right neighbor
        if (self.maze[curr_cell[0]+1][curr_cell[1]] != 'w') and (self.maze[curr_cell[0]+2][curr_cell[1]] != 'x'):
            available_paths += [(curr_cell[0]+2, curr_cell[1])]

        # can go left from curr_cell, and hasn't visited the left neighbor
        if (self.maze[curr_cell[0]-1][curr_cell[1]] != 'w') and (self.maze[curr_cell[0]-2][curr_cell[1]] != 'x'):
            available_paths += [(curr_cell[0]-2, curr_cell[1])]

        # can go down from curr_cell, and hasn't visited the neighbor below
        if (self.maze[curr_cell[0]][curr_cell[1]+1] != 'w') and (self.maze[curr_cell[0]][curr_cell[1]+2] != 'x'):
            available_paths += [(curr_cell[0], curr_cell[1]+2)]

        # can go up from curr_cell, and hasn't visited the neighbor above
        if (self.maze[curr_cell[0]][curr_cell[1]-1] != 'w') and (self.maze[curr_cell[0]][curr_cell[1]-2] != 'x'):
            available_paths += [(curr_cell[0], curr_cell[1]-2)]

        return available_paths

    """
    solves the maze by picking a random path and backtracking until the end is found
    """
    def solve_maze(self):
        solution_path = [self.startpoint]
        curr_cell = self.startpoint
        
        # mark the cell with 'x' in the maze array when visited
        self.maze[curr_cell[0]][curr_cell[1]] = 'x' 

        available_paths = []
        while (curr_cell != self.endpoint):
            available_paths = self.check_paths(curr_cell)

            # if all neighbors have been visited, pop from the stack until there is an available neighbor
            while not available_paths:
                solution_path.pop()
                curr_cell = solution_path[len(solution_path)-1]
                available_paths = self.check_paths(curr_cell)

            curr_cell = random.choice(available_paths)
            solution_path += [curr_cell]
            self.maze[curr_cell[0]][curr_cell[1]] = 'x'
        return solution_path
    
class MazeUI(Maze):
    def __init__(self, rows, columns, game_window):
        super().__init__(rows, columns)
        self.maze_width = None
        self.maze_height = None
        self.cell_width = None
        self.cell_height = None
        self.wall_thickness = None
        self.topleft = None
        self.player = None
        self.game_window = game_window
        
    def set_maze_ui_measurements(self, ui_area):
        if ui_area.width > ui_area.height:
            self.maze_height = ui_area.height
        else:
            self.maze_height = ui_area.width
        self.maze_width = self.maze_height
        
        self.cell_width = round(self.maze_width/self.columns)
        self.cell_height = round(self.maze_height/self.rows)

        self.wall_thickness = round(self.cell_width/10)
        if self.wall_thickness < 2: self.wall_thickness = 2

        # maze width & height may be slightly different. reset them to the actual width & height
        self.maze_width = self.cell_width * self.columns + self.wall_thickness
        self.maze_height = self.cell_height * self.rows + self.wall_thickness
        # set startpoint so the maze is horizontally centered
        self.topleft = (ui_area.centerx - round(self.maze_width/2), ui_area.bottom - self.maze_height)
    
    def draw_maze(self, manager):
        x_pos = self.topleft[0]
        y_pos = self.topleft[1]
        for i in range(0, self.rows*2+1):
            for j in range(0, self.columns*2+1):
                if (i % 2 == 0) and (j % 2 == 1): # horizontal
                    if self.maze[i][j] == 'w':
                        wall_rect = pygame.Rect(
                            x_pos,
                            y_pos,
                            self.cell_width,
                            self.wall_thickness
                        )
                        pygame_gui.elements.UIPanel(
                            relative_rect=wall_rect,
                            manager=manager,
                            object_id=ObjectID(class_id="@wall")
                        )
                    x_pos += self.cell_width
                elif (i % 2 == 1) and (j % 2 == 0): # vertical
                    if self.maze[i][j] == 'w':
                        wall_rect = pygame.Rect(
                            x_pos,
                            y_pos,
                            self.wall_thickness,
                            self.cell_height + self.wall_thickness
                        )
                        pygame_gui.elements.UIPanel(
                            relative_rect=wall_rect,
                            manager=manager,
                            object_id=ObjectID(class_id="@wall")
                        )
                    x_pos += self.cell_width
            if i % 2 == 1:
                y_pos += self.cell_height
            x_pos = self.topleft[0]

    """
    get the ui position of the cell based on index in the maze grid
    """
    def get_cell_ui_position(self, index):
        x_position = ((index[1]-1)/2) * self.cell_width + self.topleft[0] + self.wall_thickness
        y_position = ((index[0]-1)/2) * self.cell_height + self.topleft[1] + self.wall_thickness
        return (x_position, y_position)

    def move_player(self, direction):
        current_position = self.player_position
        if direction == "reset":
            start_rect = self.get_cell_ui_position(self.startpoint)
            startpoint_left = start_rect[0] + self.cell_width/2 - self.player.get_relative_rect().width/2 - self.wall_thickness/2
            startpoint_top = start_rect[1] + self.cell_height/2 - self.player.get_relative_rect().height/2 - self.wall_thickness/2
            self.player.set_relative_position((startpoint_left, startpoint_top))
            current_position = (self.startpoint[0], self.startpoint[1])
            self.player_position = current_position
            return

        current_left = self.player.get_relative_rect().left
        current_top = self.player.get_relative_rect().top
        if direction == "up" and self.maze[current_position[0]-1][current_position[1]] == "o":
            self.player.set_relative_position((current_left, current_top - self.cell_height))
            current_position = (current_position[0] - 2, current_position[1])

        elif direction == "down" and self.maze[current_position[0]+1][current_position[1]] == "o":
            self.player.set_relative_position((current_left, current_top + self.cell_height))
            current_position = (current_position[0] + 2, current_position[1])

        elif direction == "left" and self.maze[current_position[0]][current_position[1]-1] == "o":
            self.player.set_relative_position((current_left - self.cell_width, current_top))
            current_position = (current_position[0], current_position[1] - 2)

        elif direction == "right" and self.maze[current_position[0]][current_position[1]+1] == "o":
            self.player.set_relative_position((current_left + self.cell_width, current_top))
            current_position = (current_position[0], current_position[1] + 2)
        self.player_position = current_position
    
    def setup_maze_ui(self, manager): 
        self.create_maze()
        self.player_position = self.startpoint
        self.set_maze_ui_measurements(self.game_window.drawable_area)
        self.draw_maze(manager)

        ui_position = self.get_cell_ui_position(self.startpoint)
        start_rect = pygame.Rect(
            ui_position[0],
            ui_position[1],
            self.cell_width - self.wall_thickness,
            self.cell_height - self.wall_thickness
        )
        pygame_gui.elements.UIPanel(
            relative_rect=start_rect,
            manager=manager,
            object_id=ObjectID(object_id="#startpoint")
        )

        ui_position = self.get_cell_ui_position(self.endpoint)
        end_rect = pygame.Rect(
            ui_position[0],
            ui_position[1],
            self.cell_width - self.wall_thickness,
            self.cell_height - self.wall_thickness
        )
        pygame_gui.elements.UIPanel(
            relative_rect=end_rect,
            manager=manager,
            object_id=ObjectID(object_id="#endpoint")
        )

        player_margin = round(self.wall_thickness * 1.5)
        # set player width to be the smaller of cell width and cell height
        if start_rect.width > start_rect.height:
            player_width = self.cell_height - player_margin*2
        else:
            player_width = self.cell_width - player_margin*2
        player_height = player_width

        player_rect = pygame.Rect(
            start_rect.centerx - player_width/2,
            start_rect.centery - player_height/2,
            player_width,
            player_height
        )
        self.player = pygame_gui.elements.UIPanel(
            relative_rect=player_rect,
            manager=manager,
            object_id=ObjectID(object_id="#player")
        )
    
    def reset_maze(self):
        self.maze = []
        self.maze_width = None
        self.maze_height = None
        self.cell_width = None
        self.cell_height = None
        self.wall_thickness = None
        self.startpoint = None
        self.endpoint = None
        self.topleft = None
        self.player = None
        self.player_position = None
