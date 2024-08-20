"""
Zharia Eloby
Maze Game with Pygame
"""

import pygame, sys, threading
from classes.game_window import GameWindow
from classes.screens.loading_screen import LoadingScreen
from classes.audio import Audio

def load_content(game_window):
    audio = Audio(game_window)
    audio.initialize()
    game_window.initialize_screens(audio, game_window)
    game_window.finished_loading = True

def show_loading_screen(game_window):
    loading_screen = LoadingScreen(game_window)
    loading_screen.setup()
    loading_screen.show()

def run():
    gw = GameWindow()
    gw.initialize()

    load_content_thread = threading.Thread(target=load_content, args=(gw,))
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

    gw.settings['audio']['volume'] = pygame.mixer.music.get_volume()
    gw.settings['audio']['on'] = pygame.mixer.music.get_busy()
    gw.save_settings()

    pygame.quit()
    sys.exit()

run()
