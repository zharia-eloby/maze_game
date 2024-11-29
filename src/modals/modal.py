import pygame_gui
from src.screens.screen import Screen

class Modal(Screen):
    def __init__(self, settings, game_window, audio):
        self.settings = settings
        self.game_window = game_window
        self.audio = audio
        self.overlay_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme.theme_file)
        self.background_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme.theme_file)
        self.ui_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme.theme_file)