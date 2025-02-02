import pygame, pygame_gui, pytest
from app.src.general.maze import MazeUI
from app.src.general.settings import Settings
from tests.maze.helpers.mock_maze import get_example_maze
from unittest.mock import patch

@pytest.fixture
def mock_settings():
    class MockSettings(Settings):
        def __init__(self):
            super().__init__()
            self.screen_width = 500
            self.screen_height = 500
            margin = 50
            self.drawable_area = pygame.Rect(
                margin,
                margin,
                self.screen_width - margin*2,
                self.screen_height - margin*2
            )
    return MockSettings()

@pytest.fixture
def mock_maze_ui(mock_settings):
    class MockMazeUI(MazeUI):
        def __init__(self):
            super().__init__((5, 5), mock_settings, True)
            self.maze = get_example_maze().maze
            self.cell_width = 80
            self.cell_height = 80
            self.wall_thickness = 8
            self.maze_area_rect = pygame.Rect(
                0,
                0,
                500,
                500
            )
            self.player = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(
                    0,
                    0,
                    50,
                    50
                ),
                manager=self.maze_manager
            )
            self.player_position = self.maze[1][2]
    return MockMazeUI()

@pytest.fixture(autouse=True)
def setup_teardown():
    pygame.init()
    pygame.font.init()
    yield 
    pygame.quit()

def test_set_ui_element_sizes(mock_settings):
    maze_ui = MazeUI((5, 10), mock_settings, True)
    maze_ui.set_ui_element_sizes(maze_ui.settings.drawable_area)

    assert maze_ui.cell_width == 40
    assert maze_ui.cell_height == 80
    assert maze_ui.wall_thickness == 4
    assert maze_ui.maze_area_rect.width == 404
    assert maze_ui.maze_area_rect.height == 404
    assert maze_ui.maze_area_rect.bottom == 450
    assert maze_ui.maze_area_rect.left == 48

def test_move_player_right(mock_maze_ui):
    mock_maze_ui.player_position.walls = {'left': False, 'right': True, 'up': True, 'down': False}
    mock_maze_ui.move_player("right")

    assert mock_maze_ui.player_position == mock_maze_ui.maze[1][2]
    assert mock_maze_ui.player.get_relative_rect().topleft == (0, 0)

def test_move_player_up(mock_maze_ui):
    mock_maze_ui.player_position.walls = {'left': False, 'right': True, 'up': True, 'down': False}
    mock_maze_ui.move_player("up")

    assert mock_maze_ui.player_position == mock_maze_ui.maze[1][2]
    assert mock_maze_ui.player.get_relative_rect().topleft == (0, 0)

def test_move_player_left(mock_maze_ui):
    with patch('app.src.general.maze.MazeUI.get_neighbor_cell') as mock_get_neighbor_cell:
        cell = mock_maze_ui.maze[1][1]
        cell.rect = pygame.Rect(0, 0, 50, 50)
        mock_get_neighbor_cell.return_value = cell

        mock_maze_ui.player_position.walls = {'left': False, 'right': True, 'up': True, 'down': False}
        mock_maze_ui.move_player("left")

        assert mock_maze_ui.player_position == mock_maze_ui.maze[1][1]
        assert mock_maze_ui.player.get_relative_rect().topleft == (4, 4)

def test_move_player_down(mock_maze_ui):
    with patch('app.src.general.maze.MazeUI.get_neighbor_cell') as mock_get_neighbor_cell:
        cell = mock_maze_ui.maze[2][2]
        cell.rect = pygame.Rect(0, 0, 50, 50)
        mock_get_neighbor_cell.return_value = cell

        mock_maze_ui.player_position.walls = {'left': False, 'right': True, 'up': True, 'down': False}
        mock_maze_ui.move_player("down")

        assert mock_maze_ui.player_position == mock_maze_ui.maze[2][2]
        assert mock_maze_ui.player.get_relative_rect().topleft == (4, 4)
