import pygame, pygame_gui, math, time
from pygame_gui.core import ObjectID
from src.screens.screen import Screen
from src.general.maze import MazeUI, LineSolutionUI
from src.modals.pause_modal import PauseModal
from src.modals.finished_modal import FinishedModal
from src.modals.show_solution_modal import ShowSolutionModal

class PlayScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window, audio)
        self.maze = None
        self.show_solution_button = None
        self.reset_button = None
        self.maze_area_rect = None
        self.pause_modal = None
        self.finished_modal = None
        self.show_solution_modal = None
        self.solution_ui = None
        self.managers = None

    def set_maze(self, dimensions):
        self.maze = MazeUI(dimensions, self.settings)
        self.maze.set_maze_ui(self.maze_area_rect)
        self.solution_ui = LineSolutionUI(self.maze)
        self.managers = [self.background_manager, self.maze.maze_background_manager, self.solution_ui.solution_manager, self.maze.maze_manager, self.ui_manager]
    
    def reset(self):
        self.maze.reset()
        self.solution_ui.reset()
        self.show_solution_button.enable()
        self.skip_solution_animation_button.enable()
        self.skip_solution_animation_button.hide()
        self.managers.clear()

    def setup(self):
        self.log_setup_start()

        self.set_background()

        self.pause_modal = PauseModal(self.settings, self.game_window, self.audio)
        self.pause_modal.setup()

        self.finished_modal = FinishedModal(self.settings, self.game_window, self.audio)
        self.finished_modal.setup()

        self.show_solution_modal = ShowSolutionModal(self.settings, self.game_window, self.audio)
        self.show_solution_modal.setup()
        
        pause_button_rect = pygame.Rect(
            self.settings.drawable_area.right - self.settings.small_sq_button_width,
            self.settings.drawable_area.top,
            self.settings.small_sq_button_width,
            self.settings.small_sq_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=pause_button_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#pause-button")
        )
        
        reset_button_rect = pygame.Rect(
            pause_button_rect.left - self.settings.small_sq_button_width - self.settings.line_spacing,
            self.settings.drawable_area.top,
            self.settings.small_sq_button_width,
            self.settings.small_sq_button_height
        )
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=reset_button_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#reset-button")
        )
        
        show_solution_rect = pygame.Rect(
            self.settings.drawable_area.left,
            self.settings.drawable_area.top,
            self.settings.small_rect_button_width,
            self.settings.small_rect_button_height
        )
        self.show_solution_button = pygame_gui.elements.UIButton(
            relative_rect=show_solution_rect,
            text="Give Up",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#show-solution-button", class_id="@small-rectangle-button")
        )

        skip_solution_animation_rect = pygame.Rect(
            show_solution_rect.right + self.settings.line_spacing,
            show_solution_rect.top,
            self.settings.small_rect_button_width,
            self.settings.small_rect_button_height
        )
        self.skip_solution_animation_button = pygame_gui.elements.UIButton(
            relative_rect=skip_solution_animation_rect,
            text="Skip",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#skip-solution-animation-button", class_id="@small-rectangle-button")
        )
        self.skip_solution_animation_button.hide()

        self.maze_area_rect = pygame.Rect(
            self.settings.drawable_area.left,
            show_solution_rect.bottom + self.settings.line_spacing,
            self.settings.drawable_area.width,
            self.settings.drawable_area.height - show_solution_rect.height - self.settings.line_spacing
        )

        self.log_setup_success()

    def show_modal(self, modal):
        pygame.event.clear()

        if modal == self.pause_modal:
            result = modal.show(self.managers)
        else:
            result = modal.show()

        pygame.event.clear()
        return result
    
    """
    set the solution speed based on the area of the maze
    """
    def get_solution_speed(self):
        min_speed = self.settings.solution_speed_range[0]
        max_speed = self.settings.solution_speed_range[1]

        min_area = self.settings.minimum_dimensions[0] * self.settings.minimum_dimensions[1]
        max_area = self.settings.maximum_dimensions[0] * self.settings.maximum_dimensions[1]
        area = self.maze.dimensions[0] * self.maze.dimensions[1]

        percent_area = (area - min_area)/(max_area - min_area)

        solution_speed = round((max_speed - min_speed) * percent_area + min_speed)
        return solution_speed

    def show(self):
        self.log_display_screen()

        SHOW_SOLUTION = pygame.USEREVENT + 1

        solution_speed = self.get_solution_speed()
        done = False
        next_page = None
        solving = False
        end_reached = False
        self.redraw_elements(self.managers, 0)
        time_delta = math.ceil(time.time())
        while not done:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                elif (event.type == pygame_gui.UI_BUTTON_PRESSED) and (len(event.__dict__) > 0):
                    self.audio.play_sound_effect()
                    if event.ui_object_id == "#pause-button":
                        if solving: 
                            pygame.time.set_timer(SHOW_SOLUTION, 0)
                        next_action = self.show_modal(self.pause_modal)
                        if next_action == "home":
                            self.reset()
                            done = True
                            next_page = self.game_window.title_screen
                            break
                        elif next_action == "exit_game":
                            done = True
                            break
                        elif solving:
                            pygame.time.set_timer(SHOW_SOLUTION, solution_speed)

                    elif event.ui_object_id == "#reset-button":
                        if solving:
                            solving = False
                            pygame.time.set_timer(SHOW_SOLUTION, 0)
                        self.reset()
                        self.set_maze(self.maze.dimensions)

                    elif event.ui_object_id == "#show-solution-button":
                        give_up = self.show_solution_modal.show()
                        if give_up:
                            if len(self.maze.solution) == 0:
                                self.maze.solve_maze()
                            solving = True
                            pygame.time.set_timer(SHOW_SOLUTION, solution_speed)
                            self.show_solution_button.disable()
                            self.skip_solution_animation_button.show()

                    elif event.ui_object_id == "#skip-solution-animation-button":
                        pygame.time.set_timer(SHOW_SOLUTION, 0)
                        solving = False
                        self.skip_solution_animation_button.disable()
                        self.solution_ui.draw_complete_path()

                elif event.type == SHOW_SOLUTION:
                    complete = self.solution_ui.animate()
                    if complete:
                        solving = False
                        pygame.time.set_timer(SHOW_SOLUTION, 0)
                        self.skip_solution_animation_button.disable()
                        break

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if solving: 
                            pygame.time.set_timer(SHOW_SOLUTION, 0)
                        resume = self.show_modal(self.pause_modal)
                        if not resume:
                            self.reset()
                            done = True
                            next_page = self.game_window.title_screen
                            break
                        elif solving:
                            pygame.time.set_timer(SHOW_SOLUTION, solution_speed)

                    elif (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                        self.maze.move_player("up")

                    elif (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                        self.maze.move_player("down")

                    elif (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                        self.maze.move_player("left")
                    
                    elif (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                        self.maze.move_player("right")
                    
                    if self.maze.player_position == self.maze.endpoint:
                        self.audio.play_sound_effect(effect="victory")
                        end_reached = True
                        done = True
                        if solving:
                            pygame.time.set_timer(SHOW_SOLUTION, 0)
                            solving = False
                            self.show_solution_button.enable()
                        time_delta = math.ceil(time.time()) - time_delta
                        self.redraw_elements(self.managers, time_delta)

                self.ui_manager.process_events(event)

            if not done:
                time_delta = math.ceil(time.time()) - time_delta
                self.redraw_elements(self.managers, time_delta)
            
        if end_reached:
            restart = self.show_modal(self.finished_modal)
            if restart:
                self.reset()
                self.set_maze(self.maze.dimensions)
                next_page = self
            else:
                self.reset()
                next_page = self.game_window.title_screen

        self.log_exit_screen()
        return next_page
