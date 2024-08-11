"""
Zharia Eloby
Maze Game with Pygame
"""

import pygame, sys, threading
from classes.game_window import GameWindow
from classes.screens.loading_screen import LoadingScreen
from classes.audio import Audio

gw = GameWindow()
gw.initialize()

def load_content():
    audio = Audio(gw)
    audio.initialize()
    gw.initialize_screens(audio, gw)
    gw.finished_loading = True

def show_loading_screen():
    loading_screen = LoadingScreen(gw)
    loading_screen.setup()
    loading_screen.show()

load_content_thread = threading.Thread(target=load_content)
loading_screen_thread = threading.Thread(target=show_loading_screen)
load_content_thread.start()
loading_screen_thread.start()
load_content_thread.join()
loading_screen_thread.join()

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
