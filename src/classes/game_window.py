import pygame, os, math, json
from classes.screens.title_screen import TitleScreen
from classes.screens.pick_size_screen import PickSizeScreen
from classes.screens.custom_size_screen import CustomSizeScreen
from classes.screens.play_screen import PlayScreen
from classes.audio import AudioDisplay
from PIL import Image

class GameWindow:
    def __init__(self):
        self.screen_width = 600
        self.screen_height = 700
        self.window = pygame.display.set_mode([self.screen_width, self.screen_height])
        self.margin = 50
        self.drawable_area = pygame.Rect(
            self.margin,
            self.margin,
            self.screen_width - self.margin*2,
            self.screen_height - self.margin*2
        )
        self.small_sq_button_width = 45
        self.small_sq_button_height = self.small_sq_button_width
        self.small_rect_button_width = math.floor(self.drawable_area.width * 0.3)
        self.small_rect_button_height = self.small_sq_button_height
        self.large_rect_button_width = math.floor(self.drawable_area.width * 0.5)
        self.large_rect_button_height = math.floor(self.drawable_area.height * 0.15)
        self.settings = self.load_settings()
        self.theme_file = os.path.realpath(self.settings['theme']['path'])
        self.title_screen = None
        self.pick_size_screen = None
        self.custom_size_screen = None
        self.play_screen = None
        self.resize_images = True

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

    def redraw_elements(self, managers, time_delta):
        for m in managers:
            m.update(time_delta)
            m.draw_ui(self.window)
        pygame.display.update()

    def resize_image(self, image_id, width, height, normal=True, hovered=True):
        if self.resize_images:
            theme_file = os.path.realpath(self.settings['theme']['path'])
            file = open(theme_file, "r")
            contents = json.loads(file.read())
            file.close()
            images_folder = os.path.realpath("src/assets/images/")
            if normal:
                image_file = contents[image_id]['images']['normal_image']['resource']
                img = Image.open(os.path.join(images_folder, image_file))
                img = img.resize((width, height))
                img = img.save(os.path.join(images_folder, image_file))
            if hovered:
                image_file = contents[image_id]['images']['hovered_image']['resource']
                img = Image.open(os.path.join(images_folder, image_file))
                img = img.resize((width, height))
                img.save(os.path.join(images_folder, image_file))