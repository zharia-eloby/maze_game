import pygame_gui
from screens.screen import Screen

class Modal(Screen):
    def __init__(self, settings):
        self.settings = settings
        self.overlay_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme_file)
        self.background_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme_file)
        self.ui_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme_file)