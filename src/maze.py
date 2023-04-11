"""
Zharia Eloby
Maze Game with Pygame
"""

import pygame
import pygame_gui
from pygame_gui.core import ObjectID
import random
import math
import sys
import os
import time

black = (0, 0, 0)
white = (255, 255, 255)
gray = (230, 230, 230)
blue = (52, 118, 168)
green = (56, 220, 156)
tan = (234, 203, 187)

background_color = tan
wall_color = black
player_color = blue
startpoint_color = gray
endpoint_color = green
solution_color = white

#value may be 'rectangle' 'line' or 'circle'
solution_image = "line"

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750

MAZE_WIDTH = 600
MAZE_HEIGHT = 600

src_path = sys.path[0]
font_file = os.path.join(src_path, "./assets/fonts/Roboto-Regular.ttf")
image_file_path = os.path.join(src_path, "./assets/images/")
theme_file = os.path.join(src_path, "./assets/themes/default_theme.json")

maze_startpoint = (0, 75)

CELL_WIDTH = 0
CELL_HEIGHT = 0
WALL_THICKNESS = 0

rows = 0
columns = 0

easy_dim = (10, 10)
medium_dim = (20, 20)
hard_dim = (30, 30)

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Maze - created by Zharia Eloby")

manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)
background_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)

background_rect = pygame.Rect(
    0,
    0,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)
background = pygame_gui.elements.UIPanel(
    relative_rect=background_rect,
    manager=background_manager,
    object_id=ObjectID(object_id="#background")
)
background_manager.update(0)
background_manager.draw_ui(screen)

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([CELL_WIDTH-WALL_THICKNESS*2, CELL_HEIGHT-WALL_THICKNESS*2])
        self.image.fill(white)
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect(center=(x, y))
        
        #cell width may differ from cell height -> make the diameter of the player object that of the lesser value between 
        #   CELL_HEIGHT and CELL_WIDTH so the player image doesn't overlap the walls of the maze
        pygame.draw.circle(self.image, color, (self.rect.width/2, self.rect.height/2), min((CELL_HEIGHT - WALL_THICKNESS)/3, (CELL_WIDTH - WALL_THICKNESS)/3))

    """
    update() called to move the player
    x_direction and y_direction will always be -1, 0, or 1 with one of the values being 0 and the other being either 1 or -1
    Returns True if the player successfully moved to the desired cell, False otherwise
    """
    def update(self, x_direction, y_direction, wall_list):
        #moves the player in the desired direction halfway to it's destination
        if (x_direction != 0):
            move_factor = CELL_WIDTH/2
            self.rect.centerx += move_factor*x_direction
        else:
            move_factor = CELL_HEIGHT/2
            self.rect.centery += move_factor*y_direction
        
        #is it on a wall?
        if pygame.sprite.spritecollideany(self, wall_list) == None: #if no, move the player completely to the desired cell
            self.rect = self.rect.move(move_factor*x_direction, move_factor*y_direction)
            return True
        else:   #if yes, move the player back to where they were
            self.rect = self.rect.move(move_factor*x_direction*-1, move_factor*y_direction*-1)
            return False
"""
used to represent the starting spot, ending spot, and cells in the solution path of the maze
type - file path string, 'rectangle', or 'circle'
"""
class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, color, type):
        pygame.sprite.Sprite.__init__(self)
        if type == "rectangle":
            self.image = pygame.Surface([CELL_WIDTH-WALL_THICKNESS, CELL_HEIGHT-WALL_THICKNESS])
            self.image.fill(color)
            self.rect = self.image.get_rect(topleft=(x, y))
        elif type == "circle":
            self.image = pygame.Surface([CELL_WIDTH-WALL_THICKNESS, CELL_HEIGHT-WALL_THICKNESS])
            self.image.fill(background_color)
            self.image.set_colorkey(background_color)
            self.rect = self.image.get_rect(topleft=(x, y))
            if (CELL_WIDTH > CELL_HEIGHT):
                radius = math.ceil(CELL_HEIGHT/8)
            else:
                radius = math.ceil(CELL_WIDTH/8)
            pygame.draw.circle(self.image, color, (self.rect.width/2, self.rect.height/2), radius)
        elif type == "line":
            self.image = pygame.Surface([CELL_WIDTH, CELL_HEIGHT])
            self.image.fill(background_color)
            self.image.set_colorkey(background_color)
            self.rect = self.image.get_rect(topleft=(x - WALL_THICKNESS, y - WALL_THICKNESS))
            self.color = color

    def draw_lines(self, prev_cell, curr_cell, next_cell):
        points = []
        if prev_cell[0] < curr_cell[0]:     #prev_cell is above curr_cell
            points += [(self.rect.width/2, 0)]
        elif prev_cell[0] > curr_cell[0]:   #prev_cell is below curr_cell
            points += [(self.rect.width/2, self.rect.height)]
        elif prev_cell[1] < curr_cell[1]:   #prev_cell is to the left of curr_cell
            points += [(0, self.rect.height/2)]
        else:                               #prev_cell is to the right of curr_cell
            points += [(self.rect.width, self.rect.height/2)]
            
        points += [(self.rect.width/2, self.rect.height/2)]
        
        if next_cell[0] < curr_cell[0]:     #next_cell is above curr_cell
            points += [(self.rect.width/2, 0)]
        elif next_cell[0] > curr_cell[0]:   #next_cell is below curr_cell
            points += [(self.rect.width/2, self.rect.height)]
        elif next_cell[1] < curr_cell[1]:   #next_cell is to the left of curr_cell
            points += [(0, self.rect.height/2)]
        else:                               #next_cell is to the right of curr_cell
            points += [(self.rect.width, self.rect.height/2)]
            
        pygame.draw.lines(self.image, self.color, False, points, 2)


