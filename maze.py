#Zharia Eloby
#Maze Game with Pygame

import pygame
import random
import math

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

wall_color = black

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

MAZE_WIDTH = 700
MAZE_HEIGHT = 700

MAZE_COLS = 20
MAZE_ROWS = 20

CELL_WIDTH = math.floor(MAZE_WIDTH/MAZE_COLS)
CELL_HEIGHT = math.floor(MAZE_HEIGHT/MAZE_ROWS)

WALL_THICKNESS = round(CELL_WIDTH/10)

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([CELL_WIDTH-WALL_THICKNESS, CELL_HEIGHT-WALL_THICKNESS])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(wall_color)
        
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH+int(WALL_THICKNESS), SCREEN_HEIGHT+int(WALL_THICKNESS)])
pygame.display.set_caption("Maze")

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(white)

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
    
    print("grid initialized ----------------------\n")
    print(maze)
    
    cells_to_go = (num_rows*num_cols)-1 #when this gets to 0, it's done
    
    stack = []
    stack.append((1,1))
    maze[1][1] = 'v'
    
    print(maze)
    
    while (cells_to_go > 0):
        
        curr_cell = stack.pop()
        stack.append(curr_cell)
        
        print(curr_cell)
        
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
                endpoint = chosen
            stack.append(chosen)
            
        else:
            print("\nno neighbors, popping from stack\n")
            stack.pop()
        
    print("\nmaze created! -----------------------\n", maze, "\n")

    return maze


clock = pygame.time.Clock()

def start():
    maze = create_maze(MAZE_ROWS, MAZE_COLS)
    
    all_sprites = pygame.sprite.Group()

    x_pos = 0
    y_pos = 0
    for i in range(0, MAZE_ROWS*2+1):
        for j in range(0, MAZE_COLS*2+1):
            if (i % 2 == 0 and j % 2 == 1): #horizontal
                if (maze[i][j] == 'w'):
                    wall = Wall(x_pos, y_pos, CELL_WIDTH, WALL_THICKNESS)
                    all_sprites.add(wall)
                x_pos += CELL_WIDTH
            elif (i % 2 == 1 and j % 2 == 0): #vertical
                if (maze[i][j] == 'w'):
                    wall = Wall(x_pos, y_pos, WALL_THICKNESS, CELL_HEIGHT)
                    all_sprites.add(wall)
                x_pos += CELL_WIDTH
        if (i % 2 == 1):
            y_pos += CELL_HEIGHT
        x_pos = 0
            
    print("\nendpoint: ", endpoint)
    
    start_cell = Cell(CELL_WIDTH * (random.randrange(0, MAZE_ROWS)) + WALL_THICKNESS, CELL_HEIGHT * (random.randrange(0, MAZE_COLS)) + WALL_THICKNESS, green)
    all_sprites.add(start_cell)
    
    end_cell = Cell(CELL_WIDTH * ((endpoint[1] - 1)/2) + WALL_THICKNESS, CELL_HEIGHT * ((endpoint[0] - 1)/2) + WALL_THICKNESS, red)
    all_sprites.add(end_cell)
    
    done = False
    
    while not done:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        screen.fill(white)
        all_sprites.draw(screen)
        """
        image = pygame.Surface([100, 100])
        image.fill((255, 0, 0))
        rect = image.get_rect()
        rect.center = (0, 0)
        screen.blit(image, [25, 25])
        """
        pygame.display.flip()
                
                
start()

pygame.quit()
    