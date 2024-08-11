import pygame, pygame_gui, math, time
from pygame_gui.core import ObjectID
from classes.screens.screen import Screen

class CreditsScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window)
        self.audio = audio
        self.line_spacing = 15
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

        game_title_text_rect = pygame.Rect(
            self.game_window.drawable_area.left, 
            self.game_window.drawable_area.top,
            self.game_window.drawable_area.width, 
            back_button_rect.bottom + self.line_spacing
        )
        pygame_gui.elements.UILabel(
            relative_rect=game_title_text_rect, 
            text="A Maze Game",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@medium-text")
        )
        
        development_credits_text = pygame.Rect(
            self.game_window.drawable_area.left, 
            self.game_window.drawable_area.top,
            self.game_window.drawable_area.width, 
            game_title_text_rect.bottom + self.line_spacing
        )
        pygame_gui.elements.UILabel(
            relative_rect=development_credits_text, 
            text="Developed by Zharia Eloby",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@small-text")
        )

    def show(self):
        self.audio.set_audio_display()
        self.game_window.redraw_elements(self.managers, 0)

        time_delta = math.ceil(time.time())
        done = False
        next_page = None
        while not done:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "#back-button":
                        done = True
                        next_page = self.game_window.settings_screen
                        break

                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                self.ui_manager.process_events(event)

            time_delta = math.ceil(time.time()) - time_delta
            self.game_window.redraw_elements(self.managers, time_delta)
        return next_page