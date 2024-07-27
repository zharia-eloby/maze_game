import pygame, pygame_gui, math, time
from pygame_gui.core import ObjectID
from classes.screens.screen import Screen

class SettingsScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window)
        self.audio = audio
        self.volume_slider = None
        self.managers = [self.get_background()['background_manager'], self.ui_manager]

    def setup(self):
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

        content_area_rect = pygame.Rect(
            self.game_window.drawable_area.left,
            back_button_rect.bottom,
            self.game_window.drawable_area.width,
            self.game_window.drawable_area.bottom - back_button_rect.bottom
        )

        settings_title_rect = pygame.Rect(
            content_area_rect.left, 
            content_area_rect.top,
            content_area_rect.width, 
            50
        )
        pygame_gui.elements.UILabel(
            relative_rect=settings_title_rect, 
            text="Game Settings",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@medium-text")
        )

        volume_label_rect = pygame.Rect(
            content_area_rect.left, 
            settings_title_rect.bottom,
            content_area_rect.width * 0.3, 
            25
        )
        pygame_gui.elements.UILabel(
            relative_rect=volume_label_rect, 
            text="volume",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text")
        )

        volume_slider_rect = pygame.Rect(
            volume_label_rect.right,
            volume_label_rect.top,
            content_area_rect.width - volume_label_rect.width,
            volume_label_rect.height
        )
        self.volume_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=volume_slider_rect,
            manager=self.ui_manager,
            value_range=(0.0, 1.0),
            start_value=self.audio.volume,
            object_id=ObjectID(object_id="#volume-slider")
        )

        exit_game_button_rect = pygame.Rect(
            content_area_rect.centerx - self.game_window.large_rect_button_width/2,
            content_area_rect.centery - self.game_window.large_rect_button_height/2,
            self.game_window.large_rect_button_width,
            self.game_window.large_rect_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=exit_game_button_rect,
            text="exit game",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#exit-button", class_id="@large-button")
        )

    def show(self):
        self.volume_slider.set_current_value(pygame.mixer.music.get_volume())
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
                        next_page = self.game_window.title_screen

                    elif event.ui_object_id == "#exit-button":
                        done = True

                elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_object_id == "#volume-slider":
                        pygame.mixer.music.set_volume(self.volume_slider.get_current_value())
                        if not pygame.mixer.music.get_busy() and pygame.mixer.music.get_volume() > 0:
                            pygame.mixer.music.load(self.audio.audio_file)
                            pygame.mixer.music.play(loops=-1)
                        elif pygame.mixer.music.get_busy() and pygame.mixer.music.get_volume() == 0:
                            pygame.mixer.music.stop()
                            pygame.mixer.music.set_volume(0)
                            pygame.mixer.music.unload()

                self.ui_manager.process_events(event)

            time_delta = math.ceil(time.time()) - time_delta
            self.game_window.redraw_elements(self.managers, time_delta)
        return next_page