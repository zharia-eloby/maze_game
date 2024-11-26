import pygame

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

    def play_sound_effect(self, effect="button_pressed"):
        if effect == "button_pressed": self.sound_fx_channel.play(self.button_pressed_sound_effect)
        elif effect == "victory": self.sound_fx_channel.play(self.victory_sound_effect)
    