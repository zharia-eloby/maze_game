import pygame_gui
from screens.screen import Screen

class Modal(Screen):
    def __init__(self, game_window, settings):
        super().__init__(game_window, settings)
        self.overlay_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme_file)