import pygame_gui
from screens.screen import Screen

class Modal(Screen):
    def __init__(self, game_window):
        super().__init__(game_window)
        self.overlay_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)