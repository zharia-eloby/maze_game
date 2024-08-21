import pygame, os, json
from classes.screens.title_screen import TitleScreen
from classes.screens.help_screen import HelpScreen
from classes.screens.credits_screen import CreditsScreen
from classes.screens.pick_size_screen import PickSizeScreen
from classes.screens.custom_size_screen import CustomSizeScreen
from classes.screens.basic_custom_size_screen import BasicCustomSizeScreen
from classes.screens.play_screen import PlayScreen
from classes.screens.settings_screen import SettingsScreen
from classes.audio import AudioDisplay
from classes.modals.modal import Modal
from PIL import Image

class GameWindow:
    def __init__(self):
        self.screen_width = 650
        self.screen_height = 700
        self.window = pygame.display.set_mode([self.screen_width, self.screen_height])
        self.margin = 50
        
        self.drawable_area = pygame.Rect(
            self.margin,
            self.margin,
            self.screen_width - self.margin*2,
            self.screen_height - self.margin*2
        )

        self.small_sq_button_width = 50
        self.small_sq_button_height = self.small_sq_button_width
        self.small_rect_button_height = self.small_sq_button_height
        self.small_rect_button_width = round(self.small_rect_button_height * 2)
        self.large_rect_button_width = round(self.drawable_area.width * 0.35)
        self.large_rect_button_height = round(self.large_rect_button_width * 0.5)
        self.wide_button_width = round(self.drawable_area.width * 0.75)
        self.thick_wide_button_height = round(self.wide_button_width * 0.25)
        self.thin_wide_button_height = round(self.wide_button_width * 0.15)
        self.small_text_height = 20
        self.medium_text_height = 35
        self.slider_height = 30

        self.settings = self.load_settings()
        self.theme_file = os.path.realpath(self.settings['theme']['path'])

        self.title_screen = None
        self.credits_screen = None
        self.pick_size_screen = None
        self.custom_size_screen = None
        self.basic_custom_size_screen = None
        self.play_screen = None

        self.resize = True

        self.finished_loading = False

    def initialize(self):
        pygame.init()
        pygame.font.init()
        if self.resize: self.resize_images()
        pygame.display.set_caption('Maze')

    def initialize_screens(self, audio, game_window):
        self.title_screen = TitleScreen(self, AudioDisplay(audio, game_window))
        self.title_screen.setup()
        self.credits_screen = CreditsScreen(self, AudioDisplay(audio, game_window))
        self.credits_screen.setup()
        self.help_screen = HelpScreen(self, AudioDisplay(audio, game_window))
        self.help_screen.setup()
        self.pick_size_screen = PickSizeScreen(self, AudioDisplay(audio, game_window))
        self.pick_size_screen.setup()
        self.custom_size_screen = CustomSizeScreen(self, AudioDisplay(audio, game_window))
        self.custom_size_screen.setup()
        self.basic_custom_size_screen = BasicCustomSizeScreen(self, AudioDisplay(audio, game_window))
        self.basic_custom_size_screen.setup()
        self.play_screen = PlayScreen(self, AudioDisplay(audio, game_window))
        self.play_screen.setup()
        self.settings_screen = SettingsScreen(self, AudioDisplay(audio, game_window))
        self.settings_screen.setup()

    def load_settings(self):
        path = os.path.realpath("src/assets/settings.json")
        file = open(path, "r")
        contents = json.loads(file.read())
        file.close()
        return contents

    def save_settings(self):
        path = os.path.realpath("src/assets/settings.json")
        file = open(path, "r+")
        file.seek(0)
        json.dump(self.settings, file, indent=4)
        file.truncate()
        file.close()

    def redraw_elements(self, managers, time_delta):
        for m in managers:
            m.update(time_delta)
            m.draw_ui(self.window)
        pygame.display.update()

    def resize_image(self, image_id, width, height, normal=True, hovered=True, disabled=False):
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
        if disabled:
            image_file = contents[image_id]['images']['disabled_image']['resource']
            img = Image.open(os.path.join(images_folder, image_file))
            img = img.resize((width, height))
            img.save(os.path.join(images_folder, image_file))

    def resize_images(self):
        images = [
            {
                'id': '#settings-cog-button', 
                'width': self.small_sq_button_width,
                'height': self.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#audio-button', 
                'width': self.small_sq_button_width,
                'height': self.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#no-audio-button', 
                'width': self.small_sq_button_width,
                'height': self.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#play-button', 
                'width': self.large_rect_button_width,
                'height': self.large_rect_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#back-button', 
                'width': self.small_sq_button_width,
                'height': self.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '@thick-wide-button',
                'width': self.wide_button_width,
                'height': self.thick_wide_button_height,
                'normal': True,
                'hovered': True,
                'disabled': False
            },
            {
                'id': '@thin-wide-button',
                'width': self.wide_button_width,
                'height': self.thin_wide_button_height,
                'normal': True,
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#locked-button', 
                'width': self.small_sq_button_width,
                'height': self.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#unlocked-button', 
                'width': self.small_sq_button_width,
                'height': self.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#show-solution-button',
                'width': self.small_rect_button_width,
                'height': self.small_rect_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': True
            },
            {
                'id': '#reset-button', 
                'width': self.small_sq_button_width,
                'height': self.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#pause-button', 
                'width': self.small_sq_button_width,
                'height': self.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '@up-arrow', 
                'width': self.small_sq_button_width,
                'height': self.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '@down-arrow', 
                'width': self.small_sq_button_width,
                'height': self.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '@modal-wide-button',
                'width': Modal(self).modal_wide_button_width,
                'height': Modal(self).modal_wide_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            }
        ]
        for i in images:
            self.resize_image(i['id'], i['width'], i['height'], i['normal'], i['hovered'], i['disabled'])