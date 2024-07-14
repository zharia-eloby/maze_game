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
from PIL import Image
import json
from pathlib import Path
from helpers.settings import get_settings
from helpers.initialize import initialize_pygame
from helpers.redraw import redraw_elements
from helpers.create_maze import create_maze
from helpers.solve_maze import solve_maze
from helpers.audio import set_audio_buttons, toggle_audio

resize_images = False

settings = get_settings()
SCREEN_WIDTH = settings['screen_width']
SCREEN_MARGIN = settings['margin']
SCREEN_HEIGHT = settings['screen_height']
src_path = sys.path[0]
theme_file = os.path.join(src_path, settings['theme']['path'])
audio_file = os.path.join(src_path, settings['theme']['audio']['path'])

initialize_pygame()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

UI_AREA = pygame.Rect(
    SCREEN_MARGIN,
    SCREEN_MARGIN,
    SCREEN_WIDTH - SCREEN_MARGIN*2,
    SCREEN_HEIGHT - SCREEN_MARGIN*2
)

if (UI_AREA.width > UI_AREA.height):
    MAZE_HEIGHT = UI_AREA.height
    MAZE_WIDTH = MAZE_HEIGHT
else:
    MAZE_HEIGHT = UI_AREA.width
    MAZE_WIDTH = MAZE_HEIGHT

maze_topleft = (UI_AREA.centerx - MAZE_WIDTH/2, UI_AREA.centery - MAZE_HEIGHT/2) 

background_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)
background_rect = pygame.Rect(
    0,
    0,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)
img_file = Path(__file__).parent / "assets/images/background/pixelart_starfield.png"
if resize_images:
    img = Image.open(img_file)
    img = img.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
    img.save(img_file)
background = pygame_gui.elements.UIImage(
    relative_rect=background_rect,
    image_surface=pygame.image.load(img_file).convert(),
    manager=background_manager
)
background.disable()

clock = pygame.time.Clock()

"""
for debugging purposes
"""
def print_maze():
    for i in maze:
        print(i)

def resize_image(image_id, width, height, normal=True, hovered=True):
    if resize_images:
        file = open(theme_file, "r")
        contents = json.loads(file.read())
        file.close()
        images_folder = os.path.join(src_path, "assets/images/")
        if (normal):
            image_file = contents[image_id]['images']['normal_image']['resource']
            img = Image.open(images_folder + image_file)
            img = img.resize((width, height))
            img = img.save(images_folder + image_file)
        if (hovered):
            image_file = contents[image_id]['images']['hovered_image']['resource']
            img = Image.open(images_folder + image_file)
            img = img.resize((width, height))
            img.save(images_folder + image_file)

"""
get the left position of the cell based on the column index in the 'maze' array
"""
def get_cell_x_position(column_index):
    grid_index = ((column_index-1)/2)
    x_position = grid_index * CELL_WIDTH + maze_topleft[0] + WALL_THICKNESS
    return x_position

"""
get the top position of the cell based on the row index in the 'maze' array
"""
def get_cell_y_position(row_index):
    grid_index = ((row_index-1)/2)
    y_position = grid_index * CELL_HEIGHT + maze_topleft[1] + WALL_THICKNESS
    return y_position
    
