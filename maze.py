#Zharia Eloby
#Maze Game with Pygame

import pygame
import random
import math

black = (0, 0, 0)
white = (255, 255, 255)
gray = (230, 230, 230)
blue = (52, 118, 168)
red = (215, 74, 74)
green = (56, 220, 156)
tan = (234, 203, 187)

wall_color = black
background_color = tan

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750

MAZE_WIDTH = 600
MAZE_HEIGHT = 600

font_file = "Roboto-Regular.ttf"

maze_cols = 10
maze_rows = 10

#the coordinates for where the maze should start being drawn. top left corner = (0, 0)
maze_startpoint = (0, 75)

CELL_WIDTH = math.floor(MAZE_WIDTH/maze_cols)
CELL_HEIGHT = math.floor(MAZE_HEIGHT/maze_rows)

WALL_THICKNESS = round(CELL_WIDTH/10)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([CELL_WIDTH-WALL_THICKNESS*2, CELL_HEIGHT-WALL_THICKNESS*2])
        self.image.fill(white)
        self.image.set_colorkey(white)
        
        if CELL_WIDTH > CELL_HEIGHT:
            pygame.draw.circle(self.image, color, ((CELL_WIDTH-WALL_THICKNESS)/2, (CELL_HEIGHT-WALL_THICKNESS)/2), (CELL_HEIGHT - WALL_THICKNESS)/3)
        else:
            pygame.draw.circle(self.image, color, ((CELL_WIDTH-WALL_THICKNESS)/2, (CELL_HEIGHT-WALL_THICKNESS)/2), (CELL_WIDTH - WALL_THICKNESS)/3)
        
        self.rect = self.image.get_rect(center=(x, y))
        #self.rect.top = y
        #self.rect.left = x
        
    def update(self, x_direction, y_direction, wall_list):
        self.rect.top += 5*y_direction
        self.rect.left += 5*x_direction
        if pygame.sprite.spritecollideany(self, wall_list) == None:
            self.rect = self.rect.move(x_direction * CELL_WIDTH - 5*x_direction, y_direction * CELL_HEIGHT - 5*y_direction)
        else:
            self.rect.top -= 5*y_direction
            self.rect.left -= 5*x_direction
            

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([CELL_WIDTH-WALL_THICKNESS, CELL_HEIGHT-WALL_THICKNESS])
        self.image.fill(color)
        
        self.rect = self.image.get_rect(center=(x, y))
        #self.rect.top = y
        #self.rect.left = x


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(wall_color)
        
        if (type == 'v'):
            self.rect = self.image.get_rect(center=(x, 0))
            self.rect.top = y
        else:
            self.rect = self.image.get_rect(center=(0, y))
            self.rect.left = x
        


pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Maze")

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(white)

pygame.font.init()

def check_neighbors(maze, w, h, row, col):
    available_neighbors = []
    if (col > 1):               #has a left neighbor
        if (maze[row][col-2] != 'v'):
            available_neighbors += [(row, col-2)]
            
    if (col < w*2 - 2):         #has right neighbor
        if (maze[row][col+2] != 'v'):
            available_neighbors += [(row, col+2)]
            
    if (row > 1):               #has upper neighbor
        if (maze[row-2][col] != 'v'):
            available_neighbors += [(row-2, col)]
            
    if (row < h*2 - 2):         #has below neighbor
        if (maze[row+2][col] != 'v'):
            available_neighbors += [(row+2, col)]
            
    return available_neighbors

def create_maze(num_rows, num_cols):
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
    
    #print("grid initialized ----------------------\n")
    #print(maze)
    
    cells_to_go = (num_rows*num_cols)-1 #when this gets to 0, it's done
    
    stack = []
    stack.append((1,1))
    maze[1][1] = 'v'
    
    #print(maze)
    
    while (cells_to_go > 0):
        
        curr_cell = stack.pop()
        stack.append(curr_cell)
        
        #print(curr_cell)
        
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
            #print("\nno neighbors, popping from stack\n")
            stack.pop()
        
    #print("\nmaze created! -----------------------\n", maze, "\n")

    return maze

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

def solve_maze(maze, start, end):
    print("start: ", start)
    print("end: ", end)
    solution_path = [start]
    curr_cell = start
    maze[curr_cell[0]][curr_cell[1]] = 'x'
    available_paths = []
    while (curr_cell != end):
        available_paths = check_paths(maze, curr_cell)
        #print("ap: ", available_paths)
        while not available_paths:
            solution_path.pop()
            curr_cell = solution_path[len(solution_path)-1]
            available_paths = check_paths(maze, curr_cell)
        curr_cell = random.choice(available_paths)
        solution_path += [curr_cell]
        maze[curr_cell[0]][curr_cell[1]] = 'x'
    return solution_path

