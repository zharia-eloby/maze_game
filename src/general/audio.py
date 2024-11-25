import pygame, pygame_gui
from pygame_gui.core import ObjectID

class Audio():
    def __init__(self, settings):
        self.background_volume = settings.user_settings["background_audio"]['volume']
        self.background_audio_on = settings.user_settings["background_audio"]['on']
        self.background_audio_file = settings.theme.background_audio_file
        self.background_music_channel = pygame.mixer.Channel(0)
        self.background_music = pygame.mixer.Sound(settings.theme.background_audio_file)

        self.sound_fx_volume = settings.user_settings["sound_fx"]['volume']
        self.sound_fx_channel = pygame.mixer.Channel(1)
        self.button_pressed_sound_effect = pygame.mixer.Sound(settings.theme.button_pressed_sound_effect_file)
        self.victory_sound_effect = pygame.mixer.Sound(settings.theme.victory_sound_effect_file)
    
    def initialize(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.background_audio_file)
        self.background_music_channel.set_volume(self.background_volume)
        if self.background_audio_on:
            self.background_music_channel.play(self.background_music, loops=-1)
        self.sound_fx_channel.set_volume(self.sound_fx_volume)

    def set_background_volume(self, new_volume):
        self.background_music_channel.set_volume(new_volume)
        if new_volume > 0:
            if not self.background_music_channel.get_busy():
                self.background_music_channel.play(self.background_music, loops=-1)
        else:
            self.background_music_channel.fadeout(250)

    def set_sound_fx_volume(self, new_volume):
        self.sound_fx_channel.set_volume(new_volume)

    def turn_on_background_audio(self):
        if self.background_music_channel.get_volume() == 0:
            self.background_music_channel.set_volume(1)
        self.background_music_channel.play(self.background_music, loops=-1)

    def turn_off_background_audio(self):
        self.background_music_channel.fadeout(250)

    def play_sound_effect(self, effect="button_pressed"):
        if effect == "button_pressed": self.sound_fx_channel.play(self.button_pressed_sound_effect)
        elif effect == "victory": self.sound_fx_channel.play(self.victory_sound_effect)

class AudioUI(Audio):
    def __init__(self, parent, settings):
        super().__init__(settings)
        self.audio_button = None
        self.no_audio_button = None
        self.audio = parent

    def create_audio_buttons(self, ui_manager, settings):
        audio_button_rect = pygame.Rect(
            settings.drawable_area.right - settings.small_sq_button_width,
            settings.drawable_area.top,
            settings.small_sq_button_width,
            settings.small_sq_button_height
        )
        self.audio_button = pygame_gui.elements.UIButton(
            relative_rect=audio_button_rect, 
            text="",
            manager=ui_manager,
            object_id=ObjectID(object_id="#audio-button")
        )
        self.no_audio_button = pygame_gui.elements.UIButton(
            relative_rect=audio_button_rect,
            text="",
            manager=ui_manager,
            object_id=ObjectID(object_id="#no-audio-button")
        )
        self.audio_button.bind(pygame_gui.UI_BUTTON_PRESSED, self.turn_off_background_audio)
        self.no_audio_button.bind(pygame_gui.UI_BUTTON_PRESSED, self.turn_on_background_audio)

    def set_audio_display(self):
        if self.background_music_channel.get_busy():
            self.no_audio_button.hide()
            self.audio_button.show()
        else: 
            self.no_audio_button.show()
            self.audio_button.hide()

    def turn_on_background_audio(self):
        super().turn_on_background_audio()
        self.no_audio_button.hide()
        self.audio_button.show()

    def turn_off_background_audio(self):
        super().turn_off_background_audio()
        self.audio_button.hide()
        self.no_audio_button.show()

    def get_audio_button_rect(self):
        return self.audio_button.get_relative_rect()
    