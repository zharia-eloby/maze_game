import pygame, os, json
from screens.title_screen import TitleScreen
from screens.credits_screen import CreditsScreen
from screens.pick_size_screen import PickSizeScreen
from screens.custom_size_screen import CustomSizeScreen
from screens.basic_custom_size_screen import BasicCustomSizeScreen
from screens.play_screen import PlayScreen
from screens.settings_screen import SettingsScreen
from general.audio import AudioDisplay
from PIL import Image

class GameWindow:
    def __init__(self, settings):
        self.settings = settings
        self.title_screen = None
        self.credits_screen = None
        self.pick_size_screen = None
        self.custom_size_screen = None
        self.basic_custom_size_screen = None
        self.play_screen = None
        self.settings_screen = None

        self.resize = False

        self.loaded_percent = 0
        self.finished_loading = False

    def initialize(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_mode([self.settings.screen_width, self.settings.screen_height])
        if self.resize: self.resize_images(self.settings)
        pygame.display.set_caption('Maze')

    def initialize_screens(self, audio):
        self.title_screen = TitleScreen(self, AudioDisplay(audio, self.settings))
        self.title_screen.setup()
        self.loaded_percent = 0.3
        self.credits_screen = CreditsScreen(self, AudioDisplay(audio, self.settings))
        self.credits_screen.setup()
        self.loaded_percent = 0.4
        self.pick_size_screen = PickSizeScreen(self, AudioDisplay(audio, self.settings))
        self.pick_size_screen.setup()
        self.loaded_percent = 0.5
        self.custom_size_screen = CustomSizeScreen(self, AudioDisplay(audio, self.settings))
        self.custom_size_screen.setup()
        self.loaded_percent = 0.6
        self.basic_custom_size_screen = BasicCustomSizeScreen(self, AudioDisplay(audio, self.settings))
        self.basic_custom_size_screen.setup()
        self.loaded_percent = 0.7
        self.play_screen = PlayScreen(self, AudioDisplay(audio, self.settings))
        self.play_screen.setup()
        self.loaded_percent = 0.8
        self.settings_screen = SettingsScreen(self, AudioDisplay(audio, self.settings))
        self.settings_screen.setup()
        self.loaded_percent = 0.9

    def resize_image(self, image_id, width, height, normal=True, hovered=True, disabled=False):
        file = open(self.settings.theme_file, "r")
        contents = json.loads(file.read())
        file.close()
        images_folder = os.path.realpath("src/assets/")
        if normal:
            image_file = contents[image_id]['images']['normal_image']['resource']
            img = Image.open(os.path.join(images_folder, image_file))
            img.thumbnail((width, height))
            img.save(os.path.join(images_folder, image_file))
        if hovered:
            image_file = contents[image_id]['images']['hovered_image']['resource']
            img = Image.open(os.path.join(images_folder, image_file))
            img.thumbnail((width, height))
            img.save(os.path.join(images_folder, image_file))
        if disabled:
            image_file = contents[image_id]['images']['disabled_image']['resource']
            img = Image.open(os.path.join(images_folder, image_file))
            img.thumbnail((width, height))
            img.save(os.path.join(images_folder, image_file))

    def resize_images(self):
        # background image
        img_file = self.settings.background_file
        img = Image.open(img_file)
        img = img.resize((self.settings.screen_width, self.settings.screen_height))
        img.save(img_file)

        # all other images
        images = [
            {
                'id': '#settings-cog-button', 
                'width': self.settings.small_sq_button_width,
                'height': self.settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#audio-button', 
                'width': self.settings.small_sq_button_width,
                'height': self.settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#no-audio-button', 
                'width': self.settings.small_sq_button_width,
                'height': self.settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#play-button', 
                'width': self.settings.large_rect_button_width,
                'height': self.settings.large_rect_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#back-button', 
                'width': self.settings.small_sq_button_width,
                'height': self.settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '@thick-wide-button',
                'width': self.settings.wide_button_width,
                'height': self.settings.thick_wide_button_height,
                'normal': True,
                'hovered': True,
                'disabled': False
            },
            {
                'id': '@thin-wide-button',
                'width': self.settings.wide_button_width,
                'height': self.settings.thin_wide_button_height,
                'normal': True,
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#show-solution-button',
                'width': self.settings.small_rect_button_width,
                'height': self.settings.small_rect_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': True
            },
            {
                'id': '#reset-button', 
                'width': self.settings.small_sq_button_width,
                'height': self.settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#pause-button', 
                'width': self.settings.small_sq_button_width,
                'height': self.settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '@modal-wide-button',
                'width': self.settings.modal_wide_button_width,
                'height': self.settings.modal_wide_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            }
        ]
        for i in images:
            self.resize_image(i['id'], i['width'], i['height'], i['normal'], i['hovered'], i['disabled'])