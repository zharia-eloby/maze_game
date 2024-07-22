import pygame, pygame_gui, math, sys, time
from pygame_gui.core import ObjectID
from classes.screen import Screen
from helpers.redraw import redraw_elements
from helpers.debugging import resize_image

class TitleScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window)
        self.audio = audio
        self.managers = [self.ui_manager]

    def setup(self):
        bg = self.get_background()
        self.managers.insert(0, bg['background_manager'])

        self.audio.create_audio_buttons(self, self.ui_manager)
        resize_image('#audio-button', self.audio.button_width, self.audio.button_height)
        resize_image('#no-audio-button', self.audio.button_width, self.audio.button_height)

        button_width = math.floor(self.drawable_area.width/2)
        button_height = 100
        play_rect = pygame.Rect(
            self.drawable_area.centerx - button_width/2,
            self.drawable_area.centery + button_height/2,
            button_width,
            button_height
        )
        play_button = pygame_gui.elements.UIButton(
            relative_rect=play_rect, 
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#play-button")
        )
        resize_image('#play-button', button_width, button_height)
        
        title_rect = pygame.Rect(
            self.drawable_area.left, 
            self.drawable_area.top,
            self.drawable_area.width, 
            play_rect.top - self.drawable_area.top
        )
        pygame_gui.elements.UILabel(
            relative_rect=title_rect, 
            text="MAZE",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#title")
        )

        credits_rect = pygame.Rect(
            self.drawable_area.left,
            play_rect.bottom, 
            self.drawable_area.width, 
            self.drawable_area.bottom - play_rect.bottom
        )
        pygame_gui.elements.UILabel(
            relative_rect=credits_rect, 
            text="created by Zharia Eloby",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#created-by-text", class_id="@small-text")
        )

    def show(self):
        redraw_elements(self.game_window.window, self.managers, 0)

        time_delta = math.ceil(time.time())
        while True:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame_gui.UI_BUTTON_PRESSED :
                    if event.ui_object_id == "#play-button":
                        return self.game_window.pick_size_screen
                    elif (event.ui_object_id == "#audio-button") or (event.ui_object_id == "#no-audio-button"):
                        self.audio.toggle_audio()

                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                self.ui_manager.process_events(event)

            time_delta = math.ceil(time.time()) - time_delta
            redraw_elements(self.game_window.window, self.managers, time_delta)
