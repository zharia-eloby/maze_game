import pygame, pygame_gui, math, time
from pygame_gui.core import ObjectID
from screens.screen import Screen

class TitleScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window, audio)
        self.managers = [self.background_manager, self.ui_manager]

    def setup(self):
        self.set_background()

        settings_button_rect = pygame.Rect(
            self.settings.drawable_area.right - self.settings.small_sq_button_width,
            self.settings.drawable_area.top,
            self.settings.small_sq_button_width,
            self.settings.small_sq_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=settings_button_rect, 
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#settings-cog-button")
        )

        play_rect = pygame.Rect(
            self.settings.drawable_area.centerx - self.settings.large_rect_button_width/2,
            self.settings.drawable_area.centery + self.settings.line_spacing/2,
            self.settings.large_rect_button_width,
            self.settings.large_rect_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=play_rect, 
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#play-button")
        )
        
        title_rect = pygame.Rect(
            self.settings.drawable_area.left, 
            self.settings.drawable_area.top,
            self.settings.drawable_area.width, 
            play_rect.top - self.settings.line_spacing - self.settings.drawable_area.top
        )
        pygame_gui.elements.UILabel(
            relative_rect=title_rect, 
            text="MAZE",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#title")
        )

    def show(self):
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
                    if event.ui_object_id == "#play-button":
                        done = True
                        next_page = self.game_window.pick_size_screen

                    elif event.ui_object_id == "#settings-cog-button":
                        next_action = self.game_window.settings_screen.show()
                        if next_action == "exit_game":
                            done = True

                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                self.ui_manager.process_events(event)

            if not done:
                time_delta = math.ceil(time.time()) - time_delta
                self.redraw_elements(self.managers, time_delta)
        return next_page