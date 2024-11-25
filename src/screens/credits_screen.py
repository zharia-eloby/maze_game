import pygame, pygame_gui, math, time, webbrowser
from pygame_gui.core import ObjectID
from screens.screen import Screen

class CreditsScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window, audio)
        self.managers = [self.background_manager, self.ui_manager]
        self.credits_column_width = self.settings.drawable_area.width*0.75
        self.links_column_width = self.settings.drawable_area.width - self.credits_column_width
        self.credits = {
            "development-credits": {
                "text": "Development",
                "attribution": "Zharia Eloby",
                "link": "https://github.com/zharia-eloby",
            },
            "audio-credits": {
                "text": "Audio",
                "attribution": "'Lost in the Dessert' by jhaeka",
                "link": "https://joshuuu.itch.io/short-loopable-background-music",
            },
            "background-credits": {
                "text": "Background",
                "attribution": "Space Spheremaps",
                "link": "https://space-spheremaps.itch.io/pixelart-starfields",
            }
        }

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

        game_title_text_rect = pygame.Rect(
            self.settings.drawable_area.left, 
            back_button_rect.bottom,
            self.settings.drawable_area.width, 
            self.settings.medium_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=game_title_text_rect, 
            text="A Maze Game",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@medium-text")
        )
        
        credits_text = pygame.Rect(
            self.settings.drawable_area.left, 
            game_title_text_rect.bottom + self.settings.line_spacing,
            self.settings.drawable_area.width,
            self.settings.small_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=credits_text, 
            text="Credits",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@small-text")
        )

        html_text = ""
        for i in self.credits:
            html_text += "<p>{text} - <a href='{link}'>{attribution}</a></p><br>".format(
                text=self.credits[i]['text'], 
                link=self.credits[i]['link'], 
                attribution=self.credits[i]['attribution']
            )

        credits_text_rect = pygame.Rect(
            self.settings.drawable_area.left,
            credits_text.bottom + self.settings.line_spacing,
            self.settings.drawable_area.width,
            self.settings.drawable_area.bottom - credits_text.bottom - self.settings.line_spacing
        )
        pygame_gui.elements.UITextBox(
            relative_rect=credits_text_rect,
            html_text=html_text,
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text", object_id="#credits-text")
        )

    def show(self):
        self.audio.set_audio_display()
        self.redraw_elements(self.managers, 0)

        time_delta = math.ceil(time.time())
        done = False
        next_page = None
        while not done:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    self.audio.play_sound_effect()
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
            self.redraw_elements(self.managers, time_delta)
        return next_page