"""
home screen
- contains title, play button, and 'created by' text
"""
def title_screen():
    title_screen_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)

    # audio buttons
    button_width = 45
    button_height = button_width
    audio_button_rect = pygame.Rect(
        UI_AREA.right - button_width,   # x
        UI_AREA.top,                    # y
        button_width,                   # width
        button_height                   # height
    )
    audio_button = pygame_gui.elements.UIButton(
        relative_rect=audio_button_rect, 
        text="",
        manager=title_screen_manager,
        object_id=ObjectID(object_id="#audio-button")
    )
    no_audio_button = pygame_gui.elements.UIButton(
        relative_rect=audio_button_rect, 
        text="",
        manager=title_screen_manager,
        object_id=ObjectID(object_id="#no-audio-button")
    )
    set_audio_buttons(audio_button, no_audio_button)
    resize_image('#audio-button', button_width, button_height)
    resize_image('#no-audio-button', button_width, button_height)

    # play button
    button_width = math.floor(UI_AREA.width/2)
    button_height = 100
    play_rect = pygame.Rect(
        UI_AREA.centerx - button_width/2,  # x
        UI_AREA.centery + button_height/2, # y
        button_width,                   # width
        button_height                   # height
    )
    play_button = pygame_gui.elements.UIButton(
        relative_rect=play_rect, 
        text="",
        manager=title_screen_manager,
        object_id=ObjectID(class_id="#play-button")
    )
    resize_image('#play-button', button_width, button_height)
    
    # game title
    title_rect = pygame.Rect(
        UI_AREA.left, 
        UI_AREA.top,
        UI_AREA.width, 
        play_rect.top - UI_AREA.top
    )
    pygame_gui.elements.UILabel(
        relative_rect=title_rect, 
        text="MAZE",
        manager=title_screen_manager,
        object_id=ObjectID(object_id="#title")
    )

    # credits
    credits_height = 210
    credits_rect = pygame.Rect(
        UI_AREA.left,
        play_rect.bottom, 
        UI_AREA.width, 
        UI_AREA.bottom - play_rect.bottom
    )
    pygame_gui.elements.UILabel(
        relative_rect=credits_rect, 
        text="created by Zharia Eloby",
        manager=title_screen_manager,
        object_id=ObjectID(class_id="@small-text")
    )

    redraw_elements(screen, [background_manager, title_screen_manager], 0)

    time_delta = math.ceil(time.time())
    while True:
        for event in [pygame.event.wait()]+pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame_gui.UI_BUTTON_PRESSED :
                if event.ui_element == play_button:
                    pick_size_screen()
                elif event.ui_element == audio_button or event.ui_element == no_audio_button:
                    toggle_audio(audio_file, audio_button, no_audio_button)

            # redraw window upon reopening after minimizing
            elif event.type == pygame.WINDOWRESTORED:
                pygame.display.update()

            title_screen_manager.process_events(event)

        time_delta = math.ceil(time.time()) - time_delta
        redraw_elements(screen, [background_manager, title_screen_manager], time_delta)

"""
the user can pick the size of their maze
preset sizes are easy, medium, and hard, or they can customize the size in another screen
"""
def pick_size_screen():
    pick_size_screen_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)

    # audio buttons
    button_width = 45
    button_height = button_width
    audio_button_rect = pygame.Rect(
        UI_AREA.right - button_width,   # x
        UI_AREA.top,                    # y
        button_width,                   # width
        button_height                   # height
    )
    audio_button = pygame_gui.elements.UIButton(
        relative_rect=audio_button_rect, 
        text="",
        manager=pick_size_screen_manager,
        object_id=ObjectID(object_id="#audio-button")
    )
    no_audio_button = pygame_gui.elements.UIButton(
        relative_rect=audio_button_rect, 
        text="",
        manager=pick_size_screen_manager,
        object_id=ObjectID(object_id="#no-audio-button")
    )
    set_audio_buttons(audio_button, no_audio_button)
    resize_image('#audio-button', button_width, button_height)
    resize_image('#no-audio-button', button_width, button_height)

    # back button
    back_button_rect = pygame.Rect(
        UI_AREA.left, # x
        UI_AREA.top, # y
        45, # width
        45  # height
    )
    back_button = pygame_gui.elements.UIButton(
        relative_rect=back_button_rect, 
        text="",
        manager=pick_size_screen_manager,
        object_id=ObjectID(class_id="#back-button")
    )
    resize_image('#back-button', back_button_rect.width, back_button_rect.height)
    
    num_buttons = 4
    space_between_buttons = 50
    button_width = UI_AREA.width * 0.6
    all_buttons_height = UI_AREA.height - back_button_rect.height
    button_height = (all_buttons_height + space_between_buttons)/num_buttons - space_between_buttons
    
    # easy button
    easy_button_rect = pygame.Rect(
        UI_AREA.centerx - button_width/2,  # x
        back_button_rect.bottom,        # y
        button_width,                   # width
        button_height                   # height
    )
    easy_button = pygame_gui.elements.UIButton(
        relative_rect=easy_button_rect, 
        text="easy",
        manager=pick_size_screen_manager,
        object_id=ObjectID(class_id="@large-button")
    )
    
    # medium button
    medium_button_rect = pygame.Rect(
        UI_AREA.centerx - button_width/2,  # x
        easy_button_rect.bottom + space_between_buttons,    # y
        button_width,                   # width
        button_height                   # height
    )
    medium_button = pygame_gui.elements.UIButton(
        relative_rect=medium_button_rect, 
        text="medium",
        manager=pick_size_screen_manager,
        object_id=ObjectID(class_id="@large-button")
    )
    
    # hard button
    hard_button_rect = pygame.Rect(
        UI_AREA.centerx - button_width/2,  # x
        medium_button_rect.bottom + space_between_buttons,  # y
        button_width,                   # width
        button_height                   # height
    )
    hard_button = pygame_gui.elements.UIButton(
        relative_rect=hard_button_rect, 
        text="hard",
        manager=pick_size_screen_manager,
        object_id=ObjectID(class_id="@large-button")
    )

    # custom button
    custom_button_rect = pygame.Rect(
        UI_AREA.centerx - button_width/2,  # x
        hard_button_rect.bottom + space_between_buttons,  # y
        button_width,                   # width
        button_height                   # height
    )
    custom_button = pygame_gui.elements.UIButton(
        relative_rect=custom_button_rect, 
        text="custom",
        manager=pick_size_screen_manager,
        object_id=ObjectID(class_id="@large-button")
    )
    resize_image('@large-button', custom_button_rect.width, custom_button_rect.height)

    redraw_elements(screen, [background_manager, pick_size_screen_manager], 0)

    ready = False
    time_delta = math.ceil(time.time())
    while not ready:
        for event in [pygame.event.wait()]+pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            
            # redraw window upon reopening after minimizing
            elif event.type == pygame.WINDOWRESTORED:
                pygame.display.update()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    title_screen()

            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == easy_button:
                    ready = True
                    rows = 10
                    columns = 10
                    play(rows, columns)

                elif event.ui_element == medium_button:
                    ready = True
                    rows = 20
                    columns = 20
                    play(rows, columns)

                elif event.ui_element == hard_button:
                    ready = True
                    rows = 30
                    columns = 30
                    play(rows, columns)

                elif event.ui_element == custom_button:
                    ready = True
                    custom_size_screen()

                elif event.ui_element == back_button:
                    title_screen()
                
                elif event.ui_element == audio_button or event.ui_element == no_audio_button:
                    toggle_audio(audio_file, audio_button, no_audio_button)

            elif event.type == pygame.WINDOWRESTORED: # redraw window upon reopening after minimizing
                pygame.display.update()

            pick_size_screen_manager.process_events(event)
        
        time_delta = math.ceil(time.time()) - time_delta
        redraw_elements(screen, [background_manager, pick_size_screen_manager], time_delta)

