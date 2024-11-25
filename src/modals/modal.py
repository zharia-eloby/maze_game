import pygame_gui
from screens.screen import Screen

class Modal(Screen):
    def __init__(self, settings, audio):
        self.settings = settings
        self.audio = audio
        self.overlay_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme.theme_file)
        self.background_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme.theme_file)
        self.ui_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme.theme_file)