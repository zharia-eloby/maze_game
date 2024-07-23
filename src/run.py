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

gw.initialize_screens(audio)

next_page = gw.title_screen
done = False
while not done:
    next_page = next_page.show()
    if not next_page:
        done = True

pygame.quit()
sys.exit()