"""
custom size screen
- user may pick the dimensions of the maze
- # of rows and # of columns must be no more than 10 units apart
- min = 5, max = 50
"""
def custom_size_screen():
    custom_size_screen_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)

    rows = 15
    columns = 15

    # audio buttons
    button_width = 45
    button_height = button_width
    audio_button_rect = pygame.Rect(
        UI_AREA.right - button_width,   # x
        UI_AREA.top,                    # y
        button_width,                   # width
        button_height                   # height
    )
    audio_button = pygame_gui.elements.UIButton(
        relative_rect=audio_button_rect, 
        text="",
        manager=custom_size_screen_manager,
        object_id=ObjectID(object_id="#audio-button")
    )
    no_audio_button = pygame_gui.elements.UIButton(
        relative_rect=audio_button_rect, 
        text="",
        manager=custom_size_screen_manager,
        object_id=ObjectID(object_id="#no-audio-button")
    )
    set_audio_buttons(audio_button, no_audio_button)
    
    # back button
    back_button_rect = pygame.Rect(
        UI_AREA.left, # x
        UI_AREA.top, # y
        45, # width
        45  # height
    )
    back_button = pygame_gui.elements.UIButton(
        relative_rect=back_button_rect, 
        text="",
        manager=custom_size_screen_manager,
        object_id=ObjectID(class_id="#back-button")
    )
    
    # select dimensions text
    select_text_rect = pygame.Rect(
        UI_AREA.left,
        back_button_rect.bottom,
        UI_AREA.width,
        70
    )
    pygame_gui.elements.UILabel(
        relative_rect=select_text_rect,
        text="Select your Dimensions",
        manager=custom_size_screen_manager,
        object_id=ObjectID(class_id="@medium-text")
    )

    # warning text
    warning_text_rect = pygame.Rect(
        UI_AREA.left,
        select_text_rect.bottom,
        UI_AREA.width,
        25
    )
    pygame_gui.elements.UILabel(
        relative_rect=warning_text_rect,
        text="* dimensions must be within 10 units of each other *",
        manager=custom_size_screen_manager,
        object_id=ObjectID(object_id="@small-text")
    )
    
    # 'x' text
    x_width = UI_AREA.width * 0.1
    x_height = 100
    x_text_rect = pygame.Rect(
        UI_AREA.centerx - x_width/2,
        UI_AREA.centery - x_height/2,
        x_width,
        x_height
    )
    pygame_gui.elements.UILabel(
        relative_rect=x_text_rect,
        text="x",
        manager=custom_size_screen_manager,
        object_id=ObjectID(class_id="@medium-text")
    )
    
    # row text
    text_height = 100
    row_text_rect = pygame.Rect(
        UI_AREA.left,
        UI_AREA.centery - text_height/2,
        x_text_rect.left - UI_AREA.left,
        text_height
    )
    row_text = pygame_gui.elements.UILabel(
        relative_rect=row_text_rect,
        text=str(rows),
        manager=custom_size_screen_manager,
        object_id=ObjectID(class_id="@medium-text")
    )

    # column text
    col_text_rect = pygame.Rect(
        x_text_rect.right,
        UI_AREA.centery - text_height/2,
        UI_AREA.right - x_text_rect.right,
        text_height
    )
    col_text = pygame_gui.elements.UILabel(
        relative_rect=col_text_rect,
        text=str(columns),
        manager=custom_size_screen_manager,
        object_id=ObjectID(class_id="@medium-text")
    )

    # arrows
    arrow_width = 50
    arrow_height = 50

    row_up_arrow_rect = pygame.Rect(
        row_text_rect.centerx - arrow_width/2,
        row_text_rect.top - arrow_height,
        arrow_width,
        arrow_height
    )
    row_up_arrow_button = pygame_gui.elements.UIButton(
        relative_rect=row_up_arrow_rect,
        text="",
        manager=custom_size_screen_manager,
        object_id=ObjectID(object_id="#up-arrow")
    )
    resize_image('#up-arrow', arrow_width, arrow_height)

    row_down_arrow_rect = pygame.Rect(
        row_text_rect.centerx - arrow_width/2,
        row_text_rect.bottom,
        arrow_width,
        arrow_height
    )
    row_down_arrow_button = pygame_gui.elements.UIButton(
        relative_rect=row_down_arrow_rect,
        text="",
        manager=custom_size_screen_manager,
        object_id=ObjectID(object_id="#down-arrow")
    )
    resize_image('#down-arrow', arrow_width, arrow_height)

    column_up_arrow_rect = pygame.Rect(
        col_text_rect.centerx - arrow_width/2,
        col_text_rect.top - arrow_height,
        arrow_width,
        arrow_height
    )
    column_up_arrow_button = pygame_gui.elements.UIButton(
        relative_rect=column_up_arrow_rect,
        text="",
        manager=custom_size_screen_manager,
        object_id=ObjectID(object_id="#up-arrow")
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
        manager=custom_size_screen_manager,
        object_id=ObjectID(object_id="#down-arrow")
    )

    # ratio lock
    lock_button_width = 50
    lock_button_height = 50
    lock_button_rect = pygame.Rect(
        UI_AREA.centerx - lock_button_width/2,
        row_down_arrow_rect.bottom - lock_button_height,
        lock_button_width,
        lock_button_height
    )
    locked_button = pygame_gui.elements.UIButton(
        relative_rect=lock_button_rect,
        text="",
        manager=custom_size_screen_manager,
        object_id=ObjectID(object_id="#locked-button")
    )
    unlocked_button = pygame_gui.elements.UIButton(
        relative_rect=lock_button_rect,
        text="",
        manager=custom_size_screen_manager,
        object_id=ObjectID(object_id="#unlocked-button")
    )
    resize_image('#locked-button', lock_button_width, lock_button_height)
    resize_image('#unlocked-button', lock_button_width, lock_button_height)
    unlocked_button.hide()
    
    # play button
    button_width = math.floor(UI_AREA.width/2)
    button_height = 100
    play_button_rect = pygame.Rect(
        UI_AREA.centerx- button_width/2, # x
        UI_AREA.bottom - button_height - 50, # y
        button_width,   # width
        button_height   # height
    )
    play_button = pygame_gui.elements.UIButton(
        relative_rect=play_button_rect, 
        text="",
        manager=custom_size_screen_manager,
        object_id=ObjectID(class_id="#play-button")
    )

    row_min = 5
    row_max = 35
    col_min = 5
    col_max = 35

    max_diff = 10

    ready = False
    locked = True # if True, rows and cols change simultaneously
    redraw_elements(screen, [background_manager, custom_size_screen_manager], 0)
    time_delta = math.ceil(time.time())
    while not ready:
        for event in [pygame.event.wait()]+pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # redraw window upon reopening after minimizing
            elif event.type == pygame.WINDOWRESTORED:
                pygame.display.update()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    title_screen()

            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_button:
                    pick_size_screen()

                elif event.ui_element == audio_button or event.ui_element == no_audio_button:
                    toggle_audio(audio_file, audio_button, no_audio_button)

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
                    play(rows, columns)
                    break

                elif locked:
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
            
            custom_size_screen_manager.process_events(event)

        time_delta = math.ceil(time.time()) - time_delta
        redraw_elements(screen, [background_manager, custom_size_screen_manager], time_delta)


