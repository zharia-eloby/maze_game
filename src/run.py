"""
Zharia Eloby
Maze Game with Pygame
"""

import pygame, sys, threading
from general.settings import Settings
from general.game_window import GameWindow
from screens.loading_screen import LoadingScreen
from general.audio import Audio

def load_content(game_window, settings):
    audio = Audio(settings)
    game_window.loaded_percent = 0.1
    audio.initialize()
    game_window.loaded_percent = 0.2
    game_window.initialize_screens(audio)
    game_window.loaded_percent = 1
    game_window.finished_loading = True

def show_loading_screen(game_window):
    loading_screen = LoadingScreen(game_window)
    loading_screen.setup()
    loading_screen.show()

def run():
    settings = Settings()
    settings.load_settings()

    gw = GameWindow(settings)
    gw.initialize()

    load_content_thread = threading.Thread(target=load_content, args=(gw,settings))
    loading_screen_thread = threading.Thread(target=show_loading_screen, args=(gw,))
    load_content_thread.start()
    loading_screen_thread.start()
    load_content_thread.join()
    loading_screen_thread.join()

    pygame.event.clear()

    next_page = gw.title_screen
    done = False
    while not done:
        next_page = next_page.show()
        if not next_page:
            done = True

    settings.user_settings['audio']['volume'] = pygame.mixer.music.get_volume()
    settings.user_settings['audio']['on'] = pygame.mixer.music.get_busy()
    settings.save_settings()

    pygame.quit()
    sys.exit()

run()
