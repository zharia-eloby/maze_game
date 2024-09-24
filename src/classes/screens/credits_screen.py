import pygame, pygame_gui, math, time, webbrowser
from pygame_gui.core import ObjectID
from classes.screens.screen import Screen

class CreditsScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window)
        self.audio = audio
        self.line_spacing = 5
        self.managers = [self.get_background()['background_manager'], self.ui_manager]
        self.credits_column_width = self.game_window.drawable_area.width*0.75
        self.links_column_width = self.game_window.drawable_area.width - self.credits_column_width
        self.credits = {
            "#audio-credits": {
                "text": "Audio from",
                "attribution": "Somewhere",
                "link": "https://space-spheremaps.itch.io/pixelart-starfields",
                "object_id": "#audio-credits"
            },
            "#background-credits": {
                "text": "Background from",
                "attribution": "Space Spheremaps",
                "link": "https://space-spheremaps.itch.io/pixelart-starfields",
                "object_id": "#background-credits"
            },
            "#icons-credits": {
                "text": "Icons from",
                "attribution": "Kenney.nl",
                "link": "https://kenney.nl/assets/game-icons",
                "object_id": "#icons-credits"
            }
        }

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
            back_button_rect.bottom,
            self.game_window.drawable_area.width, 
            self.game_window.medium_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=game_title_text_rect, 
            text="A Maze Game",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@medium-text")
        )
        
        development_credits_text = pygame.Rect(
            self.game_window.drawable_area.left, 
            game_title_text_rect.bottom + self.line_spacing,
            self.game_window.drawable_area.width,
            self.game_window.small_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=development_credits_text, 
            text="Developed by Zharia Eloby",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@small-text")
        )

        html_text = ""
        for i in self.credits:
            html_text += "<p>{text} <a href='{link}'>{attribution}</a></p><br>".format(text=self.credits[i]['text'], link=self.credits[i]['link'], attribution=self.credits[i]['attribution'])

        credits_text_rect = pygame.Rect(
            self.game_window.drawable_area.left,
            development_credits_text.bottom + self.line_spacing,
            self.game_window.drawable_area.width,
            self.game_window.drawable_area.bottom - development_credits_text.bottom - self.line_spacing
        )
        pygame_gui.elements.UITextBox(
            relative_rect=credits_text_rect,
            html_text=html_text,
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text", object_id="#credits-text")
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
                elif event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
                    webbrowser.open(event.link_target)

                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                self.ui_manager.process_events(event)

            time_delta = math.ceil(time.time()) - time_delta
            self.game_window.redraw_elements(self.managers, time_delta)
        return next_page