def pause_menu():
    # all interactive elements will have this manager
    interactive_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)

    # all non-interactive elements will have this manager
    menu_background_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)

    overlay_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)
    margin = 40

    # overlay
    overlay_rect = pygame.Rect(
        0,
        0,
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )
    pygame_gui.elements.UIPanel(
        relative_rect=overlay_rect,
        manager=overlay_manager,
        object_id=ObjectID(object_id="#screen-overlay")
    )
    
    # background rectangle
    menu_width = math.floor(UI_AREA.width * 0.66)
    menu_height = math.floor(UI_AREA.height * 0.5)

    background_rect = pygame.Rect(
        UI_AREA.centerx - menu_width/2, 
        UI_AREA.centery - menu_height/2, 
        menu_width, 
        menu_height
    )
    pygame_gui.elements.UIPanel(
        relative_rect = background_rect,
        manager=menu_background_manager,
        object_id=ObjectID(class_id="#modal-background")
    )

    line_spacing = 10
    button_height = 70
    button_width = background_rect.width-margin*2
    exit_button_rect = pygame.Rect(
        UI_AREA.centerx - button_width/2,
        background_rect.bottom - margin - button_height,
        button_width,
        button_height
    )
    exit_button = pygame_gui.elements.UIButton(
        relative_rect=exit_button_rect,
        text="exit to home screen",
        manager=interactive_manager,
        object_id=ObjectID(class_id="@modal-large-button")
    )
    resize_image('@modal-large-button', button_width, button_height)

    unpause_button_rect = pygame.Rect(
        background_rect.left + margin,
        exit_button_rect.top - button_height - line_spacing,
        button_width,
        button_height
    )
    unpause_button = pygame_gui.elements.UIButton(
        relative_rect=unpause_button_rect,
        text="resume",
        manager=interactive_manager,
        object_id=ObjectID(class_id="@modal-large-button")
    )

    paused_text_rect = pygame.Rect(
        background_rect.left + margin, 
        background_rect.top + margin,
        menu_width - margin*2, 
        unpause_button_rect.top - background_rect.top - margin
    )
    pygame_gui.elements.UILabel(
        relative_rect=paused_text_rect,
        text="paused",
        manager=menu_background_manager,
        object_id=ObjectID(class_id="@medium-text")
    )
    
    paused = True
    time_delta = math.ceil(time.time())
    redraw_elements(screen, [overlay_manager, menu_background_manager, interactive_manager], 0)
    while paused:
        for event in [pygame.event.wait()]+pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame_gui.UI_BUTTON_PRESSED and len(event.__dict__) > 0:
                if event.ui_element == exit_button:
                    paused = False
                    title_screen()

                elif event.ui_element == unpause_button:
                    paused = False

            interactive_manager.process_events(event)

        time_delta = math.ceil(time.time()) - time_delta
        redraw_elements(screen, [menu_background_manager, interactive_manager], time_delta)
        
