import pygame, pygame_gui, math, time
from pygame_gui.core import ObjectID
from classes.screens.screen import Screen
from classes.maze import MazeUI

class BasicCustomSizeScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window)
        self.audio = audio
        self.maze_area = None
        self.line_spacing = 15
        self.row_min = 5
        self.row_max = 35
        self.col_min = 5
        self.col_max = 35
        self.default_rows = int((self.row_max-self.row_min)/2) + self.row_min
        self.default_columns = self.default_rows
        self.dimensions = None
        self.maze_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)
        self.managers = [self.get_background()['background_manager'], self.maze_manager, self.ui_manager]

    def setup(self):
        self.audio.create_audio_buttons(self.ui_manager)
        
        back_button_rect = pygame.Rect(
            self.game_window.drawable_area.left,
            self.game_window.drawable_area.top,
            self.game_window.small_sq_button_width,
            self.game_window.small_sq_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=back_button_rect, 
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#back-button")
        )

        slider_width = self.game_window.drawable_area.width * 0.75
        dimensions_slider_rect = pygame.Rect(
            self.game_window.drawable_area.centerx - slider_width/2,
            back_button_rect.bottom + self.line_spacing,
            slider_width,
            self.game_window.slider_height
        )
        self.dimensions_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=dimensions_slider_rect,
            manager=self.ui_manager,
            value_range=(0, 1),
            start_value=0.5,
            object_id=ObjectID(object_id="#size-slider")
        )
        
        min_text_label_rect = pygame.Rect(
            dimensions_slider_rect.left,
            dimensions_slider_rect.bottom,
            dimensions_slider_rect.width,
            self.game_window.small_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=min_text_label_rect,
            text="easy",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text-left")
        )

        max_text_label_rect = pygame.Rect(
            dimensions_slider_rect.left,
            dimensions_slider_rect.bottom,
            dimensions_slider_rect.width,
            self.game_window.small_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=max_text_label_rect,
            text="hard",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text-right")
        )

        preview_text_label_rect = pygame.Rect(
            self.game_window.drawable_area.left,
            min_text_label_rect.bottom,
            self.game_window.drawable_area.width,
            self.game_window.small_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=preview_text_label_rect,
            text="preview",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text")
        )
        
        play_button_rect = pygame.Rect(
            self.game_window.drawable_area.centerx- self.game_window.wide_button_width/2,
            self.game_window.drawable_area.bottom - self.game_window.thin_wide_button_height,
            self.game_window.wide_button_width,
            self.game_window.thin_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=play_button_rect, 
            text="start",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#start-button", class_id="@thin-wide-button")
        )

        self.maze_area = pygame.Rect(
            preview_text_label_rect.left,
            preview_text_label_rect.bottom + self.line_spacing,
            self.game_window.drawable_area.width,
            play_button_rect.top - preview_text_label_rect.bottom - self.line_spacing*2
        )

    def show(self):
        self.audio.set_audio_display()
        self.dimensions_slider.set_current_value(0.5)

        maze = MazeUI(self.default_rows, self.default_columns, self.game_window)
        maze.create_maze()
        maze.set_maze_ui_measurements(self.maze_area)
        maze.draw_maze(self.maze_manager)

        done = False
        next_page = None
        new_rows = maze.rows
        self.game_window.redraw_elements(self.managers, 0)
        time_delta = math.ceil(time.time())
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                
                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if maze.rows != new_rows:
                        maze.reset_maze()
                        self.maze_manager.clear_and_reset()
                        maze.rows = new_rows
                        maze.columns = maze.rows
                        maze.create_maze()
                        maze.set_maze_ui_measurements(self.maze_area)
                        maze.draw_maze(self.maze_manager)

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "#back-button":
                        done = True
                        del maze
                        self.maze_manager.clear_and_reset()
                        next_page = self.game_window.pick_size_screen

                    elif event.ui_object_id == "#start-button":
                        done = True
                        self.game_window.play_screen.set_maze(maze.rows, maze.columns)
                        del maze
                        self.maze_manager.clear_and_reset()
                        next_page = self.game_window.play_screen
                
                elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    new_rows = self.row_min + int((self.row_max - self.row_min) * self.dimensions_slider.get_current_value())
                
                if not done: self.ui_manager.process_events(event)

            if not done:
                time_delta = math.ceil(time.time()) - time_delta
                self.game_window.redraw_elements(self.managers, time_delta)
        
        return next_page