"""
type - either 'v' (vertical wall) or 'h' (horizontal wall)
"""
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(wall_color)
        
        if (type == 'v'):
            self.rect = self.image.get_rect(midtop=(x, y))
        else:
            self.rect = self.image.get_rect(midleft=(x, y))

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file_path + "red-flag.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (math.floor(CELL_WIDTH * 0.75), math.floor(CELL_HEIGHT * 0.75)))
        self.rect = self.image.get_rect(center=(x, y))
    
    def is_clicked(self, m_pos):
        return self.rect.collidepoint(m_pos)

"""
only used when creating the maze. returns a list of unvisited neighbors
"""
def check_neighbors(maze, num_rows, num_cols, curr_row, curr_col):
    available_neighbors = []
    if (curr_col > 1):               #has a left neighbor
        if (maze[curr_row][curr_col-2] != 'v'):
            available_neighbors += [(curr_row, curr_col-2)]
            
    if (curr_col < num_rows*2 - 2):         #has right neighbor
        if (maze[curr_row][curr_col+2] != 'v'):
            available_neighbors += [(curr_row, curr_col+2)]
            
    if (curr_row > 1):               #has upper neighbor
        if (maze[curr_row-2][curr_col] != 'v'):
            available_neighbors += [(curr_row-2, curr_col)]
            
    if (curr_row < num_cols*2 - 2):         #has below neighbor
        if (maze[curr_row+2][curr_col] != 'v'):
            available_neighbors += [(curr_row+2, curr_col)]
            
    return available_neighbors

"""
creates a maze of the specified dimensions using the backtracking algorithm
"""
def create_maze(num_rows, num_cols):
    #create grid. erase walls as maze is created
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
    
    cells_to_go = (num_rows*num_cols)-1 #when this gets to 0, it's done
    
    stack = []
    stack.append((1,1))
    maze[1][1] = 'v'
    
    while (cells_to_go > 0):
        curr_cell = stack.pop()
        stack.append(curr_cell)
        
        neighbors = check_neighbors(maze, num_cols, num_rows, curr_cell[0], curr_cell[1])
        
        if (len(neighbors) > 0):
            chosen = random.choice(neighbors)
            
            # remove the wall in between the current cell and its chosen neighbor
            if (chosen[0] == curr_cell[0]):         #same row
                if (chosen[1] > curr_cell[1]):      #neighbor is on the right
                    maze[curr_cell[0]][curr_cell[1]+1] = 'o'
                else:
                    maze[curr_cell[0]][curr_cell[1]-1] = 'o'
                    
            else:                                   #same column
                if (chosen[0] > curr_cell[0]):      #neighbor is below
                    maze[curr_cell[0]+1][curr_cell[1]] = 'o'
                else:
                    maze[curr_cell[0]-1][curr_cell[1]] = 'o'
            maze[chosen[0]][chosen[1]] = 'v'
            cells_to_go -= 1
            if (cells_to_go == 0):
                global endpoint
                endpoint = ((chosen[0]-1)/2, (chosen[1]-1)/2)
            stack.append(chosen)
            
        else:
            stack.pop()

    return maze

"""
only used for solving a maze. checks available paths for the current cell
"""
def check_paths(maze, curr_cell):
    available_paths = []
    if (maze[curr_cell[0]+1][curr_cell[1]] != 'w' and maze[curr_cell[0]+2][curr_cell[1]] != 'x'):
        available_paths += [(curr_cell[0]+2, curr_cell[1])]
    if (maze[curr_cell[0]-1][curr_cell[1]] != 'w' and maze[curr_cell[0]-2][curr_cell[1]] != 'x'):
        available_paths += [(curr_cell[0]-2, curr_cell[1])]
    if (maze[curr_cell[0]][curr_cell[1]+1] != 'w' and maze[curr_cell[0]][curr_cell[1]+2] != 'x'):
        available_paths += [(curr_cell[0], curr_cell[1]+2)]
    if (maze[curr_cell[0]][curr_cell[1]-1] != 'w' and maze[curr_cell[0]][curr_cell[1]-2] != 'x'):
        available_paths += [(curr_cell[0], curr_cell[1]-2)]
    return available_paths

