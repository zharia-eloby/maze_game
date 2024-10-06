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
    audio = Audio(game_window)
    audio.initialize()
    game_window.initialize_screens(audio, settings)
    game_window.finished_loading = True

def show_loading_screen(game_window, settings):
    loading_screen = LoadingScreen(game_window, settings)
    loading_screen.setup()
    loading_screen.show()

def run():
    settings = Settings()

    gw = GameWindow(settings)
    gw.initialize()

    load_content_thread = threading.Thread(target=load_content, args=(gw,settings))
    loading_screen_thread = threading.Thread(target=show_loading_screen, args=(gw,settings))
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

    gw.settings['audio']['volume'] = pygame.mixer.music.get_volume()
    gw.settings['audio']['on'] = pygame.mixer.music.get_busy()
    gw.save_settings()

    pygame.quit()
    sys.exit()

run()
