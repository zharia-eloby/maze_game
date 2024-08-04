import pygame, pygame_gui, math, time
from pygame_gui.core import ObjectID
from classes.screens.screen import Screen
from classes.maze import MazeUI
from classes.modals.pause_modal import PauseModal
from classes.modals.finished_modal import FinishedModal
from classes.modals.show_solution_modal import ShowSolutionModal

class PlayScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window)
        self.audio = audio
        self.maze = None
        self.solution_stack = None
        self.show_solution_button = None
        self.reset_button = None
        self.pause_modal = None
        self.finished_modal = None
        self.show_solution_modal = None
        self.solution_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)
        self.maze_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)
        self.managers = [self.get_background()['background_manager'], self.solution_manager, self.maze_manager, self.ui_manager]

    def set_maze(self, rows, columns):
        self.maze = MazeUI(rows, columns, self.game_window)
        self.maze.setup_maze_ui(self.maze_manager)
    
    def reset(self):
        self.maze.reset_maze()
        self.maze_manager.clear_and_reset()
        self.solution_manager.clear_and_reset()
        self.show_solution_button.enable()
        self.solution_stack = None

    def setup(self):
        self.audio.create_audio_buttons(self.ui_manager)

        self.pause_modal = PauseModal(self.game_window)
        self.pause_modal.setup()

        self.finished_modal = FinishedModal(self.game_window)
        self.finished_modal.setup()

        self.show_solution_modal = ShowSolutionModal(self.game_window)
        self.show_solution_modal.setup()
        
        pause_button_rect = pygame.Rect(
            self.audio.get_audio_button_rect().left - self.game_window.small_sq_button_width - 20,
            self.game_window.drawable_area.top,
            self.game_window.small_sq_button_width,
            self.game_window.small_sq_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=pause_button_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#pause-button")
        )
        
        reset_button_rect = pygame.Rect(
            pause_button_rect.left - self.game_window.small_sq_button_width - 20,
            self.game_window.drawable_area.top,
            self.game_window.small_sq_button_width,
            self.game_window.small_sq_button_height
        )
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=reset_button_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#reset-button")
        )
        
        show_solution_rect = pygame.Rect(
            self.game_window.drawable_area.left,
            self.game_window.drawable_area.top,
            self.game_window.small_rect_button_width,
            self.game_window.small_rect_button_height
        )
        self.show_solution_button = pygame_gui.elements.UIButton(
            relative_rect=show_solution_rect,
            text="give up",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#show-solution-button")
        )

    def show(self):
        self.audio.set_audio_display()
        SHOW_SOLUTION = pygame.USEREVENT + 1

        solution_speed = 10
        increment = 1

        done = False
        next_page = None
        solving = False
        completed = False
        self.game_window.redraw_elements(self.managers, 0)
        time_delta = math.ceil(time.time())
        while not done:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                elif (event.type == pygame_gui.UI_BUTTON_PRESSED) and (len(event.__dict__) > 0):
                    if event.ui_object_id == "#pause-button":
                        if solving:
                            pygame.time.set_timer(SHOW_SOLUTION, 0)
                        resume = self.pause_modal.show()
                        if not resume:
                            pygame.event.clear()
                            self.reset()
                            done = True
                            next_page = self.game_window.title_screen
                        elif solving:
                            pygame.time.set_timer(SHOW_SOLUTION, solution_speed)

                    elif event.ui_object_id == "#reset-button":
                        self.maze.move_player((0, 0))

                    elif event.ui_object_id == "#show-solution-button":
                        give_up = self.show_solution_modal.show()
                        if give_up:
                            if not self.solution_stack:
                                self.solution_stack = self.maze.solve_maze()
                            curr_index = 0
                            new_line = True
                            solving = True
                            pygame.time.set_timer(SHOW_SOLUTION, solution_speed)
                            self.solution_manager.clear_and_reset()
                            self.show_solution_button.disable()

                elif event.type == SHOW_SOLUTION:
                    if new_line:
                        if curr_index == len(self.solution_stack) - 1:
                            solving = False
                            pygame.time.set_timer(SHOW_SOLUTION, 0)
                            self.show_solution_button.enable()
                        else:
                            curr_cell = self.solution_stack[curr_index]
                            next_cell = self.solution_stack[curr_index + 1]

                            ui_position = self.maze.get_cell_ui_position(curr_cell)
                            line_rect = pygame.Rect(
                                ui_position[0] + self.maze.cell_width/2 - self.maze.wall_thickness,
                                ui_position[1] + self.maze.cell_height/2 - self.maze.wall_thickness,
                                self.maze.wall_thickness,
                                self.maze.wall_thickness
                            )
                            line = pygame_gui.elements.UIPanel(
                                relative_rect=line_rect,
                                manager=self.solution_manager,
                                object_id=ObjectID(object_id="#solution-path")
                            )

                            if (curr_cell[1] < next_cell[1]) or (curr_cell[1] > next_cell[1]):   # horizontal
                                target_width = self.maze.cell_width + self.maze.wall_thickness
                                target_height = self.maze.wall_thickness

                            elif (curr_cell[0] < next_cell[0]) or (curr_cell[0] > next_cell[0]): # vertical
                                target_width = self.maze.wall_thickness
                                target_height = self.maze.cell_height + self.maze.wall_thickness

                            new_line = False
                            curr_index += 1
                    else:
                        if curr_cell[1] < next_cell[1]:   # going right
                            line.set_dimensions((line.get_relative_rect().width + increment, line.get_relative_rect().height))

                        elif curr_cell[1] > next_cell[1]: # going left
                            left = line.get_relative_rect().left
                            line.set_dimensions((line.get_relative_rect().width + increment, line.get_relative_rect().height))
                            line.set_relative_position((left - increment, line.get_relative_rect().top))

                        elif curr_cell[0] < next_cell[0]: # going down
                            line.set_dimensions((line.get_relative_rect().width, line.get_relative_rect().height + increment))

                        elif curr_cell[0] > next_cell[0]: # going up
                            top = line.relative_rect.top
                            line.set_dimensions((line.get_relative_rect().width, line.get_relative_rect().height + increment))
                            line.set_relative_position((line.get_relative_rect().left, top - increment))
                        
                        if (line.get_relative_rect().width >= target_width) and (line.get_relative_rect().height >= target_height):
                            line.set_dimensions((target_width, target_height))
                            new_line = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_modal.show()

                    elif (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                        self.maze.move_player((-1, 0))

                    elif (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                        self.maze.move_player((1, 0))

                    elif (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                        self.maze.move_player((0, -1))
                    
                    elif (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                        self.maze.move_player((0, 1))
                    
                    if self.maze.player_position == self.maze.endpoint:
                        completed = True
                        done = True
                        if solving:
                            pygame.time.set_timer(SHOW_SOLUTION, 0)
                            solving = False
                            self.show_solution_button.enable()

                self.ui_manager.process_events(event)

            time_delta = math.ceil(time.time()) - time_delta
            self.game_window.redraw_elements(self.managers, time_delta)
            
        if completed:
            restart = self.finished_modal.show()
            if restart:
                self.reset()
                self.set_maze(self.maze.rows, self.maze.columns)
                next_page = self
            else:
                self.reset()
                next_page = self.game_window.title_screen
        return next_page