"""
solves the maze by picking a random path and backtracking until the end is found
"""
def solve_maze(maze, start, end):
    solution_path = [start]
    curr_cell = start
    maze[curr_cell[0]][curr_cell[1]] = 'x'  #mark the cell with 'x' in the maze array when visited
    available_paths = []
    while (curr_cell != end):
        available_paths = check_paths(maze, curr_cell)
        while not available_paths:
            solution_path.pop()
            curr_cell = solution_path[len(solution_path)-1]
            available_paths = check_paths(maze, curr_cell)
        curr_cell = random.choice(available_paths)
        solution_path += [curr_cell]
        maze[curr_cell[0]][curr_cell[1]] = 'x'
    return solution_path
    
"""
home screen
- contains title, play button, and 'created by' text
"""
def title_screen():
    manager.clear_and_reset()
    background_manager.update(0)
    background_manager.draw_ui(screen)

    #play button
    button_width = SCREEN_WIDTH/2
    button_height = SCREEN_HEIGHT/8
    play_rect = pygame.Rect(
        SCREEN_WIDTH/2 - button_width/2,  # x
        SCREEN_HEIGHT/2,                  # y
        button_width,                   # width
        button_height                   # height
    )
    play_button = pygame_gui.elements.UIButton(
        relative_rect=play_rect, 
        text="play",
        object_id=ObjectID(class_id="@large-button")
    )
    
    #game title
    title_rect = pygame.Rect(0, 0, SCREEN_WIDTH, play_rect.top)
    title = pygame_gui.elements.UILabel(
        relative_rect=title_rect, 
        text="Maze",
        object_id=ObjectID(object_id="#title")
    )

    #credits
    credits_rect = pygame.Rect(0, play_rect.bottom, SCREEN_WIDTH, SCREEN_HEIGHT - play_rect.bottom)
    credits = pygame_gui.elements.UILabel(
        relative_rect=credits_rect, 
        text="code by Zharia Eloby",
        object_id=ObjectID(class_id="@small-text-bottom")
    )

    manager.update(0)
    manager.draw_ui(screen)
    pygame.display.flip()

    #until the user exits or presses the play button...
    time_delta = math.floor(time.time()) # time of last call to update
    while True:
        for event in [pygame.event.wait()]+pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
                    pick_size_screen()

            elif event.type == pygame.WINDOWRESTORED:   #redraw window upon reopening after minimizing
                pygame.display.flip()

            manager.process_events(event)

        time_delta = math.floor(time.time()) - time_delta
        background_manager.update(time_delta)
        background_manager.draw_ui(screen)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

"""
the user can pick the size of their maze
preset sizes are easy, medium, and hard, or they can customize the size
"""
def pick_size_screen():
    manager.clear_and_reset()

    #back button
    back_button_rect = pygame.Rect(
        25, # x
        25, # y
        50, # width
        35  # height
    )
    back_button = pygame_gui.elements.UIButton(
        relative_rect=back_button_rect, 
        text="<",
        manager=manager,
        object_id=ObjectID(class_id="@small-button")
    )
    
    button_width = SCREEN_WIDTH/2
    button_height = 100
    space_between_buttons = 30
    
    num_buttons = 4
    total_buttons_height = num_buttons*button_height + (num_buttons-1)*space_between_buttons
    starting_y_pos = (SCREEN_HEIGHT - total_buttons_height)/2
    
    #easy button
    easy_button_rect = pygame.Rect(
        SCREEN_WIDTH/2 - button_width/2,  # x
        starting_y_pos,                 # y
        button_width,                   # width
        button_height                   # height
    )
    easy_button = pygame_gui.elements.UIButton(
        relative_rect=easy_button_rect, 
        text="easy",
        manager=manager,
        object_id=ObjectID(class_id="@large-button")
    )
    
    #medium button
    medium_button_rect = pygame.Rect(
        SCREEN_WIDTH/2 - button_width/2,  # x
        easy_button_rect.bottom + space_between_buttons,    # y
        button_width,                   # width
        button_height                   # height
    )
    medium_button = pygame_gui.elements.UIButton(
        relative_rect=medium_button_rect, 
        text="medium",
        manager=manager,
        object_id=ObjectID(class_id="@large-button")
    )
    
    #hard button
    hard_button_rect = pygame.Rect(
        SCREEN_WIDTH/2 - button_width/2,  # x
        medium_button_rect.bottom + space_between_buttons,  # y
        button_width,                   # width
        button_height                   # height
    )
    hard_button = pygame_gui.elements.UIButton(
        relative_rect=hard_button_rect, 
        text="hard",
        manager=manager,
        object_id=ObjectID(class_id="@large-button")
    )

    #custom button
    custom_button_rect = pygame.Rect(
        SCREEN_WIDTH/2 - button_width/2,  # x
        hard_button_rect.bottom + space_between_buttons,  # y
        button_width,                   # width
        button_height                   # height
    )
    custom_button = pygame_gui.elements.UIButton(
        relative_rect=custom_button_rect, 
        text="custom",
        manager=manager,
        object_id=ObjectID(class_id="@large-button")
    )

    manager.update(0)
    background_manager.update(0)
    background_manager.draw_ui(screen)
    manager.draw_ui(screen)
    pygame.display.flip()
    
    global rows
    global columns

    ready = False
    time_delta = math.floor(time.time())
    while not ready:
        for event in [pygame.event.wait()]+pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    title_screen()
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == easy_button:
                    ready = True
                    rows = easy_dim[0]
                    columns = easy_dim[1]
                    play()
                elif event.ui_element == medium_button:
                    ready = True
                    rows = medium_dim[0]
                    columns = medium_dim[1]
                    play()
                elif event.ui_element == hard_button:
                    ready = True
                    rows = hard_dim[0]
                    columns = hard_dim[1]
                    play()
                elif event.ui_element == custom_button:
                    ready = True
                    custom_size_screen()
                elif event.ui_element == back_button:
                    title_screen()
            elif event.type == pygame.WINDOWRESTORED: #redraw window upon reopening after minimizing
                pygame.display.flip()

            manager.process_events(event)
        
        time_delta = math.floor(time.time()) - time_delta
        manager.update(time_delta)

        background_manager.update(time_delta)
        background_manager.draw_ui(screen)
        manager.draw_ui(screen)
        pygame.display.update()

