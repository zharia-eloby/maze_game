import random, pygame, pygame_gui
from pygame_gui.core import ObjectID

class Cell:
    def __init__(self, row_index, col_index):
        self.row_index = row_index
        self.col_index = col_index
        self.walls = { "left": True, "right": True, "up": True, "down": True }
        self.visited = False
        self.rect = None

    """
    for debugging purposes
    prints the cell as a box, i.e. |_|
    """
    def __str__(self):
        cell_str = ""
        if self.walls["left"]: cell_str += '|'
        else: cell_str += ' '
        if self.walls["down"]: cell_str += '_' 
        else: cell_str += ' '
        if self.walls["right"]: cell_str += '|'
        else: cell_str += ' '
        return cell_str

    """
    return walls where key value is True
    """
    def get_blocked_walls(self):
        blocked_walls = []
        for i in list(self.walls):
            if self.walls[i]: blocked_walls += [i]
        return blocked_walls
    
    """
    return walls where key value is False
    """
    def get_open_walls(self):
        open_walls = []
        for i in list(self.walls):
            if not self.walls[i]: open_walls += [i]
        return open_walls
        
class Maze:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.maze = [ [ Cell(j, i) for i in range(dimensions[1]) ] for j in range(dimensions[0]) ]
        self.startpoint = None
        self.endpoint = None
        self.solution = []

    def __str__(self, pretty_print):
        if pretty_print:
            row_str = ""
            for row in self.maze:
                for cell in row:
                    row_str += cell.__str__()
                print(row_str)
                row_str = ""
        else:
            for row in self.maze:
                print("[")
                for cell in row:
                    print(cell.walls)
                print("]")

    def update_maze_size(self, new_dimensions):
        self.dimensions = new_dimensions
        self.maze = [ [ Cell(j, i) for i in range(self.dimensions[1]) ] for j in range(self.dimensions[0]) ]

    def get_direction_from_cell_to_neighbor(self, from_cell, to_cell):
        if from_cell.row_index == to_cell.row_index:
            if from_cell.col_index > to_cell.col_index: return "left"
            else: return "right"

        if from_cell.row_index > to_cell.row_index: return "up"
        else: return "down"

    def get_opposite_direction(self, direction):
        if direction == "left": return "right"
        elif direction == "right": return "left"
        elif direction == "up": return "down"
        elif direction == "down": return "up"
        
    def get_neighbor_cell(self, cell, direction):
        if direction == "left":
            return self.maze[cell.row_index][cell.col_index - 1]
        elif direction == "right":
            return self.maze[cell.row_index][cell.col_index + 1]
        elif direction == "up":
            return self.maze[cell.row_index - 1][cell.col_index]
        elif direction == "down":
            return self.maze[cell.row_index + 1][cell.col_index]

    def get_unvisited_neighbors(self, cell, for_open_paths_only):
        unvisited_neighbors = []

        if for_open_paths_only: available_directions = cell.get_open_walls()
        else:
            available_directions = []
            if cell.row_index > 0: available_directions += ["up"]
            if cell.row_index < self.dimensions[0] - 1: available_directions += ["down"]
            if cell.col_index > 0: available_directions += ["left"]
            if cell.col_index < self.dimensions[1] - 1: available_directions += ["right"]

        for i in available_directions:
            neighbor = self.get_neighbor_cell(cell, i)
            if not neighbor.visited: unvisited_neighbors += [neighbor]

        return unvisited_neighbors
    
    def set_startpoint_endpoint(self):
        max_rows = self.dimensions[0]
        max_cols = self.dimensions[1]
        self.startpoint = self.maze[random.randint(0, max_rows-1)][random.randint(0, max_cols-1)]
        self.endpoint = self.maze[random.randint(0, max_rows-1)][random.randint(0, max_cols-1)]
        while self.startpoint == self.endpoint:
            self.endpoint = self.maze[random.randint(0, max_rows-1)][random.randint(0, max_cols-1)]

    def reset_visited(self):
        for row in self.maze:
            for cell in row:
                cell.visited = False

    def remove_wall_between_cells(self, cell, neighbor):
        direction_to_neighbor = self.get_direction_from_cell_to_neighbor(cell, neighbor)
        cell.walls[direction_to_neighbor] = False

        direction_to_cell = self.get_opposite_direction(direction_to_neighbor)
        neighbor.walls[direction_to_cell] = False

    def create_maze(self):
        stack = []
        start_row = random.randint(0, self.dimensions[0]-1)
        start_col = random.randint(0, self.dimensions[1]-1)

        current_cell = self.maze[start_row][start_col]
        stack.append(current_cell)
        current_cell.visited = True
        while len(stack) > 0:
            unvisited_neighbors = self.get_unvisited_neighbors(current_cell, False)

            if len(unvisited_neighbors) > 0:
                neighbor = random.choice(unvisited_neighbors)
                self.remove_wall_between_cells(current_cell, neighbor)

                current_cell = neighbor
                current_cell.visited = True
                stack.append(current_cell)
            else:
                current_cell = stack.pop()

        self.set_startpoint_endpoint()
        self.reset_visited()

    """
    solves the maze by picking a random path and backtracking until the end is found
    """
    def solve_maze(self):
        self.solution = [self.startpoint]
        current_cell = self.startpoint

        current_cell.visited = True

        while (current_cell != self.endpoint):
            open_unvisited_neighbors = self.get_unvisited_neighbors(current_cell, True)

            # if all neighbors have been visited, pop from the stack until there is an available neighbor
            while not open_unvisited_neighbors:
                self.solution.pop()
                current_cell = self.solution[-1]
                open_unvisited_neighbors = self.get_unvisited_neighbors(current_cell, True)

            current_cell = random.choice(open_unvisited_neighbors)
            
            self.solution += [current_cell]
            current_cell.visited = True

