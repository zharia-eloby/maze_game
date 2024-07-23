import pygame, pygame_gui, math, sys, time
from pygame_gui.core import ObjectID
from classes.screen import Screen
from helpers.redraw import redraw_elements
from helpers.debugging import resize_image

class CustomSizeScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window)
        self.audio = audio
        self.managers = [self.ui_manager]
        self.locked_button = None
        self.unlocked_button = None
        self.row_up_arrow_button = None
        self.column_up_arrow_button = None
        self.row_down_arrow_button = None
        self.column_down_arrow_button = None
        self.col_text = None
        self.row_text = None
        self.default_rows = 15
        self.default_columns = 15

    def setup(self):
        bg = self.get_background()
        self.managers.insert(0, bg['background_manager'])

        self.audio.create_audio_buttons(self, self.ui_manager)
        
        button_width = 45
        button_height = 45
        back_button_rect = pygame.Rect(
            self.drawable_area.left,
            self.drawable_area.top,
            button_width,
            button_height
        )
        back_button = pygame_gui.elements.UIButton(
            relative_rect=back_button_rect, 
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#back-button")
        )
        
        select_text_rect = pygame.Rect(
            self.drawable_area.left,
            back_button_rect.bottom,
            self.drawable_area.width,
            70
        )
        pygame_gui.elements.UILabel(
            relative_rect=select_text_rect,
            text="Select your Dimensions",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@medium-text")
        )

        warning_text_rect = pygame.Rect(
            self.drawable_area.left,
            select_text_rect.bottom,
            self.drawable_area.width,
            25
        )
        pygame_gui.elements.UILabel(
            relative_rect=warning_text_rect,
            text="* dimensions must be within 10 units of each other *",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@small-text")
        )
        
        x_width = self.drawable_area.width * 0.1
        x_height = 100
        x_text_rect = pygame.Rect(
            self.drawable_area.centerx - x_width/2,
            self.drawable_area.centery - x_height/2,
            x_width,
            x_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=x_text_rect,
            text="x",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@medium-text")
        )
        
        text_height = 100
        row_text_rect = pygame.Rect(
            self.drawable_area.left,
            self.drawable_area.centery - text_height/2,
            x_text_rect.left - self.drawable_area.left,
            text_height
        )
        self.row_text = pygame_gui.elements.UILabel(
            relative_rect=row_text_rect,
            text=str(self.default_rows),
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@medium-text")
        )

        col_text_rect = pygame.Rect(
            x_text_rect.right,
            self.drawable_area.centery - text_height/2,
            self.drawable_area.right - x_text_rect.right,
            text_height
        )
        self.col_text = pygame_gui.elements.UILabel(
            relative_rect=col_text_rect,
            text=str(self.default_columns),
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@medium-text")
        )

        arrow_width = 50
        arrow_height = 50

        row_up_arrow_rect = pygame.Rect(
            row_text_rect.centerx - arrow_width/2,
            row_text_rect.top - arrow_height,
            arrow_width,
            arrow_height
        )
        self.row_up_arrow_button = pygame_gui.elements.UIButton(
            relative_rect=row_up_arrow_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#row-up-arrow", class_id="@up-arrow")
        )
        resize_image('@up-arrow', arrow_width, arrow_height)

        row_down_arrow_rect = pygame.Rect(
            row_text_rect.centerx - arrow_width/2,
            row_text_rect.bottom,
            arrow_width,
            arrow_height
        )
        self.row_down_arrow_button = pygame_gui.elements.UIButton(
            relative_rect=row_down_arrow_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#row-down-arrow", class_id="@down-arrow")
        )
        resize_image('@down-arrow', arrow_width, arrow_height)

        column_up_arrow_rect = pygame.Rect(
            col_text_rect.centerx - arrow_width/2,
            col_text_rect.top - arrow_height,
            arrow_width,
            arrow_height
        )
        self.column_up_arrow_button = pygame_gui.elements.UIButton(
            relative_rect=column_up_arrow_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#column-up-arrow", class_id="@up-arrow")
        )

        column_down_arrow_rect = pygame.Rect(
            col_text_rect.centerx - arrow_width/2,
            col_text_rect.bottom,
            arrow_width,
            arrow_height
        )
        self.column_down_arrow_button = pygame_gui.elements.UIButton(
            relative_rect=column_down_arrow_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#column-down-arrow", class_id="@down-arrow")
        )

        lock_button_width = 50
        lock_button_height = 50
        lock_button_rect = pygame.Rect(
            self.drawable_area.centerx - lock_button_width/2,
            row_down_arrow_rect.bottom - lock_button_height,
            lock_button_width,
            lock_button_height
        )
        self.locked_button = pygame_gui.elements.UIButton(
            relative_rect=lock_button_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#locked-button")
        )
        self.unlocked_button = pygame_gui.elements.UIButton(
            relative_rect=lock_button_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#unlocked-button")
        )
        resize_image('#locked-button', lock_button_width, lock_button_height)
        resize_image('#unlocked-button', lock_button_width, lock_button_height)
        self.unlocked_button.hide()
        
        button_width = math.floor(self.drawable_area.width/2)
        button_height = 100
        play_button_rect = pygame.Rect(
            self.drawable_area.centerx- button_width/2,
            self.drawable_area.bottom - button_height - 50,
            button_width,
            button_height
        )
        play_button = pygame_gui.elements.UIButton(
            relative_rect=play_button_rect, 
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#play-button")
        )

    def show(self):
        redraw_elements(self.game_window.window, self.managers, 0)

        rows = self.default_rows
        columns = self.default_columns

        row_min = 5
        row_max = 35
        col_min = 5
        col_max = 35

        max_diff = 10

        done = False
        next_page = None
        locked = True # if True, rows and cols change simultaneously
        redraw_elements(self.game_window.window, self.managers, 0)
        time_delta = math.ceil(time.time())
        while not done:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                
                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "#back-button":
                        done = True
                        next_page = self.game_window.pick_size_screen

                    elif (event.ui_object_id == "#audio-button") or (event.ui_object_id == "#no-audio-button"):
                        self.audio.toggle_audio()

                    elif (event.ui_object_id == "#locked-button") or (event.ui_object_id == "#unlocked-button"):
                        if locked:
                            locked = False
                            self.locked_button.hide()
                            self.unlocked_button.show()
                        else:
                            locked = True
                            self.unlocked_button.hide()
                            self.locked_button.show()

                    elif event.ui_object_id == "#play-button":
                        done = True
                        self.game_window.play_screen.set_maze_dimensions(rows, columns)
                        self.game_window.play_screen.setup()
                        next_page = self.game_window.play_screen

                    elif locked:
                        if (event.ui_object_id == "#row-up-arrow") or (event.ui_object_id == "#column-up-arrow"):
                            if (rows < row_max) and (columns < col_max):
                                rows += 1
                                columns += 1
                                if rows == row_max:
                                    self.row_up_arrow_button.disable()

                                if columns == col_max:
                                    self.column_up_arrow_button.disable()

                                if not self.row_down_arrow_button.is_enabled:
                                    self.row_down_arrow_button.enable()

                                if not self.column_down_arrow_button.is_enabled:
                                    self.column_down_arrow_button.enable()

                        if (event.ui_object_id == "#row-down-arrow") or (event.ui_object_id == "#column-down-arrow"):
                            if (rows > row_min) and (columns > col_min):
                                rows -= 1
                                columns -= 1
                                if rows == row_min:
                                    self.row_down_arrow_button.disable()

                                if columns == col_min:
                                    self.column_down_arrow_button.disable()

                                if not self.row_up_arrow_button.is_enabled:
                                    self.row_up_arrow_button.enable()

                                if not self.column_up_arrow_button.is_enabled:
                                    self.column_up_arrow_button.enable()
                    else:
                        if event.ui_object_id == "#row-up-arrow":
                            rows += 1
                            if abs(rows-columns) > max_diff:
                                columns += 1
                                if not (self.column_down_arrow_button.is_enabled):
                                    self.column_down_arrow_button.enable()

                            if rows == row_max:
                                self.row_up_arrow_button.disable()

                            if not self.row_down_arrow_button.is_enabled:
                                self.row_down_arrow_button.enable()

                        elif event.ui_object_id == "#row-down-arrow":
                            rows -= 1
                            if abs(rows-columns) > max_diff:
                                columns -= 1
                                if not (self.column_up_arrow_button.is_enabled):
                                    self.column_up_arrow_button.enable()

                            if rows == row_min:
                                self.row_down_arrow_button.disable()

                            if not self.row_up_arrow_button.is_enabled:
                                self.row_up_arrow_button.enable()

                        elif event.ui_object_id == "#column-up-arrow":
                            columns += 1
                            if abs(rows-columns) > max_diff:
                                rows += 1
                                if not (self.row_down_arrow_button.is_enabled):
                                    self.row_down_arrow_button.enable()

                            if columns == col_max:
                                self.column_up_arrow_button.disable()

                            if not self.column_down_arrow_button.is_enabled:
                                self.column_down_arrow_button.enable()

                        elif event.ui_object_id == "#column-down-arrow":
                            columns -= 1
                            if abs(rows-columns) > max_diff:
                                rows -= 1
                                if not (self.row_up_arrow_button.is_enabled):
                                    self.row_up_arrow_button.enable()
                                    
                            if columns == col_min:
                                self.column_down_arrow_button.disable()

                            if not self.column_up_arrow_button.is_enabled:
                                self.column_up_arrow_button.enable()

                    self.col_text.set_text(str(columns))
                    self.row_text.set_text(str(rows))
                
                if not done: self.ui_manager.process_events(event)

            if not done:
                time_delta = math.ceil(time.time()) - time_delta
                redraw_elements(self.game_window.window, self.managers, time_delta)
                
        return next_page