def custom_size_screen():
    manager.clear_and_reset()

    global rows
    global columns
    global CELL_WIDTH
    global CELL_HEIGHT
    global WALL_THICKNESS
    
    rows = 15
    columns = 15
    
    background_manager.update(0)
    background_manager.draw_ui(screen)
    
    #back button
    back_button_rect = pygame.Rect(
        25, # x
        25, # y
        50, # width
        35  # height
    )
    back_button = pygame_gui.elements.UIButton(
        relative_rect=back_button_rect, 
        text="<",
        manager=manager,
        object_id=ObjectID(class_id="@small-button")
    )
    
    #select dimensions text
    select_text_rect = pygame.Rect(
        0,
        back_button_rect.bottom,
        SCREEN_WIDTH,
        70
    )
    select_text = pygame_gui.elements.UILabel(
        relative_rect=select_text_rect,
        text="Select your Dimensions",
        manager=manager,
        object_id=ObjectID(class_id="@heading")
    )

    # warning text
    warning_text_width = SCREEN_WIDTH
    warning_text_height = 20
    warning_text_rect = pygame.Rect(
        0,
        select_text_rect.bottom,
        warning_text_width,
        warning_text_height
    )
    warning_text = pygame_gui.elements.UILabel(
        relative_rect=warning_text_rect,
        text="* dimensions must be within 10 units of each other *",
        manager=manager,
        object_id=ObjectID(object_id="@small-text-center")
    )
    
    #'x' text
    x_width = SCREEN_WIDTH * 0.1
    x_height = 80
    x_text_rect = pygame.Rect(
        SCREEN_WIDTH/2 - x_width/2,
        SCREEN_HEIGHT/2 - x_height/2,
        x_width,
        x_height
    )
    x_text = pygame_gui.elements.UILabel(
        relative_rect=x_text_rect,
        text="x",
        manager=manager,
        object_id=ObjectID(class_id="@large-text-center")
    )
    
    #row text
    text_height = 100
    row_text_rect = pygame.Rect(
        0,
        SCREEN_HEIGHT/2 - text_height/2,
        x_text_rect.left,
        text_height
    )
    row_text = pygame_gui.elements.UILabel(
        relative_rect=row_text_rect,
        text=str(rows),
        manager=manager,
        object_id=ObjectID(class_id="@large-text-center")
    )

    #column text
    col_text_rect = pygame.Rect(
        x_text_rect.right,
        SCREEN_HEIGHT/2 - text_height/2,
        SCREEN_WIDTH - x_text_rect.right,
        text_height
    )
    col_text = pygame_gui.elements.UILabel(
        relative_rect=col_text_rect,
        text=str(columns),
        manager=manager,
        object_id=ObjectID(class_id="@large-text-center")
    )

    #arrows
    arrow_width = 75
    arrow_height = 75

    row_up_arrow_rect = pygame.Rect(
        row_text_rect.centerx - arrow_width/2,
        row_text_rect.top - arrow_height,
        arrow_width,
        arrow_height
    )
    row_up_arrow_button = pygame_gui.elements.UIButton(
        relative_rect=row_up_arrow_rect,
        text="",
        manager=manager,
        object_id=ObjectID(class_id="@large-button", object_id="#up-arrow")
    )

    row_down_arrow_rect = pygame.Rect(
        row_text_rect.centerx - arrow_width/2,
        row_text_rect.bottom,
        arrow_width,
        arrow_height
    )
    row_down_arrow_button = pygame_gui.elements.UIButton(
        relative_rect=row_down_arrow_rect,
        text="",
        manager=manager,
        object_id=ObjectID(class_id="@large-button", object_id="#down-arrow")
    )

    column_up_arrow_rect = pygame.Rect(
        col_text_rect.centerx - arrow_width/2,
        col_text_rect.top - arrow_height,
        arrow_width,
        arrow_height
    )
    column_up_arrow_button = pygame_gui.elements.UIButton(
        relative_rect=column_up_arrow_rect,
        text="",
        manager=manager,
        object_id=ObjectID(class_id="@large-button", object_id="#up-arrow")
    )

    column_down_arrow_rect = pygame.Rect(
        col_text_rect.centerx - arrow_width/2,
        col_text_rect.bottom,
        arrow_width,
        arrow_height
    )
    column_down_arrow_button = pygame_gui.elements.UIButton(
        relative_rect=column_down_arrow_rect,
        text="",
        manager=manager,
        object_id=ObjectID(class_id="@large-button", object_id="#down-arrow")
    )

    #ratio lock
    lock_button_width = 50
    lock_button_height = 50
    lock_button_rect = pygame.Rect(
        SCREEN_WIDTH/2 - lock_button_width/2,
        row_down_arrow_rect.bottom - lock_button_height,
        lock_button_width,
        lock_button_height
    )
    locked_button = pygame_gui.elements.UIButton(
        relative_rect=lock_button_rect,
        text="",
        manager=manager,
        object_id=ObjectID(class_id="@large-button", object_id="#locked-button")
    )
    unlocked_button = pygame_gui.elements.UIButton(
        relative_rect=lock_button_rect,
        text="",
        manager=manager,
        object_id=ObjectID(class_id="@large-button", object_id="#unlocked-button")
    )
    unlocked_button.hide()
    
    #play button
    button_width = SCREEN_WIDTH/2
    button_height = 50
    play_button_rect = pygame.Rect(
        SCREEN_WIDTH/2 - button_width/2, # x
        SCREEN_HEIGHT/5*4, # y
        button_width,   # width
        button_height   # height
    )
    play_button = pygame_gui.elements.UIButton(
        relative_rect=play_button_rect, 
        text="play",
        manager=manager,
        object_id=ObjectID(class_id="@large-button")
    )

    manager.update(0)
    manager.draw_ui(screen)
    
    pygame.display.flip()
    
    row_min = 5
    row_max = 50
    col_min = 5
    col_max = 50

    max_diff = 10

    ready = False
    locked = True #if True, rows and cols change simultaneously
    while not ready:
        time_delta = clock.tick(60)/1000.00
        for event in [pygame.event.wait()]+pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    title_screen()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_button:
                    pick_size_screen()
                elif (event.ui_element == locked_button) or (event.ui_element == unlocked_button):
                    if locked:
                        locked = False
                        locked_button.hide()
                        unlocked_button.show()
                    else:
                        locked = True
                        unlocked_button.hide()
                        locked_button.show()
                elif event.ui_element == play_button:
                    ready = True
                    play()
                    break
                if locked:
                    if (event.ui_element == row_up_arrow_button) or (event.ui_element == column_up_arrow_button):
                        if (rows < row_max and columns < col_max):
                            rows += 1
                            columns += 1
                            if (rows == row_max):
                                row_up_arrow_button.disable()
                            if (columns == col_max):
                                column_up_arrow_button.disable()
                            if not (row_down_arrow_button.is_enabled):
                                row_down_arrow_button.enable()
                            if not (column_down_arrow_button.is_enabled):
                                column_down_arrow_button.enable()
                    if (event.ui_element == row_down_arrow_button) or (event.ui_element == column_down_arrow_button):
                        if (rows > row_min and columns > col_min):
                            rows -= 1
                            columns -= 1
                            if (rows == row_min):
                                row_down_arrow_button.disable()
                            if (columns == col_min):
                                column_down_arrow_button.disable()
                            if not (row_up_arrow_button.is_enabled):
                                row_up_arrow_button.enable()
                            if not (column_up_arrow_button.is_enabled):
                                column_up_arrow_button.enable()
                else:
                    if (event.ui_element == row_up_arrow_button):
                        rows += 1
                        if (abs(rows-columns) > max_diff):
                            columns += 1
                            if not (column_down_arrow_button.is_enabled):
                                column_down_arrow_button.enable()
                        if (rows == row_max):
                            row_up_arrow_button.disable()
                        if not row_down_arrow_button.is_enabled:
                            row_down_arrow_button.enable()
                    elif (event.ui_element == row_down_arrow_button):
                        rows -= 1
                        if (abs(rows-columns) > max_diff):
                            columns -= 1
                            if not (column_up_arrow_button.is_enabled):
                                column_up_arrow_button.enable()
                        if (rows == row_min):
                            row_down_arrow_button.disable()
                        if not row_up_arrow_button.is_enabled:
                            row_up_arrow_button.enable()
                    elif (event.ui_element == column_up_arrow_button):
                        columns += 1
                        if (abs(rows-columns) > max_diff):
                            rows += 1
                            if not (row_down_arrow_button.is_enabled):
                                row_down_arrow_button.enable()
                        if (columns == col_max):
                            column_up_arrow_button.disable()
                        if not column_down_arrow_button.is_enabled:
                            column_down_arrow_button.enable()
                    elif (event.ui_element == column_down_arrow_button):
                        columns -= 1
                        if (abs(rows-columns) > max_diff):
                            rows -= 1
                            if not (row_up_arrow_button.is_enabled):
                                row_up_arrow_button.enable()
                        if (columns == col_min):
                            column_down_arrow_button.disable()
                        if not column_up_arrow_button.is_enabled:
                            column_up_arrow_button.enable()
                col_text.set_text(str(columns))
                row_text.set_text(str(rows))
            
            manager.process_events(event)

        background_manager.update(time_delta)
        background_manager.draw_ui(screen)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


