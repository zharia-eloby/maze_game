import pygame, pygame_gui, math, time
from pygame_gui.core import ObjectID
from screens.screen import Screen
from general.maze import MazeUI, LineSolutionPath
from modals.pause_modal import PauseModal
from modals.finished_modal import FinishedModal
from modals.show_solution_modal import ShowSolutionModal

class PlayScreen(Screen):
    def __init__(self, game_window, settings, audio):
        super().__init__(game_window, settings)
        self.audio = audio
        self.maze = None
        self.show_solution_button = None
        self.reset_button = None
        self.maze_area_rect = None
        self.pause_modal = None
        self.finished_modal = None
        self.show_solution_modal = None
        self.solution_drawer = None
        self.managers = None
        self.line_spacing = 25

    def set_maze(self, rows, columns):
        self.maze = MazeUI(rows, columns, self.settings)
        self.maze.setup_maze_ui(self.maze_area_rect)
        self.solution_drawer = LineSolutionPath(self.maze)
        self.managers = [self.background_manager, self.maze.maze_background_manager, self.solution_drawer.solution_manager, self.maze.maze_manager, self.ui_manager]
    
    def reset(self):
        self.maze.reset()
        self.solution_drawer.reset()
        self.show_solution_button.enable()
        self.managers.clear()

    def setup(self):
        self.set_background()
        self.audio.create_audio_buttons(self.ui_manager, self.settings)

        self.pause_modal = PauseModal(self.game_window, self.settings)
        self.pause_modal.setup()

        self.finished_modal = FinishedModal(self.game_window, self.settings)
        self.finished_modal.setup()

        self.show_solution_modal = ShowSolutionModal(self.game_window, self.settings)
        self.show_solution_modal.setup()
        
        pause_button_rect = pygame.Rect(
            self.audio.get_audio_button_rect().left - self.settings.small_sq_button_width - 20,
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
            pause_button_rect.left - self.settings.small_sq_button_width - 20,
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
            object_id=ObjectID(object_id="#show-solution-button")
        )

        self.maze_area_rect = pygame.Rect(
            self.settings.drawable_area.left,
            show_solution_rect.bottom + self.line_spacing,
            self.settings.drawable_area.width,
            self.settings.drawable_area.height - show_solution_rect.height - self.line_spacing
        )

    def show(self):
        self.audio.set_audio_display()
        SHOW_SOLUTION = pygame.USEREVENT + 1

        solution_speed = 10
        done = False
        next_page = None
        solving = False
        end_reached = False
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
                            self.reset()
                            done = True
                            next_page = self.game_window.title_screen
                            break
                        elif solving:
                            pygame.time.set_timer(SHOW_SOLUTION, solution_speed)

                    elif event.ui_object_id == "#reset-button":
                        self.maze.move_player((0, 0))

                    elif event.ui_object_id == "#show-solution-button":
                        give_up = self.show_solution_modal.show()
                        if give_up:
                            if len(self.maze.solution) == 0:
                                self.maze.solve_maze()
                            solving = True
                            pygame.time.set_timer(SHOW_SOLUTION, solution_speed)
                            self.show_solution_button.disable()

                elif event.type == SHOW_SOLUTION:
                    complete = self.solution_drawer.draw()
                    if complete:
                        solving = False
                        pygame.time.set_timer(SHOW_SOLUTION, 0)
                        self.show_solution_button.enable()
                        break

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if solving: 
                            pygame.time.set_timer(SHOW_SOLUTION, 0)
                        resume = self.pause_modal.show()
                        if not resume:
                            pygame.event.clear()
                            self.reset()
                            done = True
                            next_page = self.game_window.title_screen
                            break
                        elif solving:
                            pygame.time.set_timer(SHOW_SOLUTION, solution_speed)

                    elif (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                        self.maze.move_player((-1, 0))

                    elif (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                        self.maze.move_player((1, 0))

                    elif (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                        self.maze.move_player((0, -1))
                    
                    elif (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                        self.maze.move_player((0, 1))
                    
                    if self.maze.player_position == self.maze.endpoint:
                        end_reached = True
                        done = True
                        if solving:
                            pygame.time.set_timer(SHOW_SOLUTION, 0)
                            solving = False
                            self.show_solution_button.enable()

                self.ui_manager.process_events(event)

            time_delta = math.ceil(time.time()) - time_delta
            self.game_window.redraw_elements(self.managers, time_delta)
            
        if end_reached:
            restart = self.finished_modal.show()
            if restart:
                self.reset()
                self.set_maze(self.maze.rows, self.maze.columns)
                next_page = self
            else:
                self.reset()
                next_page = self.game_window.title_screen
        return next_page
