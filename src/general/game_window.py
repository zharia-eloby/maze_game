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
        self.title_screen = None
        self.credits_screen = None
        self.pick_size_screen = None
        self.custom_size_screen = None
        self.basic_custom_size_screen = None
        self.play_screen = None
        self.settings_screen = None

        self.resize = False

        self.finished_loading = False

    def initialize(self, settings):
        pygame.init()
        pygame.font.init()
        pygame.display.set_mode([settings.screen_width, settings.screen_height])
        if self.resize: self.resize_images(settings)
        pygame.display.set_caption('Maze')

    def initialize_screens(self, audio, settings):
        self.title_screen = TitleScreen(self, settings, AudioDisplay(audio, settings))
        self.title_screen.setup()
        self.credits_screen = CreditsScreen(self, settings, AudioDisplay(audio, settings))
        self.credits_screen.setup()
        self.pick_size_screen = PickSizeScreen(self, settings, AudioDisplay(audio, settings))
        self.pick_size_screen.setup()
        self.custom_size_screen = CustomSizeScreen(self, settings, AudioDisplay(audio, settings))
        self.custom_size_screen.setup()
        self.basic_custom_size_screen = BasicCustomSizeScreen(self, settings, AudioDisplay(audio, settings))
        self.basic_custom_size_screen.setup()
        self.play_screen = PlayScreen(self, settings, AudioDisplay(audio, settings))
        self.play_screen.setup()
        self.settings_screen = SettingsScreen(self, settings, AudioDisplay(audio, settings))
        self.settings_screen.setup()

    def resize_image(self, settings, image_id, width, height, normal=True, hovered=True, disabled=False):
        file = open(settings.theme_file, "r")
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

    def resize_images(self, settings):
        # background image
        img_file = os.path.realpath(settings.user_settings['themes'][settings.user_settings['current_theme']]['background'])
        img = Image.open(img_file)
        img = img.resize((settings.screen_width, settings.screen_height))
        img.save(img_file)

        # all other images
        images = [
            {
                'id': '#settings-cog-button', 
                'width': settings.small_sq_button_width,
                'height': settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#audio-button', 
                'width': settings.small_sq_button_width,
                'height': settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#no-audio-button', 
                'width': settings.small_sq_button_width,
                'height': settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#play-button', 
                'width': settings.large_rect_button_width,
                'height': settings.large_rect_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#back-button', 
                'width': settings.small_sq_button_width,
                'height': settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '@thick-wide-button',
                'width': settings.wide_button_width,
                'height': settings.thick_wide_button_height,
                'normal': True,
                'hovered': True,
                'disabled': False
            },
            {
                'id': '@thin-wide-button',
                'width': settings.wide_button_width,
                'height': settings.thin_wide_button_height,
                'normal': True,
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#locked-button', 
                'width': settings.small_sq_button_width,
                'height': settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#unlocked-button', 
                'width': settings.small_sq_button_width,
                'height': settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#show-solution-button',
                'width': settings.small_rect_button_width,
                'height': settings.small_rect_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': True
            },
            {
                'id': '#reset-button', 
                'width': settings.small_sq_button_width,
                'height': settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '#pause-button', 
                'width': settings.small_sq_button_width,
                'height': settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '@up-arrow', 
                'width': settings.small_sq_button_width,
                'height': settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '@down-arrow', 
                'width': settings.small_sq_button_width,
                'height': settings.small_sq_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            },
            {
                'id': '@modal-wide-button',
                'width': settings.modal_wide_button_width,
                'height': settings.modal_wide_button_height,
                'normal': True, 
                'hovered': True,
                'disabled': False
            }
        ]
        for i in images:
            self.resize_image(settings, i['id'], i['width'], i['height'], i['normal'], i['hovered'], i['disabled'])