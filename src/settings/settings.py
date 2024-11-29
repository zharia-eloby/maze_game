import pygame, os, json, logging
from src.general.themes import BlueTheme

class Settings:
    def __init__(self):
        self.log_filename = "maze_game_app.log"
        logging.basicConfig(
            level=logging.DEBUG, 
            datefmt="%B %d, %Y %H:%M:%S", 
            format="%(levelname)s | %(asctime)s | %(filename)s:%(lineno)s | %(message)s",
            filemode='w',
            filename=self.log_filename
        )
        self.version_info = "v2.0.0 Released November 2024"
        
        self.user_settings_file = os.path.realpath("src/settings/user_settings.json")
        self.default_user_settings = {
            "background_audio": {
                "volume": 1.0
            },
            "sound_fx": {
                "volume": 1.0
            }
        }
        self.user_settings = None
        self.theme = BlueTheme()

        self.screen_width = 650
        self.screen_height = 700
        self.line_spacing = 15
        margin = 50
        self.drawable_area = pygame.Rect(
            margin,
            margin,
            self.screen_width - margin*2,
            self.screen_height - margin*2
        )

        self.minimum_dimensions = (5, 5)
        self.maximum_dimensions = (35, 35)
        self.easy_mode_dimensions = (10, 10)
        self.medium_mode_dimensions = (20, 20)
        self.hard_mode_dimensions = (30, 30)

        self.solution_speed_range = (2, 15)

        self.modal_width = round(self.drawable_area.width * 0.7)
        self.modal_height = round(self.drawable_area.height * 0.5)
        self.modal_margin = round(self.modal_width * 0.1)
        self.modal_wide_button_width = self.modal_width - self.modal_margin*2
        self.modal_wide_button_height = round(self.modal_wide_button_width * 0.2)

        self.small_sq_button_width = 50
        self.small_sq_button_height = self.small_sq_button_width
        self.small_rect_button_height = self.small_sq_button_height
        self.small_rect_button_width = round(self.small_rect_button_height * 2)
        self.large_sq_button_width = round(self.drawable_area.width * 0.15)
        self.large_sq_button_height = self.large_sq_button_width
        self.wide_button_width = round(self.drawable_area.width * 0.75)
        self.thick_wide_button_height = round(self.wide_button_width * 0.25)
        self.thin_wide_button_height = round(self.wide_button_width * 0.15)
        self.small_text_height = 21
        self.medium_text_height = 36
        self.slider_height = 30

    def load_settings(self):
        if os.path.exists(self.user_settings_file):
            file = open(self.user_settings_file, 'r')
            self.user_settings = json.loads(file.read())
            file.close()
        else:
            with open(self.user_settings_file, 'w') as file:
                self.user_settings = self.default_user_settings
                json.dump(self.default_user_settings, file, indent=4)
                file.close()

    def save_settings(self):
        with open(self.user_settings_file, 'w') as file:
            json.dump(self.user_settings, file, indent=4)
            file.close()