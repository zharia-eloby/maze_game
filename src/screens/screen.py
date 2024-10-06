import pygame, pygame_gui, os
from PIL import Image

class Screen():
    def __init__(self, game_window, settings):
        self.settings = settings
        self.game_window = game_window
        self.ui_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme_file)
        self.background_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme_file)
    
    def set_background(self):
        background_rect = pygame.Rect(
            0,
            0,
            self.settings.screen_width,
            self.settings.screen_height
        )
        
        img_file = os.path.realpath(self.settings.user_settings['themes'][self.settings.user_settings['current_theme']]['background'])
        """
        img = Image.open(img_file)
        img = img.resize((self.settings.screen_width, self.settings.screen_height))
        img.save(img_file)
        """
        
        pygame_gui.elements.UIImage(
            relative_rect=background_rect,
            image_surface=pygame.image.load(img_file).convert(),
            manager=self.background_manager
        )
    