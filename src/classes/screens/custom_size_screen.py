import pygame, pygame_gui, math, time
from pygame_gui.core import ObjectID
from classes.screens.screen import Screen

class CustomSizeScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window)
        self.audio = audio
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
        self.managers = [self.get_background()['background_manager'], self.ui_manager]

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
        
        select_text_rect = pygame.Rect(
            self.game_window.drawable_area.left,
            back_button_rect.bottom,
            self.game_window.drawable_area.width,
            self.game_window.medium_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=select_text_rect,
            text="Choose Dimensions",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@medium-text")
        )

        warning_text_rect = pygame.Rect(
            self.game_window.drawable_area.left,
            select_text_rect.bottom,
            self.game_window.drawable_area.width,
            self.game_window.small_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=warning_text_rect,
            text="* must be within 10 units of each other *",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@small-text")
        )
        
        x_width = self.game_window.drawable_area.width * 0.1
        x_height = self.game_window.medium_text_height
        x_text_rect = pygame.Rect(
            self.game_window.drawable_area.centerx - x_width/2,
            self.game_window.drawable_area.centery - x_height/2,
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
            self.game_window.drawable_area.left,
            self.game_window.drawable_area.centery - text_height/2,
            x_text_rect.left - self.game_window.drawable_area.left,
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
            self.game_window.drawable_area.centery - text_height/2,
            self.game_window.drawable_area.right - x_text_rect.right,
            text_height
        )
        self.col_text = pygame_gui.elements.UILabel(
            relative_rect=col_text_rect,
            text=str(self.default_columns),
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@medium-text")
        )

        row_up_arrow_rect = pygame.Rect(
            row_text_rect.centerx - self.game_window.small_sq_button_width/2,
            row_text_rect.top - self.game_window.small_sq_button_height,
            self.game_window.small_sq_button_width,
            self.game_window.small_sq_button_height
        )
        self.row_up_arrow_button = pygame_gui.elements.UIButton(
            relative_rect=row_up_arrow_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#row-up-arrow", class_id="@up-arrow")
        )
        self.game_window.resize_image('@up-arrow', row_up_arrow_rect.width, row_up_arrow_rect.height)

        row_down_arrow_rect = pygame.Rect(
            row_text_rect.centerx - self.game_window.small_sq_button_width/2,
            row_text_rect.bottom,
            self.game_window.small_sq_button_width,
            self.game_window.small_sq_button_height
        )
        self.row_down_arrow_button = pygame_gui.elements.UIButton(
            relative_rect=row_down_arrow_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#row-down-arrow", class_id="@down-arrow")
        )
        self.game_window.resize_image('@down-arrow', row_down_arrow_rect.width, row_down_arrow_rect.height)

        column_up_arrow_rect = pygame.Rect(
            col_text_rect.centerx - self.game_window.small_sq_button_width/2,
            col_text_rect.top - self.game_window.small_sq_button_height,
            self.game_window.small_sq_button_width,
            self.game_window.small_sq_button_height
        )
        self.column_up_arrow_button = pygame_gui.elements.UIButton(
            relative_rect=column_up_arrow_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#column-up-arrow", class_id="@up-arrow")
        )

        column_down_arrow_rect = pygame.Rect(
            col_text_rect.centerx - self.game_window.small_sq_button_width/2,
            col_text_rect.bottom,
            self.game_window.small_sq_button_width,
            self.game_window.small_sq_button_height
        )
        self.column_down_arrow_button = pygame_gui.elements.UIButton(
            relative_rect=column_down_arrow_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#column-down-arrow", class_id="@down-arrow")
        )

        lock_button_rect = pygame.Rect(
            self.game_window.drawable_area.centerx - self.game_window.small_sq_button_width/2,
            row_down_arrow_rect.bottom - self.game_window.small_sq_button_height,
            self.game_window.small_sq_button_width,
            self.game_window.small_sq_button_height
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
        self.game_window.resize_image('#locked-button', lock_button_rect.width, lock_button_rect.height)
        self.game_window.resize_image('#unlocked-button', lock_button_rect.width, lock_button_rect.height)
        self.unlocked_button.hide()
        
        play_button_rect = pygame.Rect(
            self.game_window.drawable_area.centerx- self.game_window.large_rect_button_width/2,
            self.game_window.drawable_area.bottom - self.game_window.large_rect_button_height - 50,
            self.game_window.large_rect_button_width,
            self.game_window.large_rect_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=play_button_rect, 
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#play-button")
        )

    def show(self):
        self.audio.set_audio_display()

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
        self.game_window.redraw_elements(self.managers, 0)
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
                        self.game_window.play_screen.set_maze(rows, columns)
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
                self.game_window.redraw_elements(self.managers, time_delta)
        
        self.col_text.set_text(str(self.default_columns))
        self.row_text.set_text(str(self.default_rows))
        return next_page