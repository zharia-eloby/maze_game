import pygame, os, sys, json
from classes.title_screen import TitleScreen
from classes.pick_size_screen import PickSizeScreen
from classes.custom_size_screen import CustomSizeScreen
from classes.play_screen import PlayScreen

class GameWindow:
    def __init__(self):
        self.screen_width = 600
        self.screen_height = 700
        self.margin = 50
        self.window = pygame.display.set_mode([self.screen_width, self.screen_height])
        self.settings = self.load_settings()
        self.theme_file = os.path.join(sys.path[0], os.path.relpath(self.settings['theme']['path'], sys.path[0]))
        self.audio = None
        self.title_screen = None
        self.pick_size_screen = None
        self.custom_size_screen = None
        self.play_screen = None

    def initialize(self, audio):
        pygame.init()
        pygame.font.init()
        self.title_screen = TitleScreen(self, audio)
        self.title_screen.setup()
        self.pick_size_screen = PickSizeScreen(self, audio)
        self.pick_size_screen.setup()
        self.custom_size_screen = CustomSizeScreen(self, audio)
        self.custom_size_screen.setup()
        self.play_screen = PlayScreen(self, audio)

    def load_settings(self):
        src_path = sys.path[0]
        file = os.path.join(src_path, os.path.relpath("src/assets/settings.json", sys.path[0]))
        file = open(file, "r")
        contents = json.loads(file.read())
        file.close()
        return contents

    def save_settings(self, updated_content):
        src_path = sys.path[0]
        file = os.path.join(src_path, os.path.relpath("src/assets/settings.json", sys.path[0]))
        file = open(file, "r+")
        file.seek(0)
        json.dump(updated_content, file, indent=4)
        file.truncate()
        file.close()