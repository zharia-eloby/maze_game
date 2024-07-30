import pygame, pygame_gui, math, time
from pygame_gui.core import ObjectID
from classes.screens.screen import Screen

class TitleScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window)
        self.audio = audio
        self.managers = [self.get_background()['background_manager'], self.ui_manager]

    def setup(self):
        self.audio.create_audio_buttons(self.ui_manager)
        self.game_window.resize_image('#audio-button', self.audio.get_audio_button_rect().width, self.audio.get_audio_button_rect().height)
        self.game_window.resize_image('#no-audio-button', self.audio.get_audio_button_rect().width, self.audio.get_audio_button_rect().height)

        settings_button_rect = pygame.Rect(
            self.game_window.drawable_area.left,
            self.game_window.drawable_area.top,
            self.game_window.small_sq_button_width,
            self.game_window.small_sq_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=settings_button_rect, 
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#settings-cog-button")
        )
        self.game_window.resize_image('#settings-cog-button', settings_button_rect.width, settings_button_rect.height)
        
        play_rect = pygame.Rect(
            self.game_window.drawable_area.centerx - self.game_window.large_rect_button_width/2,
            self.game_window.drawable_area.centery + self.game_window.large_rect_button_height/2,
            self.game_window.large_rect_button_width,
            self.game_window.large_rect_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=play_rect, 
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#play-button")
        )
        self.game_window.resize_image('#play-button', play_rect.width, play_rect.height)
        
        title_rect = pygame.Rect(
            self.game_window.drawable_area.left, 
            self.game_window.drawable_area.top,
            self.game_window.drawable_area.width, 
            play_rect.top - self.game_window.drawable_area.top
        )
        pygame_gui.elements.UILabel(
            relative_rect=title_rect, 
            text="MAZE",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#title")
        )

        credits_rect = pygame.Rect(
            self.game_window.drawable_area.left,
            self.game_window.drawable_area.bottom - self.game_window.small_text_height, 
            self.game_window.drawable_area.width,
            self.game_window.small_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=credits_rect, 
            text="created by Zharia Eloby",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#created-by-text", class_id="@small-text")
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
                    if event.ui_object_id == "#play-button":
                        done = True
                        next_page = self.game_window.pick_size_screen

                    elif event.ui_object_id == "#settings-cog-button":
                        done = True
                        next_page = self.game_window.settings_screen

                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                self.ui_manager.process_events(event)

            time_delta = math.ceil(time.time()) - time_delta
            self.game_window.redraw_elements(self.managers, time_delta)
        return next_page