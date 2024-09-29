import pygame, pygame_gui, os
from pygame_gui.core import ObjectID

class Audio():
    def __init__(self, game_window):
        self.game_window = game_window
        self.volume = game_window.settings['audio']['volume']
        self.audio_on = game_window.settings['audio']['on']
        self.audio_file = os.path.realpath(game_window.settings['themes'][game_window.settings['current_theme']]['audio']['path'])
    
    def initialize(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)
        if self.audio_on:
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play(loops=-1)

class AudioDisplay(Audio):
    def __init__(self, parent, game_window):
        super().__init__(game_window)
        self.audio_button = None
        self.no_audio_button = None
        self.audio = parent

    def create_audio_buttons(self, ui_manager):
        audio_button_rect = pygame.Rect(
            self.game_window.drawable_area.right - self.game_window.small_sq_button_width,
            self.game_window.drawable_area.top,
            self.game_window.small_sq_button_width,
            self.game_window.small_sq_button_height
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
        if pygame.mixer.music.get_volume() == 0:
            pygame.mixer.music.set_volume(1)
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.play(loops=-1)
        self.no_audio_button.hide()
        self.audio_button.show()

    def turn_off_audio(self):
        pygame.mixer.music.fadeout(250)
        pygame.mixer.music.unload()
        self.audio_button.hide()
        self.no_audio_button.show()

    def set_volume(self, new_volume):
        pygame.mixer.music.set_volume(new_volume)
        if new_volume > 0:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(self.audio.audio_file)
                pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.fadeout(250)
            pygame.mixer.music.unload()

    def get_audio_button_rect(self):
        return self.audio_button.get_relative_rect()