clock = pygame.time.Clock()

def home_screen():
    screen.fill(tan)
    
    #game title
    font_size = 100
    font = pygame.font.Font(font_file, font_size)
    title = "MAZE"
    title_text = font.render(title, True, white)
    text_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - font_size))
    screen.blit(title_text, text_rect)
    
    #credits
    font_size = 18
    font = pygame.font.Font(font_file, font_size)
    credit_text = font.render("created by Zharia Eloby", True, white)
    credit_text_rect = credit_text.get_rect(center=(SCREEN_WIDTH/2, 0))
    credit_text_rect.bottom = SCREEN_HEIGHT - 10
    screen.blit(credit_text, credit_text_rect)
    
    #play button
    play_button = pygame.Surface([SCREEN_WIDTH/2, SCREEN_HEIGHT/8])
    play_button.fill(white)
    play_rect = play_button.get_rect(center=(SCREEN_WIDTH/2, 0))
    play_rect.top = SCREEN_HEIGHT/2
    
    font_size = 24
    font = pygame.font.Font(font_file, font_size)
    
    play_text = font.render("play", True, black)
    play_text_rect = play_text.get_rect(center=play_rect.center)
    screen.blit(play_button, play_rect)
    screen.blit(play_text, play_text_rect)
    
    pygame.display.flip()
    
    ready = False
    while not ready:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    m_pos = pygame.mouse.get_pos()
                    if (play_rect.collidepoint(m_pos)): 
                        pick_size_screen()

def pick_size_screen():
    screen.fill(tan)
    
    font_size = 18
    font = pygame.font.Font(font_file, font_size)
    exit_text = font.render("press ESCAPE to exit", True, white)
    exit_text_rect = exit_text.get_rect()
    exit_text_rect.bottom = SCREEN_HEIGHT - 10
    exit_text_rect.right = SCREEN_WIDTH - 10
    screen.blit(exit_text, exit_text_rect)
    
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
    easy_button.fill(white)
    easy_button_rect = easy_button.get_rect(center=(SCREEN_WIDTH/2, 0))
    easy_button_rect.top = space_between_buttons
    
    easy_text = font.render("easy", True, black)
    easy_text_rect = easy_text.get_rect(center=easy_button_rect.center)
    screen.blit(easy_button, easy_button_rect)
    screen.blit(easy_text, easy_text_rect)
    
    #medium button
    medium_button = pygame.Surface([SCREEN_WIDTH/2, button_height])
    medium_button.fill(white)
    medium_button_rect = medium_button.get_rect(center=(SCREEN_WIDTH/2, 0))
    medium_button_rect.top = space_between_buttons*2+button_height
    
    medium_text = font.render("medium", True, black)
    medium_text_rect = medium_text.get_rect(center=medium_button_rect.center)
    screen.blit(medium_button, medium_button_rect)
    screen.blit(medium_text, medium_text_rect)
    
    #hard button
    hard_button = pygame.Surface([SCREEN_WIDTH/2, button_height])
    hard_button.fill(white)
    hard_button_rect = hard_button.get_rect(center=(SCREEN_WIDTH/2, 0))
    hard_button_rect.top = space_between_buttons*3+button_height*2
    
    hard_text = font.render("hard", True, black)
    hard_text_rect = hard_text.get_rect(center=hard_button_rect.center)
    screen.blit(hard_button, hard_button_rect)
    screen.blit(hard_text, hard_text_rect)
    
    #custom button
    custom_button = pygame.Surface([SCREEN_WIDTH/2, button_height])
    custom_button.fill(white)
    custom_button_rect = custom_button.get_rect(center=(SCREEN_WIDTH/2, 0))
    custom_button_rect.top = space_between_buttons*4+button_height*3
    
    custom_text = font.render("custom", True, black)
    custom_text_rect = custom_text.get_rect(center=custom_button_rect.center)
    screen.blit(custom_button, custom_button_rect)
    screen.blit(custom_text, custom_text_rect)
    
    font_size = math.floor(font_size/2)
    font = pygame.font.Font(font_file, font_size)
    
    #dimension text for easy button
    easy_dim_text = font.render(("(" + str(easy_dim[0]) + " x " + str(easy_dim[1]) + ")"), True, black)
    easy_dim_text_rect = easy_dim_text.get_rect(center=easy_text_rect.center)
    easy_dim_text_rect.top = easy_text_rect.bottom
    screen.blit(easy_dim_text, easy_dim_text_rect)

    #dimension text for medium button
    medium_dim_text = font.render(("(" + str(medium_dim[0]) + " x " + str(medium_dim[1]) + ")"), True, black)
    medium_dim_text_rect = medium_dim_text.get_rect(center=medium_text_rect.center)
    medium_dim_text_rect.top = medium_text_rect.bottom
    screen.blit(medium_dim_text, medium_dim_text_rect)

    #dimension text for hard button
    hard_dim_text = font.render(("(" + str(hard_dim[0]) + " x " + str(hard_dim[1]) + ")"), True, black)
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    home_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        m_pos = pygame.mouse.get_pos()
                        if (easy_button_rect.collidepoint(m_pos)):
                            print("\nyou chose easy")
                            maze_rows = easy_dim[0]
                            maze_cols = easy_dim[1]
                            ready = True
                        if (medium_button_rect.collidepoint(m_pos)):
                            print("\nyou chose medium")
                            maze_rows = medium_dim[0]
                            maze_cols = medium_dim[1]
                            ready = True
                        if (hard_button_rect.collidepoint(m_pos)):
                            print("\nyou chose hard")
                            maze_rows = hard_dim[0]
                            maze_cols = hard_dim[1]
                            ready = True
                        if (custom_button_rect.collidepoint(m_pos)):
                            print("\nyou chose custom")
                            custom_size_screen()
                            ready = True
                            
    CELL_WIDTH = math.floor(MAZE_WIDTH/maze_cols)
    CELL_HEIGHT = math.floor(MAZE_HEIGHT/maze_rows)

    WALL_THICKNESS = round(CELL_WIDTH/10)
    play()

