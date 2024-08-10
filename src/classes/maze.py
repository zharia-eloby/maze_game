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
        self.solution = []

    def get_neighbors(self, cell, cell_exclusions, wall_exclusions):
        neighbors = []

        # check if cell can have left neighbor. if so, check that left neighbor is valid
        if cell[1] > 1:
            if (self.maze[cell[0]][cell[1]-1] not in wall_exclusions) and (self.maze[cell[0]][cell[1]-2] not in cell_exclusions):
                neighbors += [(cell[0], cell[1]-2)]
                
        # check if cell can have right neighbor. if so, check that right neighbor is valid
        if cell[1] < len(self.maze[0]) - 2:
            if (self.maze[cell[0]][cell[1]+1] not in wall_exclusions) and (self.maze[cell[0]][cell[1]+2] not in cell_exclusions):
                neighbors += [(cell[0], cell[1]+2)]
                
        # check if cell can have above neighbor. if so, check that above neighbor is valid
        if cell[0] > 1:
            if (self.maze[cell[0]-1][cell[1]] not in wall_exclusions) and (self.maze[cell[0]-2][cell[1]] not in cell_exclusions):
                neighbors += [(cell[0]-2, cell[1])]
                
        # check if cell can have below neighbor. if so, check that below neighbor is valid
        if cell[0] < len(self.maze) - 2:
            if (self.maze[cell[0]+1][cell[1]] not in wall_exclusions) and (self.maze[cell[0]+2][cell[1]] not in cell_exclusions):
                neighbors += [(cell[0]+2, cell[1])]

        return neighbors
    
    """
    use the backtracking algorithm to create a maze
    """
    def create_maze(self):
        # start by creating a grid. walls will be erased later to create the maze
        for i in range(self.rows):
            self.maze.append(['w']*(self.columns*2+1))
            self.maze.append(['w', 'c']*(self.columns) + ['w'])
        self.maze.append(['w']*(self.columns*2+1))

        stack = []
        curr_cell = (random.randrange(0, len(self.maze)-1, 2) + 1, random.randrange(0, len(self.maze[0])-1, 2) + 1)
        stack.append(curr_cell)
        self.maze[curr_cell[0]][curr_cell[1]] = 'v'

        while (len(stack) > 0):
            neighbors = self.get_neighbors(curr_cell, ['v'], [])
            
            if len(neighbors) > 0:
                chosen = random.choice(neighbors)
                
                # remove the wall in between the current cell and its chosen neighbor
                row_index = curr_cell[0] + int((chosen[0] - curr_cell[0])/2)
                column_index = curr_cell[1] + int((chosen[1] - curr_cell[1])/2)
                self.maze[row_index][column_index] = 'o'

                self.maze[chosen[0]][chosen[1]] = 'v'

                stack.append(chosen)
                curr_cell = chosen
            else:
                curr_cell = stack.pop()

        self.endpoint = curr_cell
        while (self.startpoint is None) or (self.endpoint == self.startpoint):
            self.startpoint = (random.randrange(0, len(self.maze)-1, 2) + 1, random.randrange(0, len(self.maze[0])-1, 2) + 1)

    """
    solves the maze by picking a random path and backtracking until the end is found
    """
    def solve_maze(self):
        self.solution = [self.startpoint]
        curr_cell = self.startpoint
        
        # mark the cell with 'x' in the maze array when visited
        self.maze[curr_cell[0]][curr_cell[1]] = 'x' 

        available_paths = []
        while (curr_cell != self.endpoint):
            available_paths = self.get_neighbors(curr_cell, ['x'], ['w'])

            # if all neighbors have been visited, pop from the stack until there is an available neighbor
            while not available_paths:
                self.solution.pop()
                curr_cell = self.solution[-1]
                available_paths = self.get_neighbors(curr_cell, ['x'], ['w'])

            curr_cell = random.choice(available_paths)
            self.solution += [curr_cell]
            self.maze[curr_cell[0]][curr_cell[1]] = 'x'
    
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
        self.maze_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)

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
    
    def draw_maze(self):
        x_pos = self.topleft[0]
        y_pos = self.topleft[1]
        for i in range(0, len(self.maze)):
            for j in range(0, len(self.maze[0])):
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
                            manager=self.maze_manager,
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
                            manager=self.maze_manager,
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

    """
    move the player in the given direction
    - direction: a tuple. 1st value is the number of rows to move, 2nd value is the number of columns to move
    - (0, 1) moves the player right one cell, (1, 0) moves the player down one cell, etc
    - (0, 0) resets the player to the startpoint
    """
    def move_player(self, direction):
        current_position = self.player_position
        if direction == (0, 0):
            start_rect = self.get_cell_ui_position(self.startpoint)
            startpoint_left = start_rect[0] + self.cell_width/2 - self.player.get_relative_rect().width/2 - self.wall_thickness/2
            startpoint_top = start_rect[1] + self.cell_height/2 - self.player.get_relative_rect().height/2 - self.wall_thickness/2
            self.player.set_relative_position((startpoint_left, startpoint_top))
            current_position = (self.startpoint[0], self.startpoint[1])
            self.player_position = current_position
            return

        current_left = self.player.get_relative_rect().left
        current_top = self.player.get_relative_rect().top
        if self.maze[current_position[0]+direction[0]][current_position[1]+direction[1]] == "o":
            self.player.set_relative_position((current_left + (self.cell_width*direction[1]), current_top + (self.cell_height*direction[0])))
            current_position = (current_position[0] + (direction[0]*2), current_position[1] + (direction[1]*2))

        self.player_position = current_position
    
    def setup_maze_ui(self): 
        self.create_maze()
        self.player_position = self.startpoint
        self.set_maze_ui_measurements(self.game_window.drawable_area)
        self.draw_maze()

        ui_position = self.get_cell_ui_position(self.startpoint)
        start_rect = pygame.Rect(
            ui_position[0],
            ui_position[1],
            self.cell_width - self.wall_thickness,
            self.cell_height - self.wall_thickness
        )
        pygame_gui.elements.UIPanel(
            relative_rect=start_rect,
            manager=self.maze_manager,
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
            manager=self.maze_manager,
            object_id=ObjectID(object_id="#endpoint")
        )

        player_margin = round(self.wall_thickness * 1.5)
        # set player width to be the smaller of cell width and cell height
        if start_rect.width > start_rect.height:
            player_width = start_rect.height - player_margin*2
        else:
            player_width = start_rect.width - player_margin*2
        player_height = player_width

        player_rect = pygame.Rect(
            start_rect.left + (start_rect.width - player_width)/2,
            start_rect.top + (start_rect.height - player_height)/2,
            player_width,
            player_height
        )
        self.player = pygame_gui.elements.UIPanel(
            relative_rect=player_rect,
            manager=self.maze_manager,
            object_id=ObjectID(object_id="#player")
        )

    def draw_solution_path(self, index, line):
        return index + 1
    
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
        self.solution = []
        self.maze_manager.clear_and_reset()

