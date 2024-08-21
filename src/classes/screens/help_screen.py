import pygame, pygame_gui, math, time, webbrowser
from pygame_gui.core import ObjectID
from classes.screens.screen import Screen

class HelpScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window)
        self.audio = audio
        self.volume_slider = None
        self.section_spacing = 25
        self.line_spacing = 0
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

        how_to_section_title_rect = pygame.Rect(
            self.game_window.drawable_area.left,
            back_button_rect.bottom + self.section_spacing,
            self.game_window.drawable_area.width,
            self.game_window.medium_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=how_to_section_title_rect,
            text="how to play",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@medium-text")
        )

        how_to_section_description_rect_1 = pygame.Rect(
            self.game_window.drawable_area.left,
            how_to_section_title_rect.bottom + self.line_spacing,
            self.game_window.drawable_area.width,
            self.game_window.medium_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=how_to_section_description_rect_1,
            text="use your arrow keys or WASD keys to move the player",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text")
        )
        how_to_section_description_rect_2 = pygame.Rect(
            self.game_window.drawable_area.left,
            how_to_section_description_rect_1.bottom + self.line_spacing,
            self.game_window.drawable_area.width,
            self.game_window.medium_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=how_to_section_description_rect_2,
            text="through the maze and reach the end!",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text")
        )

        report_button_rect = pygame.Rect(
            self.game_window.drawable_area.left,
            how_to_section_description_rect_2.bottom + self.section_spacing,
            self.game_window.drawable_area.width,
            self.game_window.thin_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=report_button_rect,
            text="report an issue",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@thin-wide-button", object_id="#report-button")
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

                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()
                    
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "#back-button":
                        done = True
                        next_page = self.game_window.settings_screen
                        break
                    elif event.ui_object_id == "#report-button":
                        webbrowser.open("https://github.com/zharia-eloby/maze_game/issues/new")
                        break

                self.ui_manager.process_events(event)

            time_delta = math.ceil(time.time()) - time_delta
            self.game_window.redraw_elements(self.managers, time_delta)
        return next_page