def custom_size_screen():
    screen.fill(tan)
    
    rows = 10
    cols = 10
    
    font_size = 18
    font = pygame.font.Font(font_file, font_size)
    exit_text = font.render("press ESCAPE to exit", True, white)
    exit_text_rect = exit_text.get_rect()
    exit_text_rect.bottom = SCREEN_HEIGHT - 10
    exit_text_rect.right = SCREEN_WIDTH - 10
    screen.blit(exit_text, exit_text_rect)
    
    #select dimensions text
    font_size = 36
    font = pygame.font.Font(font_file, font_size)
    select_text = font.render("Select Your Dimensions", True, white)
    select_text_rect = select_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/5))
    screen.blit(select_text, select_text_rect)
    
    #text
    font_size = 24
    font = pygame.font.Font(font_file, font_size)
    x_text = font.render("x", True, white)
    x_text_rect = x_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(x_text, x_text_rect)
    
    font_size = 125
    font = pygame.font.Font(font_file, font_size)
    row_text = font.render(str(rows), True, white)
    row_text_rect = row_text.get_rect(center=(SCREEN_WIDTH/6*2, SCREEN_HEIGHT/2))
    screen.blit(row_text, row_text_rect)

    col_text = font.render(str(cols), True, white)
    col_text_rect = col_text.get_rect(center=(SCREEN_WIDTH/6*4, SCREEN_HEIGHT/2))
    screen.blit(col_text, col_text_rect)
    
    font_size = 24
    font = pygame.font.Font(font_file, font_size)
    play_button = pygame.Surface([SCREEN_WIDTH/2, font_size*2])
    play_button.fill(white)
    play_button_rect = play_button.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/5*4))
    
    play_text = font.render("play", True, black)
    play_text_rect = play_text.get_rect(center=play_button_rect.center)
    screen.blit(play_button, play_button_rect)
    screen.blit(play_text, play_text_rect)
    
    arrow_width = 100
    arrow_height = 100
    """
    #arrows
    row_up_arrow_image = pygame.image.load("arrow.png").convert_alpha()
    row_up_arrow_image = pygame.transform.scale(row_up_arrow_image, (25, 40))
    row_up_arrow_image = pygame.transform.rotate(row_up_arrow_image, 90)
    row_up_arrow_rect = row_up_arrow_image.get_rect(center=(row_text_rect.centerx, row_text_rect.centery - 125))
    screen.blit(row_up_arrow_image, row_up_arrow_rect)
    
    row_down_arrow_image = pygame.image.load("arrow.png").convert_alpha()
    row_down_arrow_image = pygame.transform.scale(row_down_arrow_image, (25, 40))
    row_down_arrow_image = pygame.transform.rotate(row_down_arrow_image, 270)
    row_down_arrow_rect = row_down_arrow_image.get_rect(center=(row_text_rect.centerx, row_text_rect.centery + 125))
    screen.blit(row_down_arrow_image, row_down_arrow_rect)
    
    col_up_arrow_image = pygame.image.load("arrow.png").convert_alpha()
    col_up_arrow_image = pygame.transform.scale(col_up_arrow_image, (25, 40))
    col_up_arrow_image = pygame.transform.rotate(col_up_arrow_image, 90)
    col_up_arrow_rect = col_up_arrow_image.get_rect(center=(col_text_rect.centerx, col_text_rect.centery - 125))
    screen.blit(col_up_arrow_image, col_up_arrow_rect)
    
    col_down_arrow_image = pygame.image.load("arrow.png").convert_alpha()
    col_down_arrow_image = pygame.transform.scale(col_down_arrow_image, (25, 40))
    col_down_arrow_image = pygame.transform.rotate(col_down_arrow_image, 270)
    col_down_arrow_rect = col_down_arrow_image.get_rect(center=(col_text_rect.centerx, col_text_rect.centery + 125))
    screen.blit(col_down_arrow_image, col_down_arrow_rect)
    """
    
    row_up_arrow_image = pygame.image.load("arrow-2.png").convert_alpha()
    row_up_arrow_image = pygame.transform.scale(row_up_arrow_image, (arrow_width, arrow_height))
    row_up_arrow_rect = row_up_arrow_image.get_rect(center=(row_text_rect.centerx, row_text_rect.centery - 125))
    screen.blit(row_up_arrow_image, row_up_arrow_rect)
    
    row_down_arrow_image = pygame.image.load("arrow-2.png").convert_alpha()
    row_down_arrow_image = pygame.transform.scale(row_down_arrow_image, (arrow_width, arrow_height))
    row_down_arrow_image = pygame.transform.rotate(row_down_arrow_image, 180)
    row_down_arrow_rect = row_down_arrow_image.get_rect(center=(row_text_rect.centerx, row_text_rect.centery + 125))
    screen.blit(row_down_arrow_image, row_down_arrow_rect)
    
    col_up_arrow_image = pygame.image.load("arrow-2.png").convert_alpha()
    col_up_arrow_image = pygame.transform.scale(col_up_arrow_image, (arrow_width, arrow_height))
    col_up_arrow_rect = col_up_arrow_image.get_rect(center=(col_text_rect.centerx, col_text_rect.centery - 125))
    screen.blit(col_up_arrow_image, col_up_arrow_rect)
    
    col_down_arrow_image = pygame.image.load("arrow-2.png").convert_alpha()
    col_down_arrow_image = pygame.transform.scale(col_down_arrow_image, (arrow_width, arrow_height))
    col_down_arrow_image = pygame.transform.rotate(col_down_arrow_image, 180)
    col_down_arrow_rect = col_down_arrow_image.get_rect(center=(col_text_rect.centerx, col_text_rect.centery + 125))
    screen.blit(col_down_arrow_image, col_down_arrow_rect)
    
    #ratio lock
    lock_image = pygame.image.load("ratio-lock.png").convert_alpha()
    lock_image = pygame.transform.scale(lock_image, (30, 30))
    lock_image_rect = lock_image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+125))
    lock_background = pygame.Surface([lock_image_rect.width+10, lock_image_rect.height+10])
    lock_background.fill(gray)
    lock_background_rect = lock_background.get_rect(center=lock_image_rect.center)
    screen.blit(lock_background, lock_background_rect)
    screen.blit(lock_image, lock_image_rect)
    
    #dimension error text
    font_size = 16
    font = pygame.font.Font(font_file, font_size)
    bounds_message = font.render("dimensions must stay within bounds", True, red)
    bounds_message_rect = bounds_message.get_rect(center=(SCREEN_WIDTH/2, 0))
    bounds_message_rect.top = select_text_rect.bottom
    bounds_message.set_alpha(0)
    screen.blit(bounds_message, bounds_message_rect)
    
    row_background = pygame.Surface([row_text_rect.width, row_text_rect.height])
    row_background.fill(tan)
    row_background_rect = row_background.get_rect(center=row_text_rect.center)
    
    col_background = pygame.Surface([col_text_rect.width, col_text_rect.height])
    col_background.fill(tan)
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
    locked = True
    while not ready:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    home_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    m_pos = pygame.mouse.get_pos()
                    if (lock_background_rect.collidepoint(m_pos)):
                        if locked:
                            locked = False
                            lock_background.fill(background_color)
                        else:
                            lock_background.fill(gray)
                            locked = True
                        pygame.display.update(screen.blit(lock_background, lock_background_rect))
                        pygame.display.update(screen.blit(lock_image, lock_image_rect))
                    if (play_button_rect.collidepoint(m_pos)):
                        maze_rows = rows
                        maze_cols = cols
                        CELL_WIDTH = math.floor(MAZE_WIDTH/maze_cols)
                        CELL_HEIGHT = math.floor(MAZE_HEIGHT/maze_rows)
                        WALL_THICKNESS = round(CELL_WIDTH/10)
                        play()
                        ready = True
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
                    
                    screen.fill(tan)
                    
                    pygame.display.update(screen.blit(row_background, row_background_rect))
                    pygame.display.update(screen.blit(col_background, col_background_rect))
                    
                    font_size = 125
                    font = pygame.font.Font(font_file, font_size)
                    row_text = font.render(str(rows), True, white)
                    row_text_rect = row_text.get_rect(center=(SCREEN_WIDTH/6*2, SCREEN_HEIGHT/2), width=200)
                    pygame.display.update(screen.blit(row_text, row_text_rect))

                    col_text = font.render(str(cols), True, white)
                    col_text_rect = col_text.get_rect(center=(SCREEN_WIDTH/6*4, SCREEN_HEIGHT/2))
                    pygame.display.update(screen.blit(col_text, col_text_rect))
   
        if display_bounds_message:
            screen.fill(tan)
            bounds_message.set_alpha(bounds_message.get_alpha()-5)
            if bounds_message.get_alpha() <= 50:
                display_bounds_message = False
                bounds_message.set_alpha(0)
            pygame.display.update(screen.blit(bounds_message, bounds_message_rect))
        clock.tick(60)