def finished_menu(message):
    interactive_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)
    menu_background_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)

    margin = 40
    line_spacing = 10

    overlay_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)

    # overlay
    overlay_rect = pygame.Rect(
        0,
        0,
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )
    pygame_gui.elements.UIPanel(
        relative_rect=overlay_rect,
        manager=overlay_manager,
        object_id=ObjectID(object_id="#screen-overlay")
    )
    
    # background surface
    menu_width = math.floor(UI_AREA.width * 0.66)
    menu_height = math.floor(UI_AREA.height * 0.5)
    background_rect = pygame.Rect(
        UI_AREA.centerx - menu_width/2,
        UI_AREA.centery - menu_height/2,
        menu_width,
        menu_height
    )
    pygame_gui.elements.UIPanel(
        relative_rect=background_rect,
        manager=menu_background_manager,
        object_id=ObjectID(class_id="#modal-background")
    )
    
    button_height = 70
    button_width = background_rect.width-margin*2
    
    # exit to home screen button
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
        object_id=ObjectID(class_id="@modal-large-button")
    )

    # play again button
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
        object_id=ObjectID(class_id="@modal-large-button")
    )

    # congrats message
    finished_message_rect = pygame.Rect(
        background_rect.left + margin,
        background_rect.top + margin,
        background_rect.width - margin*2,
        play_button_rect.top - (background_rect.top+margin)
    )
    pygame_gui.elements.UILabel (
        relative_rect=finished_message_rect,
        text=message,
        manager=menu_background_manager,
        object_id=ObjectID(class_id="@medium-text")
    )

    redraw_elements(screen, [overlay_manager, menu_background_manager, interactive_manager], 0)
    
    done = False
    time_delta = math.ceil(time.time())
    while not done:
        for event in [pygame.event.wait()]+pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == exit_button:
                    return False
                if event.ui_element == play_button:
                    return True
            interactive_manager.process_events(event)
        
        time_delta = math.ceil(time.time()) - time_delta
        redraw_elements(screen, [menu_background_manager, interactive_manager], time_delta)

