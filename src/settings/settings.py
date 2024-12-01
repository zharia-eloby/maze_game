import pygame, os, json, logging
from src.general.themes import BlueTheme
from src.general.file_path_helper import get_file_path

class Settings:
    def __init__(self):
        self.log_filename = get_file_path("user/maze_game_app.log", False)
        logging.basicConfig(
            level=logging.DEBUG, 
            datefmt="%B %d, %Y %H:%M:%S", 
            format="%(levelname)s | %(asctime)s | %(filename)s:%(lineno)s | %(message)s",
            filemode='w',
            filename=self.log_filename
        )
        self.version_info = "v2.0.0 Released December 2024"
        
        self.user_settings_file = get_file_path("user/user_settings.json", False)
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

    def has_required_data(self, expected, other):
        if type(expected) != dict: return True

        for key in expected.keys():
            if key not in other:
                return False
            if type(expected[key]) != type(other[key]): 
                return False
            result = self.has_required_data(expected[key], other[key])
            if not result: return result

        return True # this will be reached only if the object is empty

    def is_valid_user_settings(self, loaded_settings):
        if not type(loaded_settings) == dict: return False
        return self.has_required_data(self.default_user_settings, loaded_settings)
    
    def load_settings(self):
        if os.path.exists(self.user_settings_file):
            logging.info("Existing user settings file found")
            with open(self.user_settings_file, 'r') as file:
                try:
                    loaded_settings = json.loads(file.read())
                    if self.is_valid_user_settings(loaded_settings):
                        self.user_settings = loaded_settings
                        logging.info("Loaded user settings from existing file")
                        return
                    else: 
                        logging.info("Existing file does not have required info")
                except json.decoder.JSONDecodeError:
                    logging.info("Error parsing user settings json")
                
        logging.info("Loading default settings")
        with open(self.user_settings_file, 'w') as file:
            json.dump(self.default_user_settings, file, indent=4)
            self.user_settings = self.default_user_settings
        logging.info("Loaded default settings successfully")

    def save_settings(self):
        with open(self.user_settings_file, 'w') as file:
            json.dump(self.user_settings, file, indent=4)
