import pygame, pygame_gui, sys, os
from pygame_gui.core import ObjectID

class Audio():
    def __init__(self, game_window):
        self.game_window = game_window
        self.button_width = 45
        self.button_height = 45
        self.audio_button = None
        self.no_audio_button = None
        self.audio_on = game_window.settings['audio']['on']
        self.volume = game_window.settings['audio']['volume']
        self.audio_file = os.path.realpath(game_window.settings['theme']['audio']['path'])
    
    def get_manager(self):
        return self.manager
    
    def initialize(self):
        pygame.mixer.init()
        if self.audio_on:
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(loops=-1)

    def create_audio_buttons(self, screen, ui_manager):
        ui_area = screen.get_drawable_area()
        audio_button_rect = pygame.Rect(
            ui_area.right - self.button_width,
            ui_area.top,
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
        if self.audio_on:
            self.no_audio_button.hide()
        else:
            self.audio_button.hide()

    def turn_on_audio(self):
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        self.no_audio_button.hide()
        self.audio_button.show()
        self.audio_on = True

    def turn_off_audio(self):
        pygame.mixer.music.fadeout(250)
        pygame.mixer.music.unload()
        self.audio_button.hide()
        self.no_audio_button.show()
        self.audio_off = False

    def toggle_audio(self):
        if pygame.mixer.music.get_busy():
            self.turn_off_audio()
        else:
            self.turn_on_audio()

    def get_audio_button_rect(self):
        return self.audio_button.get_relative_rect()