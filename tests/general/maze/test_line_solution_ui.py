import pytest, pygame, pygame_gui
from app.src.general.settings import Settings
from app.src.general.maze import MazeUI, LineSolutionUI
from tests.helpers.mock_maze import get_mock_maze
from unittest.mock import patch

@pytest.fixture(autouse=True)
def setup_teardown():
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()

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
    example_maze = get_mock_maze()

    class MockMazeUI(MazeUI):
        def __init__(self):
            super().__init__((5, 5), mock_settings, True)
            self.maze = example_maze.maze
            self.startpoint = example_maze.startpoint
            self.endpoint = example_maze.endpoint
            self.solution = example_maze.solution
            self.cell_width = 50
            self.cell_height = 50
            self.wall_thickness = 4
            self.maze_area_rect = pygame.Rect(
                0,
                0,
                250,
                250
            )

        def get_cell(self):
            return self.maze[1][1]

        def get_neighbor(self, direction):
            if direction == "left":
                return self.maze[1][0]
            elif direction == "right":
                return self.maze[1][2]
            elif direction == "up":
                return self.maze[0][1]
            else:
                return self.maze[2][1]

    return MockMazeUI()

@pytest.fixture
def mock_line_solution_ui(mock_maze_ui):
    class MockLineSolutionUI(LineSolutionUI):
        def __init__(self):
            super().__init__(mock_maze_ui, True)

        def populate(self):
            self.index = 5
            self.current_line = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(0, 0, 1, 1),
                manager=self.solution_manager
            )
            self.current_line_target_width = 50
            self.current_line_target_height = 50
            self.current_direction = "right"

    return MockLineSolutionUI()

def test_init(mock_maze_ui):
    line_solution = LineSolutionUI(mock_maze_ui, True)
    assert line_solution.maze_ui == mock_maze_ui
    assert line_solution.increment == 1
    assert line_solution.index == 0
    assert line_solution.current_line == None
    assert line_solution.current_line_target_width == None
    assert line_solution.current_line_target_height == None
    assert line_solution.current_direction == None
    assert line_solution.line_width_thickness == 4
    assert line_solution.line_height_thickness == 4
    assert type(line_solution.solution_manager) == pygame_gui.UIManager

@pytest.mark.parametrize("should_draw_full_line, direction, expected_topleft, expected_size", [
    pytest.param(
        True,
        "left",
        (25, 75),
        (54, 4),
        id="when the direction is 'left' and drawing the full line"
    ),
    pytest.param(
        True,
        "right",
        (75, 75),
        (54, 4),
        id="when the direction is 'right' and drawing the full line"
    ),
    pytest.param(
        True,
        "up",
        (75, 25),
        (4, 54),
        id="when the direction is 'up' and drawing the full line"
    ),
    pytest.param(
        True,
        "down",
        (75, 75),
        (4, 54),
        id="when the direction is 'down' and drawing the full line"
    ),
    pytest.param(
        False,
        "left",
        (75, 75),
        (4, 4),
        id="when the direction is 'left' and initializing line"
    ),
    pytest.param(
        False,
        "right",
        (75, 75),
        (4, 4),
        id="when the direction is 'right' and initializing line"
    ),
    pytest.param(
        False,
        "up",
        (75, 75),
        (4, 4),
        id="when the direction is 'up' and initializing line"
    ),
    pytest.param(
        False,
        "down",
        (75, 75),
        (4, 4),
        id="when the direction is 'down' and initializing line"
    )
])
def test_draw_next_segment(mock_maze_ui, mock_line_solution_ui, should_draw_full_line, direction, expected_topleft, expected_size):
    with patch('app.src.general.maze.Cell.get_direction_to_neighbor') as mock_current_direction:
        mock_current_direction.return_value = direction
        cell = mock_maze_ui.get_cell()
        neighbor = mock_maze_ui.get_neighbor(direction)
        
        mock_line_solution_ui.draw_next_segment(should_draw_full_line, cell, neighbor)
        assert type(mock_line_solution_ui.current_line) == pygame_gui.elements.UIPanel
        assert mock_line_solution_ui.current_line.relative_rect.topleft == expected_topleft
        assert mock_line_solution_ui.current_line.relative_rect.size == expected_size

