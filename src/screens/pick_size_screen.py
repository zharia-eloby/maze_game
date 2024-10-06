import pygame, pygame_gui, math, time
from pygame_gui.core import ObjectID
from screens.screen import Screen

class PickSizeScreen(Screen):
    def __init__(self, game_window, settings, audio):
        super().__init__(game_window, settings)
        self.audio = audio
        self.managers = [self.background_manager, self.ui_manager]

    def setup(self):
        self.set_background()
        self.audio.create_audio_buttons(self.ui_manager, self.settings)

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
        
        num_buttons = 4
        line_spacing = 15
        button_area_rect = pygame.Rect(
            self.settings.drawable_area.centerx - self.settings.wide_button_width/2,
            back_button_rect.bottom + line_spacing,
            self.settings.wide_button_width,
            self.settings.drawable_area.bottom - back_button_rect.bottom - line_spacing*2
        )
        space_between_buttons = round((button_area_rect.height - (self.settings.thick_wide_button_height*num_buttons)) / (num_buttons-1))
        
        easy_button_rect = pygame.Rect(
            button_area_rect.left,
            button_area_rect.top,
            self.settings.wide_button_width,
            self.settings.thick_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=easy_button_rect, 
            text="Easy",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#easy-button", class_id="@thick-wide-button")
        )
        
        medium_button_rect = pygame.Rect(
            button_area_rect.left,
            easy_button_rect.bottom + space_between_buttons,
            self.settings.wide_button_width,
            self.settings.thick_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=medium_button_rect, 
            text="Medium",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#medium-button", class_id="@thick-wide-button")
        )
        
        hard_button_rect = pygame.Rect(
            button_area_rect.left,
            medium_button_rect.bottom + space_between_buttons,
            self.settings.wide_button_width,
            self.settings.thick_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=hard_button_rect, 
            text="Hard",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#hard-button", class_id="@thick-wide-button")
        )

        custom_button_rect = pygame.Rect(
            button_area_rect.left,
            hard_button_rect.bottom + space_between_buttons,
            self.settings.wide_button_width,
            self.settings.thick_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=custom_button_rect, 
            text="Custom",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#custom-button", class_id="@thick-wide-button")
        )

    def show(self):
        self.audio.set_audio_display()
        self.redraw_elements(self.managers, 0)

        next_page = None
        done = False
        time_delta = math.ceil(time.time())
        while not done:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                
                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "#easy-button":
                        done = True
                        rows = 10
                        columns = 10
                        self.game_window.play_screen.set_maze(rows, columns)
                        next_page = self.game_window.play_screen

                    elif event.ui_object_id == "#medium-button":
                        done = True
                        rows = 20
                        columns = 20
                        self.game_window.play_screen.set_maze(rows, columns)
                        next_page = self.game_window.play_screen

                    elif event.ui_object_id == "#hard-button":
                        done = True
                        rows = 30
                        columns = 30
                        self.game_window.play_screen.set_maze(rows, columns)
                        next_page = self.game_window.play_screen

                    elif event.ui_object_id == "#custom-button":
                        done = True
                        next_page = self.game_window.basic_custom_size_screen

                    elif event.ui_object_id == "#back-button":
                        done = True
                        next_page = self.game_window.title_screen

                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                self.ui_manager.process_events(event)
            
            time_delta = math.ceil(time.time()) - time_delta
            self.redraw_elements(self.managers, time_delta)

        return next_page
