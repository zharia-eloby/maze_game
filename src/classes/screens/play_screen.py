import pygame, pygame_gui, math, time
from pygame_gui.core import ObjectID
from classes.screens.screen import Screen
from classes.maze import MazeUI, LineSolutionPath
from classes.modals.pause_modal import PauseModal
from classes.modals.finished_modal import FinishedModal
from classes.modals.show_solution_modal import ShowSolutionModal

class PlayScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window)
        self.audio = audio
        self.maze = None
        self.show_solution_button = None
        self.reset_button = None
        self.pause_modal = None
        self.finished_modal = None
        self.show_solution_modal = None
        self.managers = [self.get_background()['background_manager'], self.ui_manager]

    def set_maze(self, rows, columns):
        self.maze = MazeUI(rows, columns, self.game_window)
        self.maze.setup_maze_ui()
        self.managers.insert(1, self.maze.maze_manager)
        self.managers.insert(1, self.maze.solution_manager)
    
    def reset(self):
        self.maze.reset_maze()
        self.show_solution_button.enable()

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
                            if len(self.maze.solution) == 0:
                                self.maze.solve_maze()
                            solving = True
                            solution_drawer = LineSolutionPath(self.maze)
                            pygame.time.set_timer(SHOW_SOLUTION, solution_speed)
                            self.maze.solution_manager.clear_and_reset()
                            self.show_solution_button.disable()

                elif event.type == SHOW_SOLUTION:
                    complete = solution_drawer.draw()
                    if complete:
                        solving = False
                        pygame.time.set_timer(SHOW_SOLUTION, 0)
                        self.show_solution_button.enable()

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
