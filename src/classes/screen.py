import pygame, pygame_gui
from pathlib import Path
from PIL import Image

class Screen():
    def __init__(self, game_window):
        self.game_window = game_window
        self.drawable_area = pygame.Rect(
            self.game_window.margin,
            self.game_window.margin,
            self.game_window.screen_width - self.game_window.margin*2,
            self.game_window.screen_height - self.game_window.margin*2
        )
        self.ui_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)
    
    def get_drawable_area(self):
        return self.drawable_area
    
    def get_background(self):
        background_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)
        background_rect = pygame.Rect(
            0,
            0,
            self.game_window.screen_width,
            self.game_window.screen_height
        )
        img_file = Path(__file__).parent / "../assets/images/background/pixelart_starfield.png"
        img = Image.open(img_file)
        img = img.resize((self.game_window.screen_width, self.game_window.screen_height))
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
    