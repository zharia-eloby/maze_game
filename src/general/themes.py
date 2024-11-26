import os

class Theme():
    def __init__(self):
        self.theme_file_path = "src/themes/{theme}/theme.json"
        self.background_audio_file_path = "src/themes/{theme}/audio/{audio}"
        self.button_pressed_sound_effect_file_path = "src/themes/{theme}/audio/{sound_fx}"
        self.victory_sound_effect_file_path = "src/themes/{theme}/audio/{sound_fx}"
        self.background_image_file_path = "src/themes/{theme}/images/background/{background}"


class BlueTheme(Theme):
    def __init__(self):
        super().__init__()
        self.theme_name = "blue"
        self.background_image = "pixelart_starfield.png"
        self.background_audio = "Lost in the Dessert.wav"
        self.button_pressed_sound_effect = "UI_button14.wav"
        self.victory_sound_effect = "Retro Event Acute 08.wav"

        self.theme_file = os.path.realpath(str.format(self.theme_file_path, theme=self.theme_name))
        self.background_image_file = os.path.realpath(str.format(
            self.background_image_file_path, 
            theme=self.theme_name, 
            background=self.background_image
        ))
        self.background_audio_file = os.path.realpath(str.format(
            self.background_audio_file_path, 
            theme=self.theme_name, 
            audio=self.background_audio
        ))
        self.button_pressed_sound_effect_file = os.path.realpath(str.format(
            self.button_pressed_sound_effect_file_path, 
            theme=self.theme_name, 
            sound_fx=self.button_pressed_sound_effect
        ))
        self.victory_sound_effect_file = os.path.realpath(str.format(
            self.victory_sound_effect_file_path, 
            theme=self.theme_name,
            sound_fx=self.victory_sound_effect
        ))