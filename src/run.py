"""
Zharia Eloby
Maze Game with Pygame
"""

import pygame, sys
from classes.game_window import GameWindow
from classes.audio import Audio

gw = GameWindow()
audio = Audio(gw)
gw.initialize(audio)
audio.initialize()

next_page = gw.title_screen
done = False
while not done:
    next_page = next_page.show()

pygame.quit()
sys.exit()
