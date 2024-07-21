import pygame, pygame_gui, math, sys, time
from pygame_gui.core import ObjectID
from classes.screen import Screen
from helpers.redraw import redraw_elements
from helpers.debugging import resize_image
from classes.maze import Maze
from classes.pause_menu import PauseMenu
from classes.finished_menu import FinishedMenu
from classes.title_screen import TitleScreen

class PlayScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window)
        self.ui_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)
        self.audio = audio
        self.rows = None
        self.columns = None
        self.maze = None
        self.solution_stack = None
        self.player = None
        self.show_solution_button = None
        self.reset_button = None
        self.pause_menu = None
        self.finished_menu = None
        self.solution_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)
        self.managers = [self.solution_manager, self.ui_manager]

    def set_maze_dimensions(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.maze = Maze(self.rows, self.columns)
    
    def reset(self):
        self.ui_manager.clear_and_reset()
        self.solution_manager.clear_and_reset()
        self.solution_stack = None
        self.player = None
        self.show_solution_button = None
        self.reset_button = None

    def setup(self):
        bg = self.get_background()
        self.managers.insert(0, bg['background_manager'])

        self.audio.create_audio_buttons(self, self.ui_manager)

        self.pause_menu = PauseMenu(self.game_window)
        self.pause_menu.setup()

        self.finished_menu = FinishedMenu(self.game_window)
        self.finished_menu.setup()

        self.maze.create_maze()

        endpoint = self.maze.get_endpoint()
        startpoint = self.maze.get_startpoint()
        self.maze.set_player_position(startpoint)

        self.maze.set_maze_dimensions()
        self.maze.draw_maze(self.ui_manager)
        
        ui_position = self.maze.get_cell_ui_position(startpoint)
        start_rect = pygame.Rect(
            ui_position[0],
            ui_position[1],
            self.maze.get_cell_width() - self.maze.get_wall_thickness(),
            self.maze.get_cell_height() - self.maze.get_wall_thickness()
        )
        start = pygame_gui.elements.UIPanel(
            relative_rect=start_rect,
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#startpoint")
        )

        ui_position = self.maze.get_cell_ui_position(endpoint)
        end_rect = pygame.Rect(
            ui_position[0],
            ui_position[1],
            self.maze.get_cell_width() - self.maze.get_wall_thickness(),
            self.maze.get_cell_height() - self.maze.get_wall_thickness()
        )
        end = pygame_gui.elements.UIPanel(
            relative_rect=end_rect,
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#endpoint")
        )

        player_margin = math.ceil(self.maze.get_wall_thickness() * 1.5)
        # set player width to be the smaller of cell width and cell height
        if (start_rect.width > start_rect.height):
            player_width = self.maze.get_cell_height() - player_margin*2
        else:
            player_width = self.maze.get_cell_width() - player_margin*2
        player_height = player_width

        player_rect = pygame.Rect(
            start_rect.centerx - player_width/2,
            start_rect.centery - player_height/2,
            player_width,
            player_height
        )
        self.player = pygame_gui.elements.UIButton(
            relative_rect=player_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#player")
        )
        self.player.disable()
        
        # pause button
        pause_button_width = 45
        pause_button_height = pause_button_width
        pause_button_rect = pygame.Rect(
            self.audio.get_audio_button_rect().left - pause_button_width - 20,
            self.drawable_area.top,
            pause_button_width,
            pause_button_height
        )
        global pause_button
        pause_button = pygame_gui.elements.UIButton(
            relative_rect=pause_button_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#pause-button")
        )

        # reset button
        reset_button_width = 45
        reset_button_height = reset_button_width
        reset_button_rect = pygame.Rect(
            pause_button_rect.left - reset_button_width - 20,
            self.drawable_area.top,
            reset_button_width,
            reset_button_height
        )
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=reset_button_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#reset-button")
        )

        # show solution button
        button_width = math.ceil(self.drawable_area.width * 0.3)
        button_height = 45
        show_solution_rect = pygame.Rect(
            self.drawable_area.left,
            self.drawable_area.top,
            button_width,
            button_height
        )
        self.show_solution_button = pygame_gui.elements.UIButton(
            relative_rect=show_solution_rect,
            text="show solution",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="#show-solution-button")
        )
        resize_image('#show-solution-button', button_width, button_height)

    def show(self):
        # custom event for showing the maze solution
        SHOW_SOLUTION = pygame.USEREVENT + 1

        solution_speed = 10
        increment = 1

        done = False
        solving = False
        redraw_elements(self.game_window.window, self.managers, 0)
        time_delta = math.ceil(time.time())
        while not done:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    pygame.quit()
                    sys.exit()

                # redraw window upon reopening after minimizing
                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                elif event.type == pygame_gui.UI_BUTTON_PRESSED and len(event.__dict__) > 0:
                    if event.ui_object_id == "#pause-button":
                        if solving:
                            pygame.time.set_timer(SHOW_SOLUTION, 0)
                        resume = self.pause_menu.show()
                        if not resume: 
                            self.maze.reset_maze()
                            self.reset()
                            return self.game_window.title_screen
                        if solving:
                            pygame.time.set_timer(SHOW_SOLUTION, solution_speed)
                    elif event.ui_object_id == "#reset-button":
                        self.maze.move_player("reset", self.player)
                    elif event.ui_object_id == "#audio-button" or event.ui_object_id == "#no-audio-button":
                        self.audio.toggle_audio()

                    elif event.ui_element == self.show_solution_button:
                        if not self.solution_stack:
                            self.solution_stack = self.maze.solve_maze()
                        curr_index = 0
                        new_line = True
                        solving = True
                        pygame.time.set_timer(SHOW_SOLUTION, solution_speed)
                        self.solution_manager.clear_and_reset()
                        self.show_solution_button.disable()
                        self.reset_button.disable()

                elif event.type == SHOW_SOLUTION:
                    if new_line:
                        if (curr_index == len(self.solution_stack) - 1):
                            solving = False
                            pygame.time.set_timer(SHOW_SOLUTION, 0)
                            self.show_solution_button.enable()
                            self.reset_button.enable()
                        else:
                            curr_cell = self.solution_stack[curr_index]
                            next_cell = self.solution_stack[curr_index + 1]

                            ui_position = self.maze.get_cell_ui_position(curr_cell)
                            line_rect = pygame.Rect(
                                ui_position[0] + self.maze.get_cell_width()/2 - self.maze.get_wall_thickness(),
                                ui_position[1] + self.maze.get_cell_height()/2 - self.maze.get_wall_thickness(),
                                self.maze.get_wall_thickness(),
                                self.maze.get_wall_thickness()
                            )
                            line = pygame_gui.elements.UIPanel(
                                relative_rect=line_rect,
                                manager=self.solution_manager,
                                object_id=ObjectID(object_id="#solution-path")
                            )

                            if (curr_cell[1] < next_cell[1]) or (curr_cell[1] > next_cell[1]):   # horizontal
                                target_width = self.maze.get_cell_width() + self.maze.get_wall_thickness()
                                target_height = self.maze.get_wall_thickness()

                            elif (curr_cell[0] < next_cell[0]) or (curr_cell[0] > next_cell[0]): # vertical
                                target_width = self.maze.get_wall_thickness()
                                target_height = self.maze.get_cell_height() + self.maze.get_wall_thickness()

                            new_line = False
                            curr_index += 1
                    else:
                        if (curr_cell[1] < next_cell[1]):   # going right
                            line.set_dimensions((line.get_relative_rect().width + increment, line.get_relative_rect().height))

                        elif (curr_cell[1] > next_cell[1]): # going left
                            left = line.get_relative_rect().left
                            line.set_dimensions((line.get_relative_rect().width + increment, line.get_relative_rect().height))
                            line.set_relative_position((left - increment, line.get_relative_rect().top))

                        elif (curr_cell[0] < next_cell[0]): # going down
                            line.set_dimensions((line.get_relative_rect().width, line.get_relative_rect().height + increment))

                        elif (curr_cell[0] > next_cell[0]): # going up
                            top = line.relative_rect.top
                            line.set_dimensions((line.get_relative_rect().width, line.get_relative_rect().height + increment))
                            line.set_relative_position((line.get_relative_rect().left, top - increment))
                        
                        if (line.get_relative_rect().width >= target_width) and (line.get_relative_rect().height >= target_height):
                            line.set_dimensions((target_width, target_height))
                            new_line = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu.show()

                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.maze.move_player("up", self.player)

                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.maze.move_player("down", self.player)

                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.maze.move_player("left", self.player)
                    
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.maze.move_player("right", self.player)
                    
                    if self.maze.get_player_position() == self.maze.get_endpoint():
                        done = True
                        if solving:
                            pygame.time.set_timer(SHOW_SOLUTION, 0)
                            solving = False

                self.ui_manager.process_events(event)

            time_delta = math.ceil(time.time()) - time_delta
            redraw_elements(self.game_window.window, self.managers, time_delta)
            
        restart = self.finished_menu.show()
        if restart:
            self.maze.reset_maze()
            self.reset()
            self.setup()
            self.show()
        else:
            return self.game_window.title_screen