import pygame

def set_audio_buttons(audio_button, no_audio_button):
    if pygame.mixer.music.get_busy():
        audio_button.show()
        no_audio_button.hide()
    else:
        no_audio_button.show()
        audio_button.hide()

def toggle_audio(audio_file, audio_button, no_audio_button):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(250)
        pygame.mixer.music.unload()
        audio_button.hide()
        no_audio_button.show()
    else:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        no_audio_button.hide()
        audio_button.show()