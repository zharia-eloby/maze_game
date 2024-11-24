import pygame, pygame_gui
from pygame_gui.core import ObjectID

class Audio():
    def __init__(self, settings):
        self.volume = settings.user_settings['audio']['volume']
        self.audio_on = settings.user_settings['audio']['on']
        self.audio_file = settings.audio_file
        self.background_music_channel = pygame.mixer.Channel(0)
        self.background_music = pygame.mixer.Sound(self.audio_file)
    
    def initialize(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.load(self.audio_file)
        if self.audio_on:
            pygame.mixer.Channel(0).play(self.background_music, loops=-1)

class AudioDisplay(Audio):
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
        self.audio_button.bind(pygame_gui.UI_BUTTON_PRESSED, self.turn_off_audio)
        self.no_audio_button.bind(pygame_gui.UI_BUTTON_PRESSED, self.turn_on_audio)

    def set_audio_display(self):
        if self.background_music_channel.get_busy():
            self.no_audio_button.hide()
            self.audio_button.show()
        else: 
            self.no_audio_button.show()
            self.audio_button.hide()

    def turn_on_audio(self):
        if self.background_music_channel.get_volume() == 0:
            self.background_music_channel.set_volume(1)
        self.background_music_channel.play(self.background_music, loops=-1)
        self.no_audio_button.hide()
        self.audio_button.show()

    def turn_off_audio(self):
        self.background_music_channel.fadeout(250)
        self.audio_button.hide()
        self.no_audio_button.show()

    def set_volume(self, new_volume):
        self.background_music_channel.set_volume(new_volume)
        if new_volume > 0:
            if not self.background_music_channel.get_busy():
                self.background_music_channel.play(self.background_music, loops=-1)
        else:
            self.background_music_channel.fadeout(250)

    def get_audio_button_rect(self):
        return self.audio_button.get_relative_rect()