class MazeUI(Maze):
    def __init__(self, dimensions, settings):
        super().__init__(dimensions)
        self.settings = settings
        self.cell_width = None
        self.cell_height = None
        self.wall_thickness = None
        self.maze_area_rect = pygame.Rect()
        self.player = None
        self.maze_background_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme.theme_file)
        self.maze_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme.theme_file)

    """
    sets the measurements for the maze's ui elements (wall size, maze width/height, cell width/height)
    """
    def set_ui_element_sizes(self, ui_area):
        if ui_area.width > ui_area.height:
            maze_height = ui_area.height
        else:
            maze_height = ui_area.width
        maze_width = maze_height
        
        self.cell_width = round(maze_width/self.dimensions[1])
        self.cell_width -= self.cell_width%2
        self.cell_height = round(maze_height/self.dimensions[0])
        self.cell_height -= self.cell_height%2

        if self.cell_width < self.cell_height: 
            self.wall_thickness = round(self.cell_width/10) 
        else: 
            self.wall_thickness = round(self.cell_height/10)
        self.wall_thickness -= self.wall_thickness%2
        if self.wall_thickness < 2: self.wall_thickness = 2

        # maze width & height may be slightly different. reset them to the actual width & height
        maze_width = self.cell_width * self.dimensions[1] + self.wall_thickness
        maze_height = self.cell_height * self.dimensions[0] + self.wall_thickness

        # set rect so the maze is horizontally centered and bottom-aligned
        self.maze_area_rect.width = maze_width
        self.maze_area_rect.height = maze_height
        self.maze_area_rect.bottom = ui_area.bottom
        self.maze_area_rect.centerx = ui_area.centerx
    
    """
    creates the ui elements to draw the walls of the maze
    to avoid duplicates, it will only draw the "right" and "down" walls unless the cell is in the 1st row and/or 1st column
    """
    def draw_walls(self, cell):
        cell.rect = pygame.Rect(
            self.maze_area_rect.left + (cell.col_index * self.cell_width),
            self.maze_area_rect.top + (cell.row_index * self.cell_height),
            self.cell_width,
            self.cell_height
        )

        # draw top wall
        if cell.row_index == 0:
            wall_rect = pygame.Rect(
                cell.rect.left,
                cell.rect.top,
                self.cell_width + self.wall_thickness,
                self.wall_thickness
            )
            pygame_gui.elements.UIPanel(
                relative_rect=wall_rect,
                manager=self.maze_manager,
                object_id=ObjectID(class_id="@wall")
            )

        # draw left wall
        if cell.col_index == 0:
            wall_rect = pygame.Rect(
                cell.rect.left,
                cell.rect.top,
                self.wall_thickness,
                self.cell_height + self.wall_thickness
            )
            pygame_gui.elements.UIPanel(
                relative_rect=wall_rect,
                manager=self.maze_manager,
                object_id=ObjectID(class_id="@wall")
            )

        # draw right wall
        if cell.walls["right"]:
            wall_rect = pygame.Rect(
                cell.rect.right,
                cell.rect.top,
                self.wall_thickness,
                self.cell_height + self.wall_thickness
            )
            pygame_gui.elements.UIPanel(
                relative_rect=wall_rect,
                manager=self.maze_manager,
                object_id=ObjectID(class_id="@wall")
            )

        # draw bottom wall
        if cell.walls["down"]:
            wall_rect = pygame.Rect(
                cell.rect.left,
                cell.rect.bottom,
                self.cell_width + self.wall_thickness,
                self.wall_thickness
            )
            pygame_gui.elements.UIPanel(
                relative_rect=wall_rect,
                manager=self.maze_manager,
                object_id=ObjectID(class_id="@wall")
            )
        
    def draw_maze(self):
        pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(self.maze_area_rect.left, self.maze_area_rect.top, self.maze_area_rect.width, self.maze_area_rect.height),
            manager=self.maze_background_manager,
            object_id=ObjectID(object_id="#maze-background")
        )

        for row in self.maze:
            for cell in row:
                self.draw_walls(cell)
    
    def set_maze_ui(self, maze_area): 
        self.create_maze()
        self.player_position = self.startpoint
        self.set_ui_element_sizes(maze_area)
        self.draw_maze()

        start_rect = pygame.Rect(
            self.startpoint.rect.left + self.wall_thickness,
            self.startpoint.rect.top + self.wall_thickness,
            self.cell_width - self.wall_thickness,
            self.cell_height - self.wall_thickness
        )
        pygame_gui.elements.UIPanel(
            relative_rect=start_rect,
            manager=self.maze_manager,
            object_id=ObjectID(object_id="#startpoint")
        )

        end_rect = pygame.Rect(
            self.endpoint.rect.left + self.wall_thickness,
            self.endpoint.rect.top + self.wall_thickness,
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

        player_rect = pygame.Rect()
        player_rect.width = player_width
        player_rect.height = player_height
        player_rect.center = (
            self.startpoint.rect.centerx + self.wall_thickness/2,
            self.startpoint.rect.centery + self.wall_thickness/2
        )
        self.player = pygame_gui.elements.UIPanel(
            relative_rect=player_rect,
            manager=self.maze_manager,
            object_id=ObjectID(object_id="#player")
        )

    def move_player(self, direction):
        if not self.player_position.walls[direction]: # if cell does not have a wall in the desired direction
            neighbor_cell = self.get_neighbor_cell(self.player_position, direction)
            self.player.relative_rect.center = (
                neighbor_cell.rect.centerx + self.wall_thickness/2,
                neighbor_cell.rect.centery + self.wall_thickness/2
            )
            self.player.set_relative_position(self.player.relative_rect.topleft)
            self.player_position = neighbor_cell
    
    def reset(self):
        self.maze = []
        self.cell_width = None
        self.cell_height = None
        self.wall_thickness = None
        self.startpoint = None
        self.endpoint = None
        self.maze_area_rect = pygame.Rect()
        self.player = None
        self.player_position = None
        self.solution = []
        self.maze_manager.clear_and_reset()

class LineSolutionUI():
    def __init__(self, maze_ui):
        self.maze_ui = maze_ui
        self.solution_manager = pygame_gui.UIManager((self.maze_ui.settings.screen_width, self.maze_ui.settings.screen_height), self.maze_ui.settings.theme.theme_file)
        self.increment = 1
        self.index = 0
        self.current_line = None
        self.current_line_target_width = None
        self.current_line_target_height = None
        self.current_direction = None

        percent_thickness = 0.1
        self.line_width_thickness = round((self.maze_ui.cell_width - self.maze_ui.wall_thickness)*percent_thickness)
        self.line_width_thickness -= self.line_width_thickness%2
        self.line_height_thickness = round((self.maze_ui.cell_height - self.maze_ui.wall_thickness)*percent_thickness)
        self.line_height_thickness -= self.line_height_thickness%2
        if self.line_width_thickness < 2: self.line_width_thickness = 2
        if self.line_height_thickness < 2: self.line_height_thickness = 2

    def draw_next_segment(self, draw_full, current_cell, next_cell):
        self.current_direction = self.maze_ui.get_direction_from_cell_to_neighbor(current_cell, next_cell)
        if self.current_direction == "down":
            line_rect = pygame.Rect()
            line_rect.left = current_cell.rect.centerx + self.maze_ui.wall_thickness/2 - self.line_width_thickness/2
            line_rect.top = current_cell.rect.centery + self.maze_ui.wall_thickness/2 - self.line_height_thickness/2
            line_rect.width = self.line_width_thickness

            if draw_full:
                line_rect.height = self.maze_ui.cell_height + self.line_height_thickness
            else:
                line_rect.height = self.line_height_thickness
                self.current_line_target_width = self.line_width_thickness
                self.current_line_target_height = self.maze_ui.cell_height + self.line_height_thickness
        
        elif self.current_direction == "up":
            line_rect = pygame.Rect()
            line_rect.width = self.line_width_thickness

            if draw_full:
                line_rect.left = next_cell.rect.centerx + self.maze_ui.wall_thickness/2 - self.line_width_thickness/2
                line_rect.top = next_cell.rect.centery + self.maze_ui.wall_thickness/2 - self.line_height_thickness/2
                line_rect.height = self.maze_ui.cell_height + self.line_height_thickness
            else:
                line_rect.left = current_cell.rect.centerx + self.maze_ui.wall_thickness/2 - self.line_width_thickness/2
                line_rect.top = current_cell.rect.centery + self.maze_ui.wall_thickness/2 - self.line_height_thickness/2
                line_rect.height = self.line_height_thickness
                self.current_line_target_width = self.line_width_thickness
                self.current_line_target_height = self.maze_ui.cell_height + self.line_height_thickness
        
        elif self.current_direction == "left":
            line_rect = pygame.Rect()
            line_rect.height = self.line_height_thickness
            
            if draw_full:
                line_rect.left = next_cell.rect.centerx + self.maze_ui.wall_thickness/2 - self.line_width_thickness/2
                line_rect.top = next_cell.rect.centery + self.maze_ui.wall_thickness/2 - self.line_height_thickness/2
                line_rect.width = self.maze_ui.cell_width + self.line_width_thickness
            else:
                line_rect.left = current_cell.rect.centerx + self.maze_ui.wall_thickness/2 - self.line_width_thickness/2
                line_rect.top = current_cell.rect.centery + self.maze_ui.wall_thickness/2 - self.line_height_thickness/2
                line_rect.width = self.line_width_thickness
                self.current_line_target_width = self.maze_ui.cell_width + self.line_width_thickness
                self.current_line_target_height = self.line_height_thickness
        
        elif self.current_direction == "right":
            line_rect = pygame.Rect()
            line_rect.left = current_cell.rect.centerx + self.maze_ui.wall_thickness/2 - self.line_width_thickness/2
            line_rect.top = current_cell.rect.centery + self.maze_ui.wall_thickness/2 - self.line_height_thickness/2
            line_rect.height = self.line_height_thickness

            if draw_full:
                line_rect.width = self.maze_ui.cell_width + self.line_width_thickness
            else:
                line_rect.width = self.line_width_thickness
                self.current_line_target_width = self.maze_ui.cell_width + self.line_width_thickness
                self.current_line_target_height = self.line_height_thickness

        self.current_line = pygame_gui.elements.UIPanel(
            relative_rect=line_rect,
            manager=self.solution_manager,
            object_id=ObjectID(object_id="#solution-path")
        )

    """
    draw the solution path segment by segment
    returns True when the entire solution path has been drawn
    """  
    def animate(self):
        if not self.current_line:
            # check that we haven't already reached the end. faster solution speeds may call the method when the solution has already finished drawing, resulting in an IndexError
            if self.index > len(self.maze_ui.solution) - 2: return True
            
            current_cell = self.maze_ui.solution[self.index]
            next_cell = self.maze_ui.solution[self.index + 1]
            self.draw_next_segment(False, current_cell, next_cell)
            return False
        
        # increment current line dimensions
        current_width = self.current_line.get_relative_rect().width
        current_height = self.current_line.get_relative_rect().height
        if self.current_direction == "down":
            self.current_line.set_dimensions((current_width, current_height + self.increment))
        elif self.current_direction == "right":
            self.current_line.set_dimensions((current_width + self.increment, current_height))
        elif self.current_direction == "left":
            self.current_line.set_relative_position((self.current_line.relative_rect.left - self.increment, self.current_line.relative_rect.top))
            self.current_line.set_dimensions((current_width + self.increment, current_height))
        elif self.current_direction == "up":
            self.current_line.set_relative_position((self.current_line.relative_rect.left, self.current_line.relative_rect.top - self.increment))
            self.current_line.set_dimensions((current_width, current_height + self.increment))

        # check if animation for entire solution path is done
        if (self.current_line.get_relative_rect().width >= self.current_line_target_width) and (self.current_line.get_relative_rect().height >= self.current_line_target_height):
            self.current_line.set_dimensions((self.current_line_target_width, self.current_line_target_height))
            self.index += 1
            self.current_line = None
            if self.index == len(self.maze_ui.solution) - 1: return True
            
        return False

    """
    draw the solution path entirely
    """  
    def draw_complete_path(self):
        # check that we haven't already reached the end. faster solution speeds may call the method when the solution has already finished drawing, resulting in an IndexError
        if self.index > len(self.maze_ui.solution) - 2: return

        if self.current_line:
            if self.current_direction == "right" or self.current_direction == "down":
                self.current_line.set_dimensions((self.current_line_target_width, self.current_line_target_height))
            elif self.current_direction == "left":
                previous_width = self.current_line.get_relative_rect().width
                self.current_line.set_dimensions((self.current_line_target_width, self.current_line_target_height))
                self.current_line.set_relative_position((self.current_line.relative_rect.left - (self.current_line.relative_rect.width - previous_width), self.current_line.relative_rect.top))
            elif self.current_direction == "up":
                previous_height = self.current_line.get_relative_rect().height
                self.current_line.set_dimensions((self.current_line_target_width, self.current_line_target_height))
                self.current_line.set_relative_position((self.current_line.relative_rect.left, self.current_line.relative_rect.top - (self.current_line.relative_rect.height - previous_height)))
            
        self.index += 1
            
        for i in range(self.index, len(self.maze_ui.solution)-1):
            current_cell = self.maze_ui.solution[i]
            next_cell = self.maze_ui.solution[i + 1]
            self.draw_next_segment(True, current_cell, next_cell)
    
    def reset(self):
        self.solution_manager.clear_and_reset()
        self.index = 0
        self.current_line = None
        self.current_line_target_width = None
        self.current_line_target_height = None
        self.current_direction = None
        