def pause_menu():
    # all interactive elements will have this manager
    interactive_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)

    # all non-interactive elements will have this manager
    background_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)
    margin = 20
    line_spacing = 10
    
    #background rectangle
    menu_width = SCREEN_WIDTH * 0.5
    menu_height = SCREEN_HEIGHT * 0.3
    background_rect = pygame.Rect(
        SCREEN_WIDTH/2 - menu_width/2, 
        SCREEN_HEIGHT/2 - menu_height/2, 
        menu_width, 
        menu_height
    )
    background = pygame_gui.elements.UIPanel(
        relative_rect = background_rect,
        manager=background_manager,
        object_id=ObjectID(class_id="@menu-background")
    )

    exit_button_height = 30
    exit_button_width = menu_width - margin*2
    exit_button_rect = pygame.Rect(
        SCREEN_WIDTH/2 - exit_button_width/2,
        background_rect.bottom - margin - exit_button_height,
        exit_button_width,
        exit_button_height
    )
    exit_button = pygame_gui.elements.UIButton(
        relative_rect=exit_button_rect,
        text="exit to home screen",
        manager=interactive_manager,
        object_id=ObjectID(class_id="@small-button")
    )

    close_button_height = 30
    close_button_width = 30
    close_button_rect = pygame.Rect(
        background_rect.right - close_button_width - margin,
        background_rect.top + margin,
        close_button_width,
        close_button_height
    )
    close_button = pygame_gui.elements.UIButton(
        relative_rect=close_button_rect,
        text="",
        manager=interactive_manager,
        object_id=ObjectID(object_id="#close-button", class_id="@small-button")
    )

    paused_text_rect = pygame.Rect(
        SCREEN_WIDTH/2 - menu_width/2, 
        close_button_rect.bottom,
        menu_width, 
        exit_button_rect.top - close_button_rect.bottom
    )
    paused_text = pygame_gui.elements.UILabel(
        relative_rect=paused_text_rect,
        text="paused",
        manager=interactive_manager,
        object_id=ObjectID(class_id="@small-text-center")
    )
    
    background_manager.update(0)
    background_manager.draw_ui(screen)
    interactive_manager.update(0)
    interactive_manager.draw_ui(screen)
    pygame.display.update()
    
    paused = True
    time_delta = math.floor(time.time())
    while paused:
        for event in [pygame.event.wait()]+pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == exit_button:
                    paused = False
                    title_screen()
                elif event.ui_element == close_button:
                    paused = False

            interactive_manager.process_events(event)

        time_delta = math.floor(time.time()) - time_delta
        background_manager.update(time_delta)
        background_manager.draw_ui(screen)
        interactive_manager.update(time_delta)
        interactive_manager.draw_ui(screen)
        pygame.display.update()
        
