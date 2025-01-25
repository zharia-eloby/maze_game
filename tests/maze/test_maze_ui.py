#!/usr/bin/env python
import pygame, pytest
from app.src.general.maze import MazeUI
from app.src.general.settings import Settings

@pytest.fixture
def settings():
    settings = Settings()
    settings.user_settings = settings.default_user_settings
    settings.screen_width = 500
    settings.screen_height = 500
    settings.line_spacing = 10
    margin = 50
    settings.drawable_area = pygame.Rect(
        margin,
        margin,
        settings.screen_width - margin*2,
        settings.screen_height - margin*2
    )
    return settings

@pytest.fixture(autouse=True)
def setup_teardown():
    pygame.init()
    pygame.font.init()
    yield 
    pygame.quit()

def test_set_ui_element_sizes(settings):
    maze_ui = MazeUI((5, 10), settings, True)
    maze_ui.set_ui_element_sizes(maze_ui.settings.drawable_area)

    assert maze_ui.cell_width == 40
    assert maze_ui.cell_height == 80
    assert maze_ui.wall_thickness == 4
    assert maze_ui.maze_area_rect.width == 404
    assert maze_ui.maze_area_rect.height == 404
    assert maze_ui.maze_area_rect.bottom == 450
    assert maze_ui.maze_area_rect.left == 4