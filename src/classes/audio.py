import pygame, pygame_gui, os
from pygame_gui.core import ObjectID

class Audio():
    def __init__(self, game_window):
        self.game_window = game_window
        self.volume = game_window.settings['audio']['volume']
        self.audio_file = os.path.realpath(game_window.settings['theme']['audio']['path'])
    
    def initialize(self):
        pygame.mixer.init()
        if self.volume > 0:
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(loops=-1)

class AudioDisplay(Audio):
    def __init__(self, parent, game_window):
        super().__init__(game_window)
        self.button_width = 45
        self.button_height = 45
        self.audio_button = None
        self.no_audio_button = None
        self.audio = parent

    def create_audio_buttons(self, ui_manager):
        audio_button_rect = pygame.Rect(
            self.game_window.drawable_area.right - self.button_width,
            self.game_window.drawable_area.top,
            self.button_width,
            self.button_height
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
        if pygame.mixer.music.get_busy():
            self.no_audio_button.hide()
            self.audio_button.show()
        else: 
            self.no_audio_button.show()
            self.audio_button.hide()

    def turn_on_audio(self):
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(loops=-1)
        self.no_audio_button.hide()
        self.audio_button.show()

    def turn_off_audio(self):
        pygame.mixer.music.fadeout(250)
        pygame.mixer.music.unload()
        self.audio_button.hide()
        self.no_audio_button.show()

    def toggle_audio(self):
        if pygame.mixer.music.get_busy():
            self.turn_off_audio()
        else:
            self.turn_on_audio()

    def get_audio_button_rect(self):
        return self.audio_button.get_relative_rect()