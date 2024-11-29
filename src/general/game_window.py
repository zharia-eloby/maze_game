import pygame, os, json
from screens.title_screen import TitleScreen
from screens.credits_screen import CreditsScreen
from screens.pick_size_screen import PickSizeScreen
from screens.basic_custom_size_screen import BasicCustomSizeScreen
from screens.play_screen import PlayScreen
from screens.settings_screen import SettingsScreen
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
        self.error = False

    def initialize(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_mode([self.settings.screen_width, self.settings.screen_height])
        if self.resize: self.resize_images()
        pygame.display.set_caption('Maze')

    def initialize_screens(self, audio):
        self.title_screen = TitleScreen(self, audio)
        self.title_screen.setup()
        self.loaded_percent = 0.22
        self.credits_screen = CreditsScreen(self, audio)
        self.credits_screen.setup()
        self.loaded_percent = 0.33
        self.pick_size_screen = PickSizeScreen(self, audio)
        self.pick_size_screen.setup()
        self.loaded_percent = 0.44
        self.basic_custom_size_screen = BasicCustomSizeScreen(self, audio)
        self.basic_custom_size_screen.setup()
        self.loaded_percent = 0.55
        self.play_screen = PlayScreen(self, audio)
        self.play_screen.setup()
        self.loaded_percent = 0.66
        self.settings_screen = SettingsScreen(self, audio)
        self.settings_screen.setup()
        self.loaded_percent = 0.77

    def resize_image(self, image_id, width, height, normal=True, hovered=True, disabled=False):
        file = open(self.settings.theme.theme_file, "r")
        contents = json.loads(file.read())
        file.close()
        images_folder = os.path.realpath("src/themes/")
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

    def resize_images(self, all_images=False):
        # background image
        img_file = self.settings.theme.background_image_file
        img = Image.open(img_file)
        img = img.resize((self.settings.screen_width, self.settings.screen_height))
        img.save(img_file)

        # all images
        images = [
            {
                'id': '#settings-cog-button', 
                'width': self.settings.small_sq_button_width,
                'height': self.settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False,
                'must_resize': False
            },
            {
                'id': '#large-play-button', 
                'width': self.settings.large_sq_button_width,
                'height': self.settings.large_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False,
                'must_resize': False
            },
            {
                'id': '#back-button', 
                'width': self.settings.small_sq_button_width,
                'height': self.settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False,
                'must_resize': False
            },
            {
                'id': '@thick-wide-button',
                'width': self.settings.wide_button_width,
                'height': self.settings.thick_wide_button_height,
                'normal': True,
                'hovered': True,
                'disabled': False,
                'must_resize': False
            },
            {
                'id': '@thin-wide-button',
                'width': self.settings.wide_button_width,
                'height': self.settings.thin_wide_button_height,
                'normal': True,
                'hovered': True,
                'disabled': False,
                'must_resize': False
            },
            {
                'id': '@small-rectangle-button',
                'width': self.settings.small_rect_button_width,
                'height': self.settings.small_rect_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': True,
                'must_resize': False
            },
            {
                'id': '#reset-button', 
                'width': self.settings.small_sq_button_width,
                'height': self.settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False,
                'must_resize': False
            },
            {
                'id': '#pause-button', 
                'width': self.settings.small_sq_button_width,
                'height': self.settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False,
                'must_resize': False
            },
            {
                'id': '@modal-wide-button',
                'width': self.settings.modal_wide_button_width,
                'height': self.settings.modal_wide_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False,
                'must_resize': False
            },
            {
                'id': '#home-button', 
                'width': self.settings.small_sq_button_width,
                'height': self.settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False,
                'must_resize': False
            },
            {
                'id': '#play-square-button', 
                'width': self.settings.small_sq_button_width,
                'height': self.settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False,
                'must_resize': False
            }
        ]
        for i in images:
            if all_images or i['must_resize']:
                self.resize_image(i['id'], i['width'], i['height'], i['normal'], i['hovered'], i['disabled'])