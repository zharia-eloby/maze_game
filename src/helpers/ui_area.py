import pygame
from helpers.settings import get_settings

settings = get_settings()
margin = settings['margin']
screen_width = settings['screen_width']
screen_height = settings['screen_height']

def get_ui_area():
    return pygame.Rect(
    margin,
    margin,
    screen_width - margin*2,
    screen_width - margin*2
)