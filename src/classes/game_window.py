import pygame, os, sys, json
from classes.screens.title_screen import TitleScreen
from classes.screens.pick_size_screen import PickSizeScreen
from classes.screens.custom_size_screen import CustomSizeScreen
from classes.screens.play_screen import PlayScreen
from classes.audio import AudioDisplay

class GameWindow:
    def __init__(self):
        self.screen_width = 600
        self.screen_height = 700
        self.margin = 50
        self.window = pygame.display.set_mode([self.screen_width, self.screen_height])
        self.settings = self.load_settings()
        self.theme_file = os.path.realpath(self.settings['theme']['path'])
        self.title_screen = None
        self.pick_size_screen = None
        self.custom_size_screen = None
        self.play_screen = None

    def initialize(self):
        pygame.init()
        pygame.font.init()

    def initialize_screens(self, audio, game_window):
        self.title_screen = TitleScreen(self, AudioDisplay(audio, game_window))
        self.title_screen.setup()
        self.pick_size_screen = PickSizeScreen(self, AudioDisplay(audio, game_window))
        self.pick_size_screen.setup()
        self.custom_size_screen = CustomSizeScreen(self, AudioDisplay(audio, game_window))
        self.custom_size_screen.setup()
        self.play_screen = PlayScreen(self, AudioDisplay(audio, game_window))
        self.play_screen.setup()

    def load_settings(self):
        path = os.path.realpath("src/assets/settings.json")
        file = open(path, "r")
        contents = json.loads(file.read())
        file.close()
        return contents

    def save_settings(self, updated_content):
        path = os.path.realpath("src/assets/settings.json")
        file = open(path, "r+")
        file.seek(0)
        json.dump(updated_content, file, indent=4)
        file.truncate()
        file.close()