def pause_menu():
    margin = 20
    line_spacing = 10
    
    #background rectangle
    background = pygame.Surface([SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
    background.fill(gray)
    background_rect = background.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(background, background_rect)
    
    #paused bar
    paused_bar = pygame.Surface([background_rect.width, 30])
    paused_bar.fill(white)
    paused_bar_rect = paused_bar.get_rect(topleft=background_rect.topleft)
    screen.blit(paused_bar, paused_bar_rect)
    
    #paused bar text
    font_size = 16
    font = pygame.font.Font(font_file, font_size)
    paused_text = font.render("paused", True, black)
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
    nav_text = font.render("to navigate through the maze", True, black)
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
    press_S_text = font.render("to see the maze solution", True, black)
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
    right_click_text = font.render("to place marker", True, black)
    right_click_text_rect = right_click_text.get_rect(midleft=(mouse_rect.right+line_spacing, mouse_rect.centery))
    screen.blit(right_click_text, right_click_text_rect)
    
    #exit button
    exit_button = pygame.Surface([background_rect.width-margin*2, 50])
    exit_button.fill(white)
    exit_button_rect = exit_button.get_rect(midbottom=(background_rect.centerx, background_rect.bottom-margin))
    screen.blit(exit_button, exit_button_rect)
    
    #exit text for exit button
    font_size = 16
    font = pygame.font.Font(font_file, font_size)
    exit_text = font.render("exit to home screen", True, black)
    exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
    screen.blit(exit_text, exit_text_rect)
    
    pygame.display.update()
    
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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

def play():
    font_size = 24
    font = pygame.font.Font(font_file, font_size)

    maze = create_maze(maze_rows, maze_cols)
    
    all_sprites = pygame.sprite.Group()
    wall_list = pygame.sprite.Group()

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
            
    print("\nendpoint: ", endpoint)

    startpoint = (random.randrange(0, maze_rows), random.randrange(0, maze_cols))
    while (startpoint == endpoint):
        startpoint = (random.randrange(0, maze_rows), random.randrange(0, maze_cols))
    print("\nstartpoint: ", startpoint)
    start_cell = Cell(CELL_WIDTH * startpoint[1] + CELL_WIDTH/2 + maze_startpoint[0], CELL_HEIGHT * startpoint[0] + CELL_HEIGHT/2 + maze_startpoint[1], gray)
    all_sprites.add(start_cell)
    
    end_cell = Cell(CELL_WIDTH * endpoint[1] + CELL_WIDTH/2 + maze_startpoint[0], CELL_HEIGHT * endpoint[0] + CELL_HEIGHT/2 + maze_startpoint[1], green)
    all_sprites.add(end_cell)
    
    player = Player(CELL_WIDTH * startpoint[1] + CELL_WIDTH/2 + maze_startpoint[0], CELL_HEIGHT * startpoint[0] + CELL_HEIGHT/2 + maze_startpoint[1], blue)
    all_sprites.add(player)
    
    #pause button
    pause_button_image = pygame.image.load("pause-button.png").convert_alpha()
    pause_button_image = pygame.transform.scale(pause_button_image, (30, 30))
    pause_button_rect = pause_button_image.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    screen.blit(pause_button_image, pause_button_rect)
    
    """
    #"press ESC to exit" text
    font_size = 18
    font = pygame.font.Font(font_file, font_size)
    exit_text = font.render("press ESCAPE to exit", True, white)
    exit_text_rect = exit_text.get_rect()
    exit_text_rect.bottom = SCREEN_HEIGHT - 10
    exit_text_rect.right = SCREEN_WIDTH - 10
    """
    
    done = False
    solving = False
    solution_stack = []
    
    paused = False
    while not done:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    m_pos = pygame.mouse.get_pos()
                    if (pause_button_rect.collidepoint(m_pos)):
                        pause_menu()
                        paused = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    home_screen()
                    done = True
                if event.key == pygame.K_UP:
                    player.update(0, -1, wall_list)
                if event.key == pygame.K_DOWN:
                    player.update(0, 1, wall_list)
                if event.key == pygame.K_LEFT:
                    player.update(-1, 0, wall_list)
                if event.key == pygame.K_RIGHT:
                    player.update(1, 0, wall_list)
                if pygame.sprite.collide_rect(player, end_cell):
                    message = "YOU DID IT!"
                    done = True
                if event.key == pygame.K_s:
                    start = (startpoint[0]*2+1, startpoint[1]*2+1)
                    end = (endpoint[0]*2+1, endpoint[1]*2+1)
                    solution_stack = solve_maze(maze, start, end)
                    solution_stack.pop()
                    print("s: ", solution_stack)
                    for i in range(len(solution_stack) - 1):
                        curr_cell = solution_stack[i+1]
                        new_cell = Cell(CELL_WIDTH * ((curr_cell[1]-curr_cell[1]%2)/2) + CELL_WIDTH/2 + maze_startpoint[0], CELL_HEIGHT * ((curr_cell[0]-curr_cell[0]%2)/2) + CELL_HEIGHT/2 + maze_startpoint[1], white)
                        all_sprites.add(new_cell)
                        all_sprites.draw(screen)
                        pygame.display.flip()
                        clock.tick(10)

        screen.fill(tan)
        all_sprites.draw(screen)

        #screen.blit(exit_text, exit_text_rect)
        screen.blit(pause_button_image, pause_button_rect)
        
        pygame.display.flip()
        
        clock.tick(10)
                
    end_card = pygame.Surface([MAZE_WIDTH/3*2, MAZE_HEIGHT/3])
    end_card.fill(black)
    end_card_rect = end_card.get_rect(center=[MAZE_WIDTH/2, MAZE_HEIGHT/2])
    
    done = False
    restart = False
    
    all_sprites.draw(screen)
                
    screen.blit(end_card, end_card_rect)
    
    message_text = font.render(message, True, white)
    text_rect = message_text.get_rect(center=(MAZE_WIDTH/2, MAZE_HEIGHT/2 - font_size*2))
    screen.blit(message_text, text_rect)
    
    replay_text = font.render("press ENTER to play again", True, white)
    text_rect = replay_text.get_rect(center=(MAZE_WIDTH/2, MAZE_HEIGHT/2))
    screen.blit(replay_text, text_rect)
    
    exit_text = font.render("press ESCAPE to exit", True, white)
    text_rect = exit_text.get_rect(center=(MAZE_WIDTH/2, MAZE_HEIGHT/2 + font_size*2))
    screen.blit(exit_text, text_rect)

    pygame.display.flip()
        
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    home_screen()
                    done = True
                if event.key == pygame.K_RETURN:
                    done = True
                    restart = True
        
        clock.tick(10)
        
    del all_sprites
    if restart:
        play()
        
home_screen()

pygame.quit()
    