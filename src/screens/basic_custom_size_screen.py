import pygame, pygame_gui, math, time
from pygame_gui.core import ObjectID
from screens.screen import Screen
from general.maze import MazeUI

class BasicCustomSizeScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window, audio)
        self.maze_area_rect = None
        self.row_min = 5
        self.row_max = 35
        self.col_min = 5
        self.col_max = 35
        self.default_rows = int((self.row_max-self.row_min)/2) + self.row_min
        self.default_columns = self.default_rows
        self.preview_text_str = "Preview ({rows} x {columns})"
        self.preview_text = None
        self.managers = [self.background_manager, self.ui_manager]

    def setup(self):
        self.set_background()

        settings_button_rect = pygame.Rect(
            self.settings.drawable_area.right - self.settings.small_sq_button_width,
            self.settings.drawable_area.top,
            self.settings.small_sq_button_width,
            self.settings.small_sq_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=settings_button_rect, 
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#settings-cog-button")
        )
        
        back_button_rect = pygame.Rect(
            self.settings.drawable_area.left,
            self.settings.drawable_area.top,
            self.settings.small_sq_button_width,
            self.settings.small_sq_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=back_button_rect, 
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#back-button")
        )

        slider_width = self.settings.drawable_area.width * 0.75
        dimensions_slider_rect = pygame.Rect(
            self.settings.drawable_area.centerx - slider_width/2,
            back_button_rect.bottom + self.settings.line_spacing,
            slider_width,
            self.settings.slider_height
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
            self.settings.small_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=min_text_label_rect,
            text="Easy",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text-left")
        )

        max_text_label_rect = pygame.Rect(
            dimensions_slider_rect.left,
            dimensions_slider_rect.bottom,
            dimensions_slider_rect.width,
            self.settings.small_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=max_text_label_rect,
            text="Hard",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text-right")
        )

        preview_text_label_rect = pygame.Rect(
            self.settings.drawable_area.left,
            min_text_label_rect.bottom,
            self.settings.drawable_area.width,
            self.settings.small_text_height
        )
        self.preview_text = pygame_gui.elements.UILabel(
            relative_rect=preview_text_label_rect,
            text=self.preview_text_str.format(rows=self.default_rows, columns=self.default_columns),
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text")
        )
        
        play_button_rect = pygame.Rect(
            self.settings.drawable_area.centerx- self.settings.wide_button_width/2,
            self.settings.drawable_area.bottom - self.settings.thin_wide_button_height,
            self.settings.wide_button_width,
            self.settings.thin_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=play_button_rect, 
            text="Start",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#start-button", class_id="@thin-wide-button")
        )

        self.maze_area_rect = pygame.Rect(
            preview_text_label_rect.left,
            preview_text_label_rect.bottom + self.settings.line_spacing,
            self.settings.drawable_area.width,
            play_button_rect.top - preview_text_label_rect.bottom - self.settings.line_spacing*2
        )

    def show(self):
        self.dimensions_slider.set_current_value(0.5)

        maze = MazeUI((self.default_rows, self.default_columns), self.settings)
        maze.create_maze()
        maze.set_ui_element_sizes(self.maze_area_rect)
        maze.draw_maze()
        self.managers.insert(1, maze.maze_manager)

        done = False
        next_page = None
        new_rows = maze.dimensions[0]
        self.redraw_elements(self.managers, 0)
        time_delta = math.ceil(time.time())
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    break
                
                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if maze.dimensions[0] != new_rows:
                        self.preview_text.set_text(self.preview_text_str.format(rows=new_rows, columns=new_rows))
                        maze.reset()
                        maze.update_maze_size((new_rows, new_rows))
                        maze.create_maze()
                        maze.set_ui_element_sizes(self.maze_area_rect)
                        maze.draw_maze()

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if "#sliding_button" not in event.ui_object_id: self.audio.play_sound_effect()
                    if event.ui_object_id == "#back-button":
                        done = True
                        next_page = self.game_window.pick_size_screen
                        break

                    elif event.ui_object_id == "#start-button":
                        done = True
                        self.game_window.play_screen.set_maze(maze.dimensions)
                        next_page = self.game_window.play_screen
                        break

                    elif event.ui_object_id == "#settings-cog-button":
                        next_action = self.game_window.settings_screen.show()
                        if next_action == "exit_game":
                            done = True
                
                elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    new_rows = self.row_min + int((self.row_max - self.row_min) * self.dimensions_slider.get_current_value())
                
                self.ui_manager.process_events(event)

            if not done:
                time_delta = math.ceil(time.time()) - time_delta
                self.redraw_elements(self.managers, time_delta)
        
        del maze
        self.managers = [self.background_manager, self.ui_manager]
        self.preview_text.set_text(self.preview_text_str.format(rows=self.default_rows, columns=self.default_columns))
        return next_page