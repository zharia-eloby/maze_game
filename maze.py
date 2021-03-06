"""
Zharia Eloby
Maze Game with Pygame
"""

import pygame
import random
import math
import sys

black = (0, 0, 0)
white = (255, 255, 255)
gray = (230, 230, 230)
blue = (52, 118, 168)
red = (215, 74, 74)
green = (56, 220, 156)
tan = (234, 203, 187)

background_color = tan
wall_color = black
player_color = blue
startpoint_color = gray
endpoint_color = green
text_color = white
button_color = white
button_text_color = black
pause_menu_background_color = gray
pause_menu_text_color = black
pause_menu_button_color = white
pause_menu_button_text_color = black
finished_menu_background_color = black
finished_menu_text_color = white
finished_menu_button_color = white
finished_menu_button_text_color = black
error_color = red
solution_color = white

#value may be 'rectangle' 'line' or 'circle'
solution_image = "line"

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750

MAZE_WIDTH = 600
MAZE_HEIGHT = 600

font_file = "Roboto-Regular.ttf"

maze_cols = 10
maze_rows = 10

maze_startpoint = (0, 75)

CELL_WIDTH = 0
CELL_HEIGHT = 0

WALL_THICKNESS = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([CELL_WIDTH-WALL_THICKNESS*2, CELL_HEIGHT-WALL_THICKNESS*2])
        self.image.fill(white)
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect(center=(x, y))
        
        #cell width may differ from cell height -> make the diameter of the player object that of the lesser value between 
        #   CELL_HEIGHT and CELL_WIDTH so the player image doesn't overlap the walls of the maze
        if CELL_WIDTH > CELL_HEIGHT:
            pygame.draw.circle(self.image, color, (self.rect.width/2, self.rect.height/2), (CELL_HEIGHT - WALL_THICKNESS)/3)
        else:
            pygame.draw.circle(self.image, color, (self.rect.width/2, self.rect.height/2), (CELL_WIDTH - WALL_THICKNESS)/3)

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
        self.image = pygame.image.load("red-flag.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (math.floor(CELL_WIDTH * 0.75), math.floor(CELL_HEIGHT * 0.75)))
        self.rect = self.image.get_rect(center=(x, y))
    
    def is_clicked(self, m_pos):
        return self.rect.collidepoint(m_pos)

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Maze - created by Zharia Eloby")

clock = pygame.time.Clock()

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
home screen = the first screen the user sees. the hub
"""
def home_screen():
    screen.fill(background_color)
    
    #game title
    font_size = 100
    font = pygame.font.Font(font_file, font_size)
    title = "MAZE"
    title_text = font.render(title, True, text_color)
    text_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - font_size))
    screen.blit(title_text, text_rect)

    #credits
    font_size = 18
    font = pygame.font.Font(font_file, font_size)
    credit_text = font.render("created by Zharia Eloby", True, text_color)
    credit_text_rect = credit_text.get_rect(center=(SCREEN_WIDTH/2, 0))
    credit_text_rect.bottom = SCREEN_HEIGHT - 10
    screen.blit(credit_text, credit_text_rect)
    
    #play button
    play_button = pygame.Surface([SCREEN_WIDTH/2, SCREEN_HEIGHT/8])
    play_button.fill(button_color)
    play_rect = play_button.get_rect(center=(SCREEN_WIDTH/2, 0))
    play_rect.top = SCREEN_HEIGHT/2
    
    font_size = 24
    font = pygame.font.Font(font_file, font_size)
    
    play_text = font.render("play", True, button_text_color)
    play_text_rect = play_text.get_rect(center=play_rect.center)
    screen.blit(play_button, play_rect)
    screen.blit(play_text, play_text_rect)
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    m_pos = pygame.mouse.get_pos()
                    if (play_rect.collidepoint(m_pos)): 
                        pick_size_screen()

"""
the user can pick the size of their maze
preset sizes are easy, medium, and hard, or they can customize the size
"""
def pick_size_screen():
    screen.fill(background_color)
    
    back_button = pygame.image.load("arrow.png").convert_alpha()
    back_button = pygame.transform.scale(back_button, (20, 32))
    back_button = pygame.transform.rotate(back_button, 180)
    back_button_rect = back_button.get_rect(topleft=(25, 25))
    screen.blit(back_button, back_button_rect)
    
    num_buttons = 4
    space_between_buttons = SCREEN_HEIGHT/20
    button_height = (SCREEN_HEIGHT - space_between_buttons*(num_buttons+1))/num_buttons
    
    #set the dimensions for each difficulty
    easy_dim = (10, 10)
    medium_dim = (20, 20)
    hard_dim = (30, 30)
    
    font_size = math.floor(button_height/4)
    font = pygame.font.Font(font_file, font_size)
    
    #easy button
    easy_button = pygame.Surface([SCREEN_WIDTH/2, button_height])
    easy_button.fill(button_color)
    easy_button_rect = easy_button.get_rect(center=(SCREEN_WIDTH/2, 0))
    easy_button_rect.top = space_between_buttons
    
    easy_text = font.render("easy", True, button_text_color)
    easy_text_rect = easy_text.get_rect(center=easy_button_rect.center)
    screen.blit(easy_button, easy_button_rect)
    screen.blit(easy_text, easy_text_rect)
    
    #medium button
    medium_button = pygame.Surface([SCREEN_WIDTH/2, button_height])
    medium_button.fill(button_color)
    medium_button_rect = medium_button.get_rect(center=(SCREEN_WIDTH/2, 0))
    medium_button_rect.top = space_between_buttons*2+button_height
    
    medium_text = font.render("medium", True, button_text_color)
    medium_text_rect = medium_text.get_rect(center=medium_button_rect.center)
    screen.blit(medium_button, medium_button_rect)
    screen.blit(medium_text, medium_text_rect)
    
    #hard button
    hard_button = pygame.Surface([SCREEN_WIDTH/2, button_height])
    hard_button.fill(button_color)
    hard_button_rect = hard_button.get_rect(center=(SCREEN_WIDTH/2, 0))
    hard_button_rect.top = space_between_buttons*3+button_height*2
    
    hard_text = font.render("hard", True, button_text_color)
    hard_text_rect = hard_text.get_rect(center=hard_button_rect.center)
    screen.blit(hard_button, hard_button_rect)
    screen.blit(hard_text, hard_text_rect)
    
    #custom button
    custom_button = pygame.Surface([SCREEN_WIDTH/2, button_height])
    custom_button.fill(button_color)
    custom_button_rect = custom_button.get_rect(center=(SCREEN_WIDTH/2, 0))
    custom_button_rect.top = space_between_buttons*4+button_height*3
    
    custom_text = font.render("custom", True, button_text_color)
    custom_text_rect = custom_text.get_rect(center=custom_button_rect.center)
    screen.blit(custom_button, custom_button_rect)
    screen.blit(custom_text, custom_text_rect)
    
    font_size = math.floor(font_size/2)
    font = pygame.font.Font(font_file, font_size)
    
    #dimension text for easy button
    easy_dim_text = font.render(("(" + str(easy_dim[0]) + " x " + str(easy_dim[1]) + ")"), True, button_text_color)
    easy_dim_text_rect = easy_dim_text.get_rect(center=easy_text_rect.center)
    easy_dim_text_rect.top = easy_text_rect.bottom
    screen.blit(easy_dim_text, easy_dim_text_rect)

    #dimension text for medium button
    medium_dim_text = font.render(("(" + str(medium_dim[0]) + " x " + str(medium_dim[1]) + ")"), True, button_text_color)
    medium_dim_text_rect = medium_dim_text.get_rect(center=medium_text_rect.center)
    medium_dim_text_rect.top = medium_text_rect.bottom
    screen.blit(medium_dim_text, medium_dim_text_rect)

    #dimension text for hard button
    hard_dim_text = font.render(("(" + str(hard_dim[0]) + " x " + str(hard_dim[1]) + ")"), True, button_text_color)
    hard_dim_text_rect = hard_dim_text.get_rect(center=hard_text_rect.center)
    hard_dim_text_rect.top = hard_text_rect.bottom
    screen.blit(hard_dim_text, hard_dim_text_rect)

    pygame.display.flip()
    
    global maze_cols
    global maze_rows
    global CELL_WIDTH
    global CELL_HEIGHT
    global WALL_THICKNESS
    
    ready = False   
    while not ready:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    home_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        m_pos = pygame.mouse.get_pos()
                        if (back_button_rect.collidepoint(m_pos)):
                            home_screen()
                        if (easy_button_rect.collidepoint(m_pos)):
                            maze_rows = easy_dim[0]
                            maze_cols = easy_dim[1]
                            ready = True
                        if (medium_button_rect.collidepoint(m_pos)):
                            maze_rows = medium_dim[0]
                            maze_cols = medium_dim[1]
                            ready = True
                        if (hard_button_rect.collidepoint(m_pos)):
                            maze_rows = hard_dim[0]
                            maze_cols = hard_dim[1]
                            ready = True
                        if (custom_button_rect.collidepoint(m_pos)):
                            custom_size_screen()
                            
    CELL_WIDTH = math.floor(MAZE_WIDTH/maze_cols)
    CELL_WIDTH -= CELL_WIDTH%2
    CELL_HEIGHT = math.floor(MAZE_HEIGHT/maze_rows)
    CELL_HEIGHT -= CELL_HEIGHT%2

    WALL_THICKNESS = round(CELL_WIDTH/10)
    WALL_THICKNESS -= WALL_THICKNESS%2
    if (WALL_THICKNESS < 2):
        WALL_THICKNESS = 2
    play()

def custom_size_screen():
    screen.fill(background_color)
    
    rows = 15
    cols = 15
    
    back_button = pygame.image.load("arrow.png").convert_alpha()
    back_button = pygame.transform.scale(back_button, (20, 32))
    back_button = pygame.transform.rotate(back_button, 180)
    back_button_rect = back_button.get_rect(topleft=(25, 25))
    screen.blit(back_button, back_button_rect)
    
    #select dimensions text
    font_size = 36
    font = pygame.font.Font(font_file, font_size)
    select_text = font.render("Select Your Dimensions", True, text_color)
    select_text_rect = select_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/5))
    screen.blit(select_text, select_text_rect)
    
    #'x' text
    font_size = 24
    font = pygame.font.Font(font_file, font_size)
    x_text = font.render("x", True, text_color)
    x_text_rect = x_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(x_text, x_text_rect)
    
    #row text
    font_size = 125
    font = pygame.font.Font(font_file, font_size)
    row_text = font.render(str(rows), True, text_color)
    row_text_rect = row_text.get_rect(center=(SCREEN_WIDTH/6*2, SCREEN_HEIGHT/2))
    screen.blit(row_text, row_text_rect)

    #column text
    col_text = font.render(str(cols), True, text_color)
    col_text_rect = col_text.get_rect(center=(SCREEN_WIDTH/6*4, SCREEN_HEIGHT/2))
    screen.blit(col_text, col_text_rect)
    
    #play button
    font_size = 24
    font = pygame.font.Font(font_file, font_size)
    play_button = pygame.Surface([SCREEN_WIDTH/2, font_size*2])
    play_button.fill(button_color)
    play_button_rect = play_button.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/5*4))
    
    play_text = font.render("play", True, button_text_color)
    play_text_rect = play_text.get_rect(center=play_button_rect.center)
    screen.blit(play_button, play_button_rect)
    screen.blit(play_text, play_text_rect)
    
    #arrows
    arrow_width = 100
    arrow_height = 100
    
    arrow_padding = 125
    
    row_up_arrow_image = pygame.image.load("arrow-2.png").convert_alpha()
    row_up_arrow_image = pygame.transform.scale(row_up_arrow_image, (arrow_width, arrow_height))
    row_up_arrow_rect = row_up_arrow_image.get_rect(center=(row_text_rect.centerx, row_text_rect.centery - arrow_padding))
    screen.blit(row_up_arrow_image, row_up_arrow_rect)
    
    row_down_arrow_image = pygame.image.load("arrow-2.png").convert_alpha()
    row_down_arrow_image = pygame.transform.scale(row_down_arrow_image, (arrow_width, arrow_height))
    row_down_arrow_image = pygame.transform.rotate(row_down_arrow_image, 180)
    row_down_arrow_rect = row_down_arrow_image.get_rect(center=(row_text_rect.centerx, row_text_rect.centery + arrow_padding))
    screen.blit(row_down_arrow_image, row_down_arrow_rect)
    
    col_up_arrow_image = pygame.image.load("arrow-2.png").convert_alpha()
    col_up_arrow_image = pygame.transform.scale(col_up_arrow_image, (arrow_width, arrow_height))
    col_up_arrow_rect = col_up_arrow_image.get_rect(center=(col_text_rect.centerx, col_text_rect.centery - arrow_padding))
    screen.blit(col_up_arrow_image, col_up_arrow_rect)
    
    col_down_arrow_image = pygame.image.load("arrow-2.png").convert_alpha()
    col_down_arrow_image = pygame.transform.scale(col_down_arrow_image, (arrow_width, arrow_height))
    col_down_arrow_image = pygame.transform.rotate(col_down_arrow_image, 180)
    col_down_arrow_rect = col_down_arrow_image.get_rect(center=(col_text_rect.centerx, col_text_rect.centery + arrow_padding))
    screen.blit(col_down_arrow_image, col_down_arrow_rect)
    
    #ratio lock
    lock_image = pygame.image.load("ratio-lock.png").convert_alpha()
    lock_image = pygame.transform.scale(lock_image, (30, 30))
    lock_image_rect = lock_image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+125))
    lock_background = pygame.Surface([lock_image_rect.width+10, lock_image_rect.height+10])
    lock_background.fill(button_color)
    lock_background_rect = lock_background.get_rect(center=lock_image_rect.center)
    screen.blit(lock_background, lock_background_rect)
    screen.blit(lock_image, lock_image_rect)
    
    #dimension error text
    font_size = 16
    font = pygame.font.Font(font_file, font_size)
    bounds_message = font.render("dimensions must stay within bounds", True, error_color)
    bounds_message_rect = bounds_message.get_rect(center=(SCREEN_WIDTH/2, 0))
    bounds_message_rect.top = select_text_rect.bottom
    bounds_message.set_alpha(0)
    screen.blit(bounds_message, bounds_message_rect)
    
    #makes sure that past displays don't show behind current text (specifically for single digit dimension)
    row_background = pygame.Surface([row_text_rect.width, row_text_rect.height])
    row_background.fill(background_color)
    row_background_rect = row_background.get_rect(center=row_text_rect.center)
    
    col_background = pygame.Surface([col_text_rect.width, col_text_rect.height])
    col_background.fill(background_color)
    col_background_rect = col_background.get_rect(center=col_text_rect.center)
    
    pygame.display.flip()
    
    row_min = 5
    row_max = 50
    col_min = 5
    col_max = 50
    
    global maze_cols
    global maze_rows
    global CELL_WIDTH
    global CELL_HEIGHT
    global WALL_THICKNESS
    
    display_bounds_message = False
    ready = False
    locked = True #if True, rows and cols change simultaneously
    while not ready:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    home_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    m_pos = pygame.mouse.get_pos()
                    if (back_button_rect.collidepoint(m_pos)):
                        pick_size_screen()
                    if (lock_background_rect.collidepoint(m_pos)):
                        if locked:
                            locked = False
                            lock_background.fill(background_color)
                        else:
                            lock_background.fill(button_color)
                            locked = True
                        pygame.display.update(screen.blit(lock_background, lock_background_rect))
                        pygame.display.update(screen.blit(lock_image, lock_image_rect))
                    if (play_button_rect.collidepoint(m_pos)):
                        maze_rows = rows
                        maze_cols = cols
                        CELL_WIDTH = math.floor(MAZE_WIDTH/maze_cols)
                        CELL_WIDTH -= CELL_WIDTH % 2
                        CELL_HEIGHT = math.floor(MAZE_HEIGHT/maze_rows)
                        CELL_HEIGHT -= CELL_HEIGHT % 2
                        WALL_THICKNESS = round(CELL_WIDTH/10)
                        WALL_THICKNESS -= WALL_THICKNESS%2
                        if (WALL_THICKNESS < 2):
                            WALL_THICKNESS = 2
                        play()
                        ready = True
                        break
                    if (row_up_arrow_rect.collidepoint(m_pos) and rows < row_max):
                        rows += 1
                        if locked: 
                            cols += 1
                        elif (rows - cols > 10):
                            cols += 1
                            display_bounds_message = True
                    if (row_down_arrow_rect.collidepoint(m_pos) and rows > row_min):
                        rows -= 1
                        if locked:
                            cols -= 1
                        elif (cols - rows > 10):
                            cols -= 1
                            display_bounds_message = True
                    if (col_up_arrow_rect.collidepoint(m_pos) and cols < col_max):
                        cols += 1
                        if locked:
                            rows += 1
                        elif (cols - rows > 10):
                            rows += 1
                            display_bounds_message = True
                    if (col_down_arrow_rect.collidepoint(m_pos) and cols > col_min):
                        cols -= 1
                        if locked:
                            rows -= 1
                        elif (rows - cols > 10):
                            rows -= 1
                            display_bounds_message = True
                    if display_bounds_message:
                        bounds_message.set_alpha(255)
                    
                    screen.fill(background_color)
                    
                    pygame.display.update(screen.blit(row_background, row_background_rect))
                    pygame.display.update(screen.blit(col_background, col_background_rect))
                    
                    font_size = 125
                    font = pygame.font.Font(font_file, font_size)
                    row_text = font.render(str(rows), True, text_color)
                    row_text_rect = row_text.get_rect(center=(SCREEN_WIDTH/6*2, SCREEN_HEIGHT/2), width=200)
                    pygame.display.update(screen.blit(row_text, row_text_rect))

                    col_text = font.render(str(cols), True, text_color)
                    col_text_rect = col_text.get_rect(center=(SCREEN_WIDTH/6*4, SCREEN_HEIGHT/2))
                    pygame.display.update(screen.blit(col_text, col_text_rect))
   
        #bounds message slowly fades over a few seconds
        if display_bounds_message:
            screen.fill(background_color)
            bounds_message.set_alpha(bounds_message.get_alpha()-2)
            if bounds_message.get_alpha() <= 50:
                display_bounds_message = False
                bounds_message.set_alpha(0)
            pygame.display.update(screen.blit(bounds_message, bounds_message_rect))
        clock.tick(30)

def pause_menu():
    margin = 20
    line_spacing = 10
    
    #background rectangle
    background = pygame.Surface([SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
    background.fill(pause_menu_background_color)
    background_rect = background.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(background, background_rect)
    
    #paused bar
    paused_bar = pygame.Surface([background_rect.width, 30])
    paused_bar.fill(pause_menu_button_color)
    paused_bar_rect = paused_bar.get_rect(topleft=background_rect.topleft)
    screen.blit(paused_bar, paused_bar_rect)
    
    #paused bar text
    font_size = 16
    font = pygame.font.Font(font_file, font_size)
    paused_text = font.render("PAUSED", True, pause_menu_button_text_color)
    paused_text_rect = paused_text.get_rect(center=paused_bar_rect.center)
    screen.blit(paused_text, paused_text_rect)
    
    #close button
    close_button_image = pygame.image.load("close-button.png").convert_alpha()
    close_button_image = pygame.transform.scale(close_button_image, (25, 25))
    close_button_rect = close_button_image.get_rect(midright=(paused_bar_rect.right-line_spacing, paused_bar_rect.centery))
    screen.blit(close_button_image, close_button_rect)
    
    #arrow keys for nav info
    arrow_keys_image = pygame.image.load("arrow-keys.png").convert_alpha()
    arrow_keys_image = pygame.transform.scale(arrow_keys_image, (50, 50))
    arrow_keys_rect = arrow_keys_image.get_rect(topleft=(paused_bar_rect.left+margin, paused_bar_rect.bottom+line_spacing))
    screen.blit(arrow_keys_image, arrow_keys_rect)
    
    #navigation info
    font_size = 16
    font = pygame.font.Font(font_file, font_size)
    nav_text = font.render("to navigate through the maze", True, pause_menu_text_color)
    nav_text_rect = nav_text.get_rect(midleft=(arrow_keys_rect.right+line_spacing, arrow_keys_rect.centery))
    screen.blit(nav_text, nav_text_rect)
    
    #s key image
    s_key_image = pygame.image.load("s-key.png").convert_alpha()
    s_key_image = pygame.transform.scale(s_key_image, (50, 50))
    s_key_rect = s_key_image.get_rect(topleft=(arrow_keys_rect.left, arrow_keys_rect.bottom+line_spacing))
    screen.blit(s_key_image, s_key_rect)
    
    #press S to solve text
    font_size = 16
    font = pygame.font.Font(font_file, font_size)
    press_S_text = font.render("to see the maze solution", True, pause_menu_text_color)
    press_S_rect = press_S_text.get_rect(midleft=(s_key_rect.right+line_spacing, s_key_rect.centery))
    screen.blit(press_S_text, press_S_rect)
    
    #mouse right click image
    mouse_image = pygame.image.load("mouse-right-click.png").convert_alpha()
    mouse_image = pygame.transform.scale(mouse_image, (50, 50))
    mouse_rect = mouse_image.get_rect(topleft=(s_key_rect.left, s_key_rect.bottom+line_spacing))
    screen.blit(mouse_image, mouse_rect)
    
    #mouse right click text
    font_size = 16
    font = pygame.font.Font(font_file, font_size)
    right_click_text = font.render("to place/remove a marker", True, pause_menu_text_color)
    right_click_text_rect = right_click_text.get_rect(midleft=(mouse_rect.right+line_spacing, mouse_rect.centery))
    screen.blit(right_click_text, right_click_text_rect)
    
    #flag image
    flag_image = pygame.image.load("red-flag.png").convert_alpha()
    flag_image = pygame.transform.scale(flag_image, (30, 30))
    flag_rect = flag_image.get_rect(bottomleft=right_click_text_rect.bottomright)
    screen.blit(flag_image, flag_rect)
    
    #exit button
    exit_button = pygame.Surface([background_rect.width-margin*2, 50])
    exit_button.fill(pause_menu_button_color)
    exit_button_rect = exit_button.get_rect(midbottom=(background_rect.centerx, background_rect.bottom-margin))
    screen.blit(exit_button, exit_button_rect)
    
    #exit text for exit button
    font_size = 16
    font = pygame.font.Font(font_file, font_size)
    exit_text = font.render("exit to home screen", True, pause_menu_button_text_color)
    exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
    screen.blit(exit_text, exit_text_rect)
    
    pygame.display.update()
    
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    background.set_alpha(0)
                    paused = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    m_pos = pygame.mouse.get_pos()
                    if exit_button_rect.collidepoint(m_pos):
                        home_screen()
                        paused = False
                    if close_button_rect.collidepoint(m_pos):
                        background.set_alpha(0)
                        paused = False
                    
                
        clock.tick(60)
        
def finished_menu(message):
    margin = 35
    line_spacing = 5
    
    #background surface
    background = pygame.Surface([2*SCREEN_WIDTH/3, SCREEN_HEIGHT/3])
    background.fill(finished_menu_background_color)
    background.set_alpha(200)
    background_rect = background.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(background, background_rect)
    
    #congrats message
    font_size = 24
    font = pygame.font.Font(font_file, font_size)
    message_text = font.render(message, True, finished_menu_text_color)
    message_text_rect = message_text.get_rect(center=(background_rect.centerx, background_rect.top+margin))
    screen.blit(message_text, message_text_rect)
    
    button_height = 40
    button_width = background_rect.width-margin*2
    
    #play again button
    play_again_button = pygame.Surface([button_width, button_height])
    play_again_button.fill(finished_menu_button_color)
    play_again_button_rect = play_again_button.get_rect(bottomleft=(background_rect.left+margin, background_rect.bottom-margin-line_spacing-button_height))
    screen.blit(play_again_button, play_again_button_rect)
    
    #text for play again button
    font_size = 16
    font = pygame.font.Font(font_file, font_size)
    play_again_text = font.render("play again", True, finished_menu_button_text_color)
    play_again_text_rect = play_again_text.get_rect(center=play_again_button_rect.center)
    screen.blit(play_again_text, play_again_text_rect)
    
    #exit to home screen button
    exit_button = pygame.Surface([button_width, button_height])
    exit_button.fill(finished_menu_button_color)
    exit_button_rect = exit_button.get_rect(bottomleft=(background_rect.left+margin, background_rect.bottom-margin))
    screen.blit(exit_button, exit_button_rect)
    
    #text for exit button
    exit_button_text = font.render("exit to home screen", True, finished_menu_button_text_color)
    exit_button_text_rect = exit_button_text.get_rect(center=exit_button_rect.center)
    screen.blit(exit_button_text, exit_button_text_rect)
    
    pygame.display.update()
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    m_pos = pygame.mouse.get_pos()
                    if play_again_button_rect.collidepoint(m_pos):    
                        return True
                    if exit_button_rect.collidepoint(m_pos):
                        return False
        clock.tick(30)

def check_for_flag(flag_list, m_pos):
    for flag in flag_list:
        if flag.is_clicked(m_pos):
            return flag
    return None

def play():
    font_size = 24
    font = pygame.font.Font(font_file, font_size)

    maze = create_maze(maze_rows, maze_cols)
    
    all_sprites = pygame.sprite.Group()
    wall_list = pygame.sprite.Group()
    flag_list = pygame.sprite.Group()

    #draw the maze
    x_pos = maze_startpoint[0]
    y_pos = maze_startpoint[1]
    for i in range(0, maze_rows*2+1):
        for j in range(0, maze_cols*2+1):
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

    startpoint = (random.randrange(0, maze_rows), random.randrange(0, maze_cols))
    while (startpoint == endpoint):
        startpoint = (random.randrange(0, maze_rows), random.randrange(0, maze_cols))
    start_cell = Cell(CELL_WIDTH * startpoint[1] + maze_startpoint[0] + WALL_THICKNESS/2, CELL_HEIGHT * startpoint[0] + maze_startpoint[1] + WALL_THICKNESS/2, startpoint_color, "rectangle")
    all_sprites.add(start_cell)
    
    end_cell = Cell(CELL_WIDTH * endpoint[1] + maze_startpoint[0] + WALL_THICKNESS/2, CELL_HEIGHT * endpoint[0] + maze_startpoint[1] + WALL_THICKNESS/2, endpoint_color, "rectangle")
    all_sprites.add(end_cell)
    
    player = Player(CELL_WIDTH * startpoint[1] + CELL_WIDTH/2 + maze_startpoint[0], CELL_HEIGHT * startpoint[0] + CELL_HEIGHT/2 + maze_startpoint[1], player_color)
    all_sprites.add(player)
    
    #pause button
    pause_button_image = pygame.image.load("pause-button.png").convert_alpha()
    pause_button_image = pygame.transform.scale(pause_button_image, (30, 30))
    pause_button_rect = pause_button_image.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    screen.blit(pause_button_image, pause_button_rect)
    
    #'press Enter to skip animation'
    font_size = 24
    font = pygame.font.Font(font_file, font_size)
    skip_text = font.render("press ENTER to skip animation", True, text_color)
    skip_text_rect = skip_text.get_rect(topleft=(10, 10))
                    
    done = False
    solving = False
    solution_stack = []
    solved = False
    solving = False
    curr_index = 1
    paused = False

    while not done:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    m_pos = pygame.mouse.get_pos()
                    if (pause_button_rect.collidepoint(m_pos)):
                        pause_menu()
                        paused = True
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
                        all_sprites.remove(player)
                        all_sprites.add(player)
                    else:
                        if not solution_stack:
                            start = (startpoint[0]*2+1, startpoint[1]*2+1)
                            end = (endpoint[0]*2+1, endpoint[1]*2+1)
                            solution_stack = solve_maze(maze, start, end)
                        solving = True
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
                    all_sprites.remove(player)
                    all_sprites.add(player)
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
                all_sprites.remove(player)
                all_sprites.add(player)

        screen.fill(background_color)
        all_sprites.draw(screen)
        
        screen.blit(pause_button_image, pause_button_rect)
        if solving:
            screen.blit(skip_text, skip_text_rect)
        
        pygame.display.flip()
        
        clock.tick(30)
        
    restart = finished_menu(message)
    del all_sprites
    if restart:
        play()
    else:
        home_screen()
    
home_screen()

pygame.quit()
sys.exit()
    