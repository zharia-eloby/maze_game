import pygame, pygame_gui, math, time, webbrowser
from pygame_gui.core import ObjectID
from src.screens.screen import Screen

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
            "background-credits": {
                "text": "Background",
                "attribution": "Space Spheremaps",
                "link": "https://space-spheremaps.itch.io/pixelart-starfields",
            },
            "ui-buttons-credits": {
                "text": "UI Buttons",
                "attribution": "Prinbles",
                "link": "https://prinbles.itch.io/candy-buttons-pack-i",
            },
            "audio-credits": {
                "text": "Background Music",
                "attribution": "jhaeka",
                "link": "https://joshuuu.itch.io/short-loopable-background-music",
            },
            "button-sound-fx-credits": {
                "text": "Button Sound FX",
                "attribution": "kasse",
                "link": "https://kasse.itch.io/ui-buttons-sound-effects-pack",
            },
            "other-sound-fx-credits": {
                "text": "Other Sound FX",
                "attribution": "Kronbits",
                "link": "https://kronbits.itch.io/freesfx",
            }
        }

    def setup(self):
        self.log_setup_start()

        self.set_background()

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

        self.log_setup_success()

    def show(self):
        self.log_display_screen()
        
        self.redraw_elements(self.managers, 0)

        time_delta = math.ceil(time.time())
        done = False
        while not done:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    self.log_button_press(event.ui_object_id)
                    self.audio.play_sound_effect()

                    if event.ui_object_id == "#back-button":
                        done = True

                elif event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
                    webbrowser.open(event.link_target)

                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                self.ui_manager.process_events(event)

            if not done:
                time_delta = math.ceil(time.time()) - time_delta
                self.redraw_elements(self.managers, time_delta)
        
        self.log_exit_screen()
        