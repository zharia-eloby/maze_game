import pygame, pygame_gui, pytest
from app.src.general.maze import MazeUI
from app.src.general.settings import Settings
from tests.helpers.mock_maze import get_example_maze

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
    example_maze = get_example_maze()
    
    class MockMazeUI(MazeUI):
        def __init__(self):
            super().__init__((5, 5), mock_settings, True)
            self.maze = example_maze.maze
            self.startpoint = example_maze.startpoint
            self.endpoint = example_maze.endpoint
            self.solution = example_maze.solution
            self.cell_width = 80
            self.cell_height = 80
            self.wall_thickness = 8
            self.maze_area_rect = pygame.Rect(
                0,
                0,
                500,
                500
            )
            self.player_position = self.maze[1][2]
            self.player = pygame_gui.elements.UIPanel(
                relative_rect=self.player_position.rect,
                manager=self.maze_manager
            )
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

@pytest.mark.parametrize("cell_coordinates, expected_call_count", [
    pytest.param(
        (0, 0),
        3,
        id="when cell is in the first row and first column"
    ),
    pytest.param(
        (2, 4),
        2,
        id="when only the 'right' and 'down' walls should be drawn"
    ),
    pytest.param(
        (1, 3),
        0,
        id="when cell has no walls"
    )
])
def test_draw_walls(mocker, mock_maze_ui, cell_coordinates, expected_call_count):
    spy = mocker.spy(pygame_gui.elements, "UIPanel")
    cell = mock_maze_ui.maze[cell_coordinates[0]][cell_coordinates[1]]
    mock_maze_ui.draw_walls(cell)

    assert cell.rect is not None
    assert spy.call_count == expected_call_count

def test_draw_maze(mocker, mock_maze_ui):
    spy = mocker.spy(MazeUI, "draw_walls")
    mock_maze_ui.draw_maze()

    assert spy.call_count == 25

def test_set_maze_ui(mocker, mock_settings):
    maze_ui = MazeUI((5, 5), mock_settings, True)

    spy_create_maze = mocker.spy(MazeUI, "create_maze")
    spy_set_ui_element_sizes = mocker.spy(MazeUI, "set_ui_element_sizes")
    spy_draw_maze = mocker.spy(MazeUI, "draw_maze")

    maze_ui.set_maze_ui(mock_settings.drawable_area)

    assert maze_ui.startpoint is not None
    assert spy_create_maze.call_count == 1
    assert spy_set_ui_element_sizes.call_count == 1
    assert spy_draw_maze.call_count == 1

    object_ids = list(map(lambda x: x.object_ids, maze_ui.maze_manager.ui_group))

    assert ["#player"] in object_ids
    assert ["#startpoint"] in object_ids
    assert ["#endpoint"] in object_ids

@pytest.mark.parametrize("direction, expected_player_coordinates, expected_rect_topleft", [
    pytest.param(
        "right",
        (1, 2),
        (100, 50),
        id="when player cannot move in the specified direction"
    ),
    pytest.param(
        "down",
        (2, 2),
        (104, 104),
        id="when player can move in the specified direction"
    )
])
def test_move_player(mock_maze_ui, direction, expected_player_coordinates, expected_rect_topleft):
    mock_maze_ui.move_player(direction)

    expected_row = expected_player_coordinates[0]
    expected_col = expected_player_coordinates[1]
    assert mock_maze_ui.player_position == mock_maze_ui.maze[expected_row][expected_col]
    assert mock_maze_ui.player.get_abs_rect().topleft == expected_rect_topleft

def test_reset_maze(mock_maze_ui):
    mock_maze_ui.reset()

    assert mock_maze_ui.maze == []
    assert mock_maze_ui.cell_width == None
    assert mock_maze_ui.cell_height == None
    assert mock_maze_ui.wall_thickness == None
    assert mock_maze_ui.startpoint == None
    assert mock_maze_ui.endpoint == None
    assert mock_maze_ui.maze_area_rect == pygame.Rect()
    assert mock_maze_ui.player == None
    assert mock_maze_ui.player_position == None
    assert mock_maze_ui.solution == []
    assert len(mock_maze_ui.maze_manager.ui_group) == 1