@pytest.mark.parametrize("starting_rect, direction, expected_rect", [
    pytest.param(
        pygame.Rect(0, 0, 4, 10),
        "left",
        pygame.Rect(-1, 0, 5, 10),
        id="animating the current line when the direction is 'left'"
    ),
    pytest.param(
        pygame.Rect(0, 0, 4, 10),
        "right",
        pygame.Rect(0, 0, 5, 10),
        id="animating the current line when the direction is 'right'"
    ),
    pytest.param(
        pygame.Rect(0, 0, 4, 10),
        "up",
        pygame.Rect(0, -1, 4, 11),
        id="animating the current line when the direction is 'up'"
    ),
    pytest.param(
        pygame.Rect(0, 0, 4, 10),
        "down",
        pygame.Rect(0, 0, 4, 11),
        id="animating the current line when the direction is 'down'"
    )
])
def test_animate(mocker, mock_line_solution_ui, starting_rect, direction, expected_rect):
    with patch('app.src.general.maze.LineSolutionUI.draw_next_segment') as mock_draw_next_segment:
        mock_draw_next_segment.return_value = None
        spy = mocker.spy(LineSolutionUI, "draw_next_segment")
        mock_line_solution_ui.current_line = pygame_gui.elements.UIPanel(
            relative_rect=starting_rect
        )
        mock_line_solution_ui.current_direction = direction
        mock_line_solution_ui.current_line_target_width = 6
        mock_line_solution_ui.current_line_target_height = 10

        animate_return_value = mock_line_solution_ui.animate()
        assert animate_return_value == False
        assert mock_line_solution_ui.current_line.get_relative_rect() == expected_rect
        assert mock_line_solution_ui.index == 0
        assert spy.call_count == 0

def test_animate_new_line(mocker, mock_line_solution_ui):
    with patch('app.src.general.maze.LineSolutionUI.draw_next_segment') as mock_draw_next_segment:
        mock_draw_next_segment.return_value = None
        spy = mocker.spy(LineSolutionUI, "draw_next_segment")
        solution = mock_line_solution_ui.maze_ui.solution

        animate_return_value = mock_line_solution_ui.animate()
        spy.assert_called_once_with(False, solution[0], solution[1])
        assert animate_return_value == False

def test_animate_finish_line(mocker, mock_line_solution_ui):
    spy = mocker.spy(LineSolutionUI, "draw_next_segment")
    mock_line_solution_ui.current_line = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect(0, 0, 4, 10)
    )
    line = mock_line_solution_ui.current_line
    mock_line_solution_ui.current_direction = "left"
    mock_line_solution_ui.current_line_target_width = 5
    mock_line_solution_ui.current_line_target_height = 10

    animate_return_value = mock_line_solution_ui.animate()
    assert line.get_relative_rect() == pygame.Rect(-1, 0, 5, 10)
    assert mock_line_solution_ui.current_line is None
    assert mock_line_solution_ui.index == 1
    assert animate_return_value == False
    assert spy.call_count == 0

def test_animate_completed_solution(mocker, mock_line_solution_ui):
    spy = mocker.spy(LineSolutionUI, "draw_next_segment")
    mock_line_solution_ui.index = 9
    mock_line_solution_ui.current_line = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect(0, 0, 4, 10)
    )
    line = mock_line_solution_ui.current_line
    mock_line_solution_ui.current_direction = "left"
    mock_line_solution_ui.current_line_target_width = 5
    mock_line_solution_ui.current_line_target_height = 10

    animate_return_value = mock_line_solution_ui.animate()
    assert line.get_relative_rect() == pygame.Rect(-1, 0, 5, 10)
    assert mock_line_solution_ui.current_line is None
    assert mock_line_solution_ui.index == 10
    assert animate_return_value == True
    assert spy.call_count == 0

def test_draw_complete_path(mocker, mock_line_solution_ui):
    with patch('app.src.general.maze.LineSolutionUI.draw_next_segment') as mock_draw_next_segment:
        mock_draw_next_segment.return_value = None
        spy = mocker.spy(LineSolutionUI, "draw_next_segment")

        mock_line_solution_ui.draw_complete_path()
        assert spy.call_count == 9

def test_reset(mock_line_solution_ui):
    mock_line_solution_ui.populate()

    mock_line_solution_ui.reset()
    assert mock_line_solution_ui.index == 0
    assert mock_line_solution_ui.current_line == None
    assert mock_line_solution_ui.current_line_target_width == None
    assert mock_line_solution_ui.current_line_target_height == None
    assert mock_line_solution_ui.current_direction == None
    assert len(mock_line_solution_ui.solution_manager.ui_group) == 1