def move_player(direction, player, current_position):
    if direction == "reset":
        player.set_relative_position((startpoint_left, startpoint_top))
        maze[current_position[0]][current_position[1]] = "v"
        current_position = (startpoint[0], startpoint[1])
        maze[current_position[0]][current_position[1]] = "p"
        return current_position

    current_left = player.get_relative_rect().left
    current_top = player.get_relative_rect().top
    if direction == "up" and maze[current_position[0]-1][current_position[1]] == "o":
        player.set_relative_position((current_left, current_top - CELL_HEIGHT))
        maze[current_position[0]][current_position[1]] = "v"
        maze[current_position[0]-2][current_position[1]] = "p"
        current_position = (current_position[0] - 2, current_position[1])

    elif direction == "down" and maze[current_position[0]+1][current_position[1]] == "o":
        player.set_relative_position((current_left, current_top + CELL_HEIGHT))
        maze[current_position[0]][current_position[1]] = "v"
        maze[current_position[0]+2][current_position[1]] = "p"
        current_position = (current_position[0] + 2, current_position[1])

    elif direction == "left" and maze[current_position[0]][current_position[1]-1] == "o":
        player.set_relative_position((current_left - CELL_WIDTH, current_top))
        maze[current_position[0]][current_position[1]] = "v"
        maze[current_position[0]][current_position[1]-2] = "p"
        current_position = (current_position[0], current_position[1] - 2)

    elif direction == "right" and maze[current_position[0]][current_position[1]+1] == "o":
        player.set_relative_position((current_left + CELL_WIDTH, current_top))
        maze[current_position[0]][current_position[1]] = "v"
        maze[current_position[0]][current_position[1]+2] = "p"
        current_position = (current_position[0], current_position[1] + 2)
    return current_position

"""
This function:
1. sets the measurements for CELL_WIDTH, CELL_HEIGHT, and WALL_THICKNESS.
2. resets the maze_topleft to ensure it's centered.
3. MAZE_WIDTH and MAZE_HEIGHT reference the intended width and height,
however, the actual dimensions may be smaller. reset these variables as well
"""
def set_measurements(rows, columns):
    global CELL_WIDTH
    global CELL_HEIGHT
    global MAZE_WIDTH
    global MAZE_HEIGHT
    global WALL_THICKNESS
    global maze_topleft

    CELL_WIDTH = math.floor(MAZE_WIDTH/columns)
    CELL_WIDTH -= CELL_WIDTH%2
    CELL_HEIGHT = math.floor(MAZE_HEIGHT/rows)
    CELL_HEIGHT -= CELL_HEIGHT%2

    WALL_THICKNESS = round(CELL_WIDTH/10)
    WALL_THICKNESS -= WALL_THICKNESS%2
    if (WALL_THICKNESS < 2):
        WALL_THICKNESS = 2

    # set startpoint so the maze is centered
    MAZE_WIDTH = CELL_WIDTH * columns + WALL_THICKNESS
    MAZE_HEIGHT = CELL_HEIGHT * rows + WALL_THICKNESS
    maze_topleft = (UI_AREA.centerx - MAZE_WIDTH/2, UI_AREA.centery - MAZE_HEIGHT/2)

def draw_maze(manager, rows, columns):
    set_measurements(rows, columns)

    x_pos = maze_topleft[0]
    y_pos = maze_topleft[1]
    for i in range(0, rows*2+1):
        for j in range(0, columns*2+1):
            if (i % 2 == 0 and j % 2 == 1): # horizontal
                if (maze[i][j] == 'w'):
                    wall_rect = pygame.Rect(
                        x_pos,
                        y_pos,
                        CELL_WIDTH,
                        WALL_THICKNESS
                    )
                    pygame_gui.elements.UIPanel(
                        relative_rect=wall_rect,
                        manager=manager,
                        object_id=ObjectID(object_id="#wall")
                    )
                x_pos += CELL_WIDTH
            elif (i % 2 == 1 and j % 2 == 0): # vertical
                if (maze[i][j] == 'w'):
                    wall_rect = pygame.Rect(
                        x_pos,
                        y_pos,
                        WALL_THICKNESS,
                        CELL_HEIGHT + WALL_THICKNESS
                    )
                    pygame_gui.elements.UIPanel(
                        relative_rect=wall_rect,
                        manager=manager,
                        object_id=ObjectID(object_id="#wall")
                    )
                x_pos += CELL_WIDTH
        if (i % 2 == 1):
            y_pos += CELL_HEIGHT
        x_pos = maze_topleft[0]

