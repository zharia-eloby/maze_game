import pygame, pygame_gui, os
from PIL import Image

class Screen():
    def __init__(self, game_window):
        self.game_window = game_window
        self.ui_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)
    
    def get_background(self):
        background_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)
        background_rect = pygame.Rect(
            0,
            0,
            self.game_window.screen_width,
            self.game_window.screen_height
        )
        
        img_file = os.path.realpath("src/assets/images/background/pixelart_starfield.png")
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
    