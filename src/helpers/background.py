import pygame_gui, pygame, sys, os
from PIL import Image
from pathlib import Path
from helpers.settings import get_settings

settings = get_settings()
screen_width = settings['screen_width']
screen_height = settings['screen_height']
src_path = sys.path[0]
theme_file = os.path.join(src_path, settings['theme']['path'])

def get_background():
    background_manager = pygame_gui.UIManager((screen_width, screen_height), theme_file)
    background_rect = pygame.Rect(
        0,
        0,
        screen_width,
        screen_height
    )
    img_file = Path(__file__).parent / "../assets/images/background/pixelart_starfield.png"
    img = Image.open(img_file)
    img = img.resize((screen_width, screen_height))
    img.save(img_file)
    background = pygame_gui.elements.UIImage(
        relative_rect=background_rect,
        image_surface=pygame.image.load(img_file).convert(),
        manager=background_manager
    )
    return {
        "background_manager": background_manager,
        "background_rect": background_rect,
        "background_element": background
    }