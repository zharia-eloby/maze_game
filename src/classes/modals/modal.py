import pygame_gui
from classes.screens.screen import Screen

class Modal(Screen):
    def __init__(self, game_window):
        super().__init__(game_window)
        self.overlay_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)
        self.width = round(self.game_window.drawable_area.width * 0.66)
        self.height = round(self.game_window.drawable_area.height * 0.5)
        self.margin = 40
        self.line_spacing = 10
        self.modal_wide_button_width = self.width - self.margin*2
        self.modal_wide_button_height = self.height * 0.2