class LineSolutionPath():
    def __init__(self, maze_ui):
        self.maze_ui = maze_ui
        self.solution_manager = pygame_gui.UIManager((self.maze_ui.game_window.screen_width, self.maze_ui.game_window.screen_height), self.maze_ui.game_window.theme_file)
        self.line_thickness = round((self.maze_ui.cell_width - self.maze_ui.wall_thickness)*0.25)
        if self.line_thickness < 2: self.line_thickness = 2
        self.current_line = None
        self.increment = 1
        self.index = 0
        self.current_line_target_width = None
        self.current_line_target_height = None
        self.current_direction = None

    def set_current_direction(self):
        col_direction = self.maze_ui.solution[self.index+1][1] - self.maze_ui.solution[self.index][1]
        row_direction = self.maze_ui.solution[self.index+1][0] - self.maze_ui.solution[self.index][0]
        self.current_direction = (row_direction, col_direction)

    def draw(self):
        if self.current_line is None:
            cell_ui_position = self.maze_ui.get_cell_ui_position(self.maze_ui.solution[self.index])
            self.set_current_direction()
            # horizontal
            if self.current_direction[0] == 0:
                if self.current_direction[1] < 0:
                    adjustment = self.increment
                else:
                    adjustment = 0
                self.current_line_target_width = self.maze_ui.cell_width + self.line_thickness
                self.current_line_target_height = self.line_thickness
                line_rect = pygame.Rect(
                    # shift x position left by 1 if going left from current cell to next cell
                    cell_ui_position[0] + (self.maze_ui.cell_width - self.maze_ui.wall_thickness - self.line_thickness)/2 - adjustment,
                    cell_ui_position[1] + (self.maze_ui.cell_height - self.maze_ui.wall_thickness - self.line_thickness)/2,
                    self.line_thickness + adjustment,
                    self.line_thickness
                )

            # vertical
            else:
                if self.current_direction[0] < 0:
                    adjustment = self.increment
                else:
                    adjustment = 0
                self.current_line_target_width = self.line_thickness
                self.current_line_target_height = self.maze_ui.cell_height + self.line_thickness
                line_rect = pygame.Rect(
                    cell_ui_position[0] + (self.maze_ui.cell_width - self.maze_ui.wall_thickness - self.line_thickness)/2,
                    # shift y position up by 1 if going up from current cell to next cell
                    cell_ui_position[1] + (self.maze_ui.cell_height - self.maze_ui.wall_thickness - self.line_thickness)/2 - adjustment,
                    self.line_thickness,
                    self.line_thickness + adjustment
                )

            self.current_line = pygame_gui.elements.UIPanel(
                relative_rect=line_rect,
                manager=self.solution_manager,
                object_id=ObjectID(object_id="#solution-path")
            )
        else:
            # going right
            if self.current_direction[1] > 0:
                self.current_line.set_dimensions((self.current_line.get_relative_rect().width + self.increment, self.current_line.get_relative_rect().height))

            # going left
            elif self.current_direction[1] < 0:
                left = self.current_line.get_relative_rect().left
                self.current_line.set_dimensions((self.current_line.get_relative_rect().width + self.increment, self.current_line.get_relative_rect().height))
                self.current_line.set_relative_position((left - self.increment, self.current_line.get_relative_rect().top))

            # going down
            elif self.current_direction[0] > 0:
                self.current_line.set_dimensions((self.current_line.get_relative_rect().width, self.current_line.get_relative_rect().height + self.increment))

            # going up
            elif self.current_direction[0] < 0:
                top = self.current_line.relative_rect.top
                self.current_line.set_dimensions((self.current_line.get_relative_rect().width, self.current_line.get_relative_rect().height + self.increment))
                self.current_line.set_relative_position((self.current_line.get_relative_rect().left, top - self.increment))
            
            if (self.current_line.get_relative_rect().width >= self.current_line_target_width) and (self.current_line.get_relative_rect().height >= self.current_line_target_height):
                self.current_line.set_dimensions((self.current_line_target_width, self.current_line_target_height))
                self.index += 1
                self.current_line = None
                if self.index == len(self.maze_ui.solution) - 1:
                    return True
        return False

    def reset(self):
        self.solution_manager.clear_and_reset()
        self.index = 0
        self.current_line = None
        self.current_line_target_width = None
        self.current_line_target_height = None
        self.current_direction = None