def finished_menu(message):
    interactive_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)
    background_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)

    margin = 35
    line_spacing = 5
    
    #background surface
    menu_width = SCREEN_WIDTH * 0.5
    menu_height = SCREEN_HEIGHT * 0.3
    background_rect = pygame.Rect(
        SCREEN_WIDTH/2 - menu_width/2,
        SCREEN_HEIGHT/2 - menu_height/2,
        menu_width,
        menu_height
    )
    background = pygame_gui.elements.UIPanel(
        relative_rect=background_rect,
        manager=background_manager,
        object_id=ObjectID(class_id="@menu-background")
    )
    
    button_height = 40
    button_width = background_rect.width-margin*2
    
    #exit to home screen button
    exit_button_rect = pygame.Rect(
        background_rect.left + margin,
        background_rect.bottom - margin - button_height,
        button_width,
        button_height
    )
    exit_button = pygame_gui.elements.UIButton(
        relative_rect=exit_button_rect,
        text="exit to home screen",
        manager=interactive_manager,
        object_id=ObjectID(class_id="@small-button")
    )

    #play again button
    play_button_rect = pygame.Rect(
        background_rect.left + margin,
        exit_button_rect.top - button_height - line_spacing,
        button_width,
        button_height
    )
    play_button = pygame_gui.elements.UIButton(
        relative_rect=play_button_rect,
        text="play again",
        manager=interactive_manager,
        object_id=ObjectID(class_id="@small-button")
    )

    #congrats message
    finished_message_rect = pygame.Rect(
        background_rect.left + margin,
        background_rect.top + margin,
        background_rect.width - margin*2,
        play_button_rect.top - (background_rect.top+margin)
    )
    finished_message = pygame_gui.elements.UILabel (
        relative_rect=finished_message_rect,
        text=message,
        manager=background_manager,
        object_id=ObjectID(class_id="@small-text-center")
    )

    background_manager.update(0)
    background_manager.draw_ui(screen)
    interactive_manager.update(0)
    interactive_manager.draw_ui(screen)
    pygame.display.update()
    
    done = False
    time_delta = math.floor(time.time())
    while not done:
        for event in [pygame.event.wait()]+pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == exit_button:
                    title_screen()
                if event.ui_element == play_button:
                    play()
            interactive_manager.process_events(event)
        
        time_delta = math.floor(time.time()) - time_delta
        interactive_manager.update(time_delta)
        interactive_manager.draw_ui(screen)
        pygame.display.update()

