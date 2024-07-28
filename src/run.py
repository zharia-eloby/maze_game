"""
Zharia Eloby
Maze Game with Pygame
"""

import pygame, sys
from classes.game_window import GameWindow
from classes.audio import Audio

gw = GameWindow()
gw.initialize()

audio = Audio(gw)
audio.initialize()

gw.initialize_screens(audio, gw)

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
