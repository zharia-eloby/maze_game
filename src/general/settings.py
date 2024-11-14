import pygame, os, json

class Settings:
    def __init__(self):
        self.settings_file = os.path.realpath("src/general/settings.json")

        self.debug_mode = False

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

        self.modal_width = round(self.drawable_area.width * 0.7)
        self.modal_height = round(self.drawable_area.height * 0.5)
        self.modal_margin = round(self.modal_width * 0.1)
        self.modal_wide_button_width = self.modal_width - self.modal_margin*2
        self.modal_wide_button_height = round(self.modal_wide_button_width * 0.2)

        self.small_sq_button_width = 50
        self.small_sq_button_height = self.small_sq_button_width
        self.small_rect_button_height = self.small_sq_button_height
        self.small_rect_button_width = round(self.small_rect_button_height * 2)
        self.large_rect_button_width = round(self.drawable_area.width * 0.35)
        self.large_rect_button_height = round(self.large_rect_button_width * 0.5)
        self.wide_button_width = round(self.drawable_area.width * 0.75)
        self.thick_wide_button_height = round(self.wide_button_width * 0.25)
        self.thin_wide_button_height = round(self.wide_button_width * 0.15)
        self.small_text_height = 21
        self.medium_text_height = 36
        self.slider_height = 30

        self.theme_file_path = "src/themes/{theme}/theme.json"
        self.audio_file_path = "src/themes/{theme}/audio/{audio}"
        self.background_file_path = "src/themes/{theme}/images/background/{background}"
        self.theme_file = None
        self.audio_file = None
        self.background_file = None
        self.user_settings = None

    def load_settings(self):
        file = open(self.settings_file, "r")
        self.user_settings = json.loads(file.read())
        
        current_theme = self.user_settings['current_theme']
        self.theme_file = os.path.realpath(str.format(self.theme_file_path, theme=current_theme))
        self.audio_file = os.path.realpath(str.format(
            self.audio_file_path, 
            theme=current_theme, 
            audio=self.user_settings['themes'][current_theme]['audio']
        ))
        self.background_file = os.path.realpath(str.format(
            self.background_file_path, 
            theme=current_theme, 
            background=self.user_settings['themes'][current_theme]['background']
        ))
        
        file.close()

    def save_settings(self):
        file = open(self.settings_file, "r+")
        file.seek(0)
        json.dump(self.user_settings, file, indent=4)
        file.truncate()
        file.close()