def play(rows, columns):
    solution_stack = None

    game_ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)
    solution_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_file)

    global maze
    mazeInfo = create_maze(rows, columns)
    maze = mazeInfo['maze']
    endpoint = mazeInfo['endpoint']

    draw_maze(game_ui_manager, rows, columns)

    # define starting point
    global startpoint
    startpoint = (random.randrange(0, rows) * 2 + 1, random.randrange(0, columns) * 2 + 1)
    while (startpoint == endpoint):
        startpoint = (random.randrange(0, rows) * 2 + 1, random.randrange(0, columns) * 2 + 1)

    # convert startpoint values from grid indices to maze array indices

    maze[startpoint[0]][startpoint[1]] = "p"
    current_position = (startpoint[0], startpoint[1])
    
    start_rect = pygame.Rect(
        get_cell_x_position(startpoint[1]),
        get_cell_y_position(startpoint[0]),
        CELL_WIDTH - WALL_THICKNESS,
        CELL_HEIGHT - WALL_THICKNESS
    )
    start = pygame_gui.elements.UIPanel(
        relative_rect=start_rect,
        manager=game_ui_manager,
        object_id=ObjectID(object_id="#startpoint")
    )

    end_rect = pygame.Rect(
        get_cell_x_position(endpoint[1]),
        get_cell_y_position(endpoint[0]),
        CELL_WIDTH - WALL_THICKNESS,
        CELL_HEIGHT - WALL_THICKNESS
    )
    end = pygame_gui.elements.UIPanel(
        relative_rect=end_rect,
        manager=game_ui_manager,
        object_id=ObjectID(object_id="#endpoint")
    )

    player_margin = math.ceil(WALL_THICKNESS * 1.5)
    # set player width to be the smaller of CELL_WIDTH and CELL_HEIGHT. defaults to CELL_WIDTH
    if (start_rect.width > start_rect.height):
        player_width = CELL_HEIGHT - player_margin*2
    else:
        player_width = CELL_WIDTH - player_margin*2
    player_height = player_width

    global startpoint_left
    startpoint_left = start_rect.centerx - player_width/2

    global startpoint_top
    startpoint_top = start_rect.centery - player_height/2

    player_rect = pygame.Rect(
        start_rect.centerx - player_width/2,
        start_rect.centery - player_height/2,
        player_width,
        player_height
    )
    player = pygame_gui.elements.UIButton(
        relative_rect=player_rect,
        text="",
        manager=game_ui_manager,
        object_id=ObjectID(object_id="#player")
    )
    player.disable()

    # audio buttons
    button_width = 45
    button_height = button_width
    audio_button_rect = pygame.Rect(
        UI_AREA.right - button_width,   # x
        UI_AREA.top,                    # y
        button_width,                   # width
        button_height                   # height
    )
    audio_button = pygame_gui.elements.UIButton(
        relative_rect=audio_button_rect, 
        text="",
        manager=game_ui_manager,
        object_id=ObjectID(object_id="#audio-button")
    )
    no_audio_button = pygame_gui.elements.UIButton(
        relative_rect=audio_button_rect, 
        text="",
        manager=game_ui_manager,
        object_id=ObjectID(object_id="#no-audio-button")
    )
    set_audio_buttons(audio_button, no_audio_button)
    
    # pause button
    pause_button_width = 45
    pause_button_height = pause_button_width
    pause_button_rect = pygame.Rect(
        audio_button_rect.left - pause_button_width - 20,
        UI_AREA.top,
        pause_button_width,
        pause_button_height
    )
    global pause_button
    pause_button = pygame_gui.elements.UIButton(
        relative_rect=pause_button_rect,
        text="",
        manager=game_ui_manager,
        object_id=ObjectID(object_id="#pause-button")
    )

    # reset button
    reset_button_width = 45
    reset_button_height = reset_button_width
    reset_button_rect = pygame.Rect(
        pause_button_rect.left - reset_button_width - 20,
        UI_AREA.top,
        reset_button_width,
        reset_button_height
    )
    reset_button = pygame_gui.elements.UIButton(
        relative_rect=reset_button_rect,
        text="",
        manager=game_ui_manager,
        object_id=ObjectID(object_id="#reset-button")
    )

    # show solution button
    button_width = math.ceil(UI_AREA.width * 0.3)
    button_height = 45
    show_solution_rect = pygame.Rect(
        UI_AREA.left,
        UI_AREA.top,
        button_width,
        button_height
    )
    show_solution_button = pygame_gui.elements.UIButton(
        relative_rect=show_solution_rect,
        text="show solution",
        manager=game_ui_manager,
        object_id=ObjectID(class_id="#show-solution-button")
    )
    resize_image('#show-solution-button', button_width, button_height)

    # custom event for showing the maze solution
    SHOW_SOLUTION = pygame.USEREVENT + 1

    solution_speed = 10
    increment = 1

    done = False
    solving = False
    redraw_elements(screen, [background_manager, game_ui_manager], 0)
    time_delta = math.ceil(time.time())
    while not done:
        for event in [pygame.event.wait()]+pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()

            # redraw window upon reopening after minimizing
            elif event.type == pygame.WINDOWRESTORED:
                pygame.display.update()

            elif event.type == pygame_gui.UI_BUTTON_PRESSED and len(event.__dict__) > 0:
                if event.ui_element == pause_button:
                    if solving:
                        pygame.time.set_timer(SHOW_SOLUTION, 0)
                    pause_menu()
                    if solving:
                        pygame.time.set_timer(SHOW_SOLUTION, solution_speed)
                elif event.ui_element == reset_button:
                    current_position = move_player("reset", player, current_position)
                elif event.ui_element == audio_button or event.ui_element == no_audio_button:
                    toggle_audio(audio_file, audio_button, no_audio_button)

                elif event.ui_element == show_solution_button:
                    if not solution_stack:
                        solution_stack = solve_maze(maze, startpoint, endpoint)
                    curr_index = 0
                    new_line = True
                    solving = True
                    pygame.time.set_timer(SHOW_SOLUTION, solution_speed)
                    solution_manager.clear_and_reset()
                    show_solution_button.disable()
                    reset_button.disable()

            elif event.type == SHOW_SOLUTION:
                if new_line:
                    if (curr_index == len(solution_stack) - 1):
                        solving = False
                        pygame.time.set_timer(SHOW_SOLUTION, 0)
                        show_solution_button.enable()
                        reset_button.enable()
                    else:
                        curr_cell = solution_stack[curr_index]
                        next_cell = solution_stack[curr_index + 1]
                        line_rect = pygame.Rect(
                            get_cell_x_position(curr_cell[1]) + CELL_WIDTH/2 - WALL_THICKNESS,
                            get_cell_y_position(curr_cell[0]) + CELL_HEIGHT/2 - WALL_THICKNESS,
                            WALL_THICKNESS,
                            WALL_THICKNESS
                        )
                        line = pygame_gui.elements.UIPanel(
                            relative_rect=line_rect,
                            manager=solution_manager,
                            object_id=ObjectID(object_id="#solution-path")
                        )

                        if (curr_cell[1] < next_cell[1]) or (curr_cell[1] > next_cell[1]):   # horizontal
                            target_width = CELL_WIDTH + WALL_THICKNESS
                            target_height = WALL_THICKNESS

                        elif (curr_cell[0] < next_cell[0]) or (curr_cell[0] > next_cell[0]): # vertical
                            target_width = WALL_THICKNESS
                            target_height = CELL_HEIGHT + WALL_THICKNESS

                        new_line = False
                        curr_index += 1
                else:
                    if (curr_cell[1] < next_cell[1]):   # going right
                        line.set_dimensions((line.get_relative_rect().width + increment, line.get_relative_rect().height))

                    elif (curr_cell[1] > next_cell[1]): # going left
                        left = line.get_relative_rect().left
                        line.set_dimensions((line.get_relative_rect().width + increment, line.get_relative_rect().height))
                        line.set_relative_position((left - increment, line.get_relative_rect().top))

                    elif (curr_cell[0] < next_cell[0]): # going down
                        line.set_dimensions((line.get_relative_rect().width, line.get_relative_rect().height + increment))

                    elif (curr_cell[0] > next_cell[0]): # going up
                        top = line.relative_rect.top
                        line.set_dimensions((line.get_relative_rect().width, line.get_relative_rect().height + increment))
                        line.set_relative_position((line.get_relative_rect().left, top - increment))
                    
                    if (line.get_relative_rect().width >= target_width) and (line.get_relative_rect().height >= target_height):
                        line.set_dimensions((target_width, target_height))
                        new_line = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    current_position = move_player("up", player, current_position)

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    current_position = move_player("down", player, current_position)

                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    current_position = move_player("left", player, current_position)
                
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    current_position = move_player("right", player, current_position)
                
                if current_position == (endpoint[0], endpoint[1]):
                    message = "YOU DID IT!"
                    done = True
                    if solving:
                        pygame.time.set_timer(SHOW_SOLUTION, 0)
                        solving = False

            game_ui_manager.process_events(event)

        time_delta = math.ceil(time.time()) - time_delta
        redraw_elements(screen, [background_manager, game_ui_manager, solution_manager], time_delta)
        
    restart = finished_menu(message)
    if restart:
        play(rows, columns)
    else:
        title_screen()

pygame.mixer.music.load(audio_file)
pygame.mixer.music.play(loops=-1)
title_screen()

pygame.quit()
sys.exit()
    