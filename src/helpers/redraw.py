import pygame

"""
redraws all ui elements on the screen
managers - array of managers that need to draw ui
time_delta - time in seconds since last call to update (as defined by pygame_gui)
"""
def redraw_elements(screen, managers, time_delta):
    for m in managers:
        m.update(time_delta)
        m.draw_ui(screen)
    pygame.display.update()