def check_for_flag(flag_list, m_pos):
    for flag in flag_list:
        if flag.is_clicked(m_pos):
            return flag
    return None

def play():
    manager.clear_and_reset()

    global CELL_WIDTH
    global CELL_HEIGHT
    global MAZE_WIDTH
    global MAZE_HEIGHT
    global WALL_THICKNESS
    global rows
    global columns

    CELL_WIDTH = math.floor(MAZE_WIDTH/columns)
    CELL_WIDTH -= CELL_WIDTH%2
    CELL_HEIGHT = math.floor(MAZE_HEIGHT/rows)
    CELL_HEIGHT -= CELL_HEIGHT%2

    WALL_THICKNESS = round(CELL_WIDTH/10)
    WALL_THICKNESS -= WALL_THICKNESS%2
    if (WALL_THICKNESS < 2):
        WALL_THICKNESS = 2

    maze = create_maze(rows, columns)
    
    all_sprites = pygame.sprite.Group()
    wall_list = pygame.sprite.Group()
    flag_list = pygame.sprite.Group()

    #draw the maze
    x_pos = maze_startpoint[0]
    y_pos = maze_startpoint[1]
    for i in range(0, rows*2+1):
        for j in range(0, columns*2+1):
            if (i % 2 == 0 and j % 2 == 1): #horizontal
                if (maze[i][j] == 'w'):
                    wall = Wall(x_pos, y_pos, CELL_WIDTH, WALL_THICKNESS, 'h')
                    wall_list.add(wall)
                    all_sprites.add(wall)
                x_pos += CELL_WIDTH
            elif (i % 2 == 1 and j % 2 == 0): #vertical
                if (maze[i][j] == 'w'):
                    wall = Wall(x_pos, y_pos, WALL_THICKNESS, CELL_HEIGHT, 'v')
                    wall_list.add(wall)
                    all_sprites.add(wall)
                x_pos += CELL_WIDTH
        if (i % 2 == 1):
            y_pos += CELL_HEIGHT
        x_pos = 0

    startpoint = (random.randrange(0, rows), random.randrange(0, columns))
    while (startpoint == endpoint):
        startpoint = (random.randrange(0, rows), random.randrange(0, columns))
    start_cell = Cell(CELL_WIDTH * startpoint[1] + maze_startpoint[0] + WALL_THICKNESS/2, CELL_HEIGHT * startpoint[0] + maze_startpoint[1] + WALL_THICKNESS/2, startpoint_color, "rectangle")
    all_sprites.add(start_cell)
    
    end_cell = Cell(CELL_WIDTH * endpoint[1] + maze_startpoint[0] + WALL_THICKNESS/2, CELL_HEIGHT * endpoint[0] + maze_startpoint[1] + WALL_THICKNESS/2, endpoint_color, "rectangle")
    all_sprites.add(end_cell)
    
    player = Player(CELL_WIDTH * startpoint[1] + CELL_WIDTH/2 + maze_startpoint[0], CELL_HEIGHT * startpoint[0] + CELL_HEIGHT/2 + maze_startpoint[1], player_color)
    all_sprites.add(player)
    
    #pause button
    margin = 10

    pause_button_width = 30
    pause_button_height = 30
    pause_button_rect = pygame.Rect(
        SCREEN_WIDTH - margin - pause_button_width,
        margin,
        pause_button_width,
        pause_button_height
    )
    pause_button = pygame_gui.elements.UIButton(
        relative_rect=pause_button_rect,
        text="",
        manager=manager,
        object_id=ObjectID(object_id="#pause-button", class_id="@small-button")
    )
    
    #'press Enter to skip animation'
    skip_text_rect = pygame.Rect(
        10,
        10,
        SCREEN_WIDTH,
        50
    )
    skip_text = pygame_gui.elements.UILabel(
        relative_rect=skip_text_rect,
        text="press ENTER to skip animation",
        manager=manager,
        object_id=ObjectID(class_id="@small-text-center")
    )
    skip_text.hide()
                    
    done = False
    solving = False
    solution_stack = []
    solved = False
    solving = False
    curr_index = 1
    paused = False

    manager.update(0)
    manager.draw_ui(screen)
    while not done:
        time_delta = clock.tick(60)/1000.00
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == pause_button:
                    paused = True
                    pause_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (0, 0, 1):
                    m_pos = pygame.mouse.get_pos()
                    flag = check_for_flag(flag_list, m_pos)
                    if not flag:
                        new_flag = Flag(m_pos[0], m_pos[1])
                        flag_list.add(new_flag)
                        all_sprites.add(new_flag)
                    else:
                        flag_list.remove(flag)
                        all_sprites.remove(flag)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()
                if event.key == pygame.K_UP and not solving:
                    player.update(0, -1, wall_list)
                if event.key == pygame.K_DOWN and not solving:
                    player.update(0, 1, wall_list)
                if event.key == pygame.K_LEFT and not solving:
                    player.update(-1, 0, wall_list)
                if event.key == pygame.K_RIGHT and not solving:
                    player.update(1, 0, wall_list)
                if pygame.sprite.collide_rect(player, end_cell):
                    message = "YOU DID IT!"
                    done = True
                if event.key == pygame.K_s and not solved:
                    if solving:
                        solving = False
                        skip_text.hide()
                        all_sprites.remove(player)
                        all_sprites.add(player)
                    else:
                        if not solution_stack:
                            start = (startpoint[0]*2+1, startpoint[1]*2+1)
                            end = (endpoint[0]*2+1, endpoint[1]*2+1)
                            solution_stack = solve_maze(maze, start, end)
                        solving = True
                        skip_text.show()
                if event.key == pygame.K_RETURN and solving:
                    while (curr_index < len(solution_stack)-1):
                        curr_cell = solution_stack[curr_index]
                        new_cell = Cell(CELL_WIDTH * ((curr_cell[1]-curr_cell[1]%2)/2) + maze_startpoint[0] + WALL_THICKNESS/2, CELL_HEIGHT * ((curr_cell[0]-curr_cell[0]%2)/2) + maze_startpoint[1] + WALL_THICKNESS/2, solution_color, solution_image)
                        if solution_image == "line":
                            new_cell.draw_lines(solution_stack[curr_index-1], curr_cell, solution_stack[curr_index+1])
                        all_sprites.add(new_cell)
                        curr_index += 1
                    solving = False
                    solved = True
                    skip_text.hide()
                    all_sprites.remove(player)
                    all_sprites.add(player)

            manager.process_events(event)
        if solving and curr_index < len(solution_stack):
            curr_cell = solution_stack[curr_index]
            new_cell = Cell(CELL_WIDTH * ((curr_cell[1]-curr_cell[1]%2)/2) + maze_startpoint[0] + WALL_THICKNESS/2, CELL_HEIGHT * ((curr_cell[0]-curr_cell[0]%2)/2) + maze_startpoint[1] + WALL_THICKNESS/2, solution_color, solution_image)
            if solution_image == "line":
                new_cell.draw_lines(solution_stack[curr_index-1], curr_cell, solution_stack[curr_index+1])
            all_sprites.add(new_cell)
            curr_index += 1
            if curr_index >= len(solution_stack)-1:
                solving = False
                solved = True
                skip_text.hide()
                all_sprites.remove(player)
                all_sprites.add(player)
        background_manager.update(time_delta)
        background_manager.draw_ui(screen)
        all_sprites.draw(screen)
        manager.update(time_delta)
        manager.draw_ui(screen)
        
        pygame.display.update()
        
    restart = finished_menu(message)
    del all_sprites
    if restart:
        play()
    else:
        title_screen()

title_screen()

pygame.quit()
sys.exit()
    