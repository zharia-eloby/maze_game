import pygame, pygame_gui, math, time
from pygame_gui.core import ObjectID
from classes.screens.screen import Screen

class SettingsScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window)
        self.audio = audio
        self.volume_slider = None
        self.line_spacing = 25
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
            self.game_window.medium_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=settings_title_rect, 
            text="Game Settings",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@medium-text")
        )

        volume_label_rect = pygame.Rect(
            content_area_rect.left, 
            settings_title_rect.bottom + self.line_spacing,
            content_area_rect.width * 0.5, 
            self.game_window.slider_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=volume_label_rect, 
            text="Volume",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text")
        )

        slider_label_width = 25
        volume_slider_rect = pygame.Rect(
            volume_label_rect.right + slider_label_width,
            volume_label_rect.top,
            content_area_rect.width - volume_label_rect.width - slider_label_width*2,
            self.game_window.slider_height
        )
        self.volume_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=volume_slider_rect,
            manager=self.ui_manager,
            value_range=(0.0, 1.0),
            start_value=self.audio.volume,
            object_id=ObjectID(object_id="#volume-slider")
        )
        slider_minus_label_rect = pygame.Rect(
            volume_label_rect.right, 
            volume_label_rect.top,
            slider_label_width, 
            volume_slider_rect.height
        )
        pygame_gui.elements.UILabel(
            relative_rect=slider_minus_label_rect, 
            text="-",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text")
        )
        slider_add_label_rect = pygame.Rect(
            volume_slider_rect.right, 
            volume_slider_rect.top,
            slider_label_width, 
            volume_slider_rect.height
        )
        pygame_gui.elements.UILabel(
            relative_rect=slider_add_label_rect, 
            text="+",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text")
        )

        help_button_rect = pygame.Rect(
            content_area_rect.centerx - self.game_window.wide_button_width/2,
            volume_slider_rect.bottom + self.line_spacing,
            self.game_window.wide_button_width,
            self.game_window.thin_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=help_button_rect,
            text="Help",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#help-button", class_id="@thin-wide-button")
        )

        credits_button_rect = pygame.Rect(
            content_area_rect.centerx - self.game_window.wide_button_width/2,
            help_button_rect.bottom + self.line_spacing,
            self.game_window.wide_button_width,
            self.game_window.thin_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=credits_button_rect,
            text="Credits",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#credits-button", class_id="@thin-wide-button")
        )

        exit_game_button_rect = pygame.Rect(
            content_area_rect.centerx - self.game_window.wide_button_width/2,
            credits_button_rect.bottom + self.line_spacing,
            self.game_window.wide_button_width,
            self.game_window.thin_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=exit_game_button_rect,
            text="Exit Game",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#exit-button", class_id="@thin-wide-button")
        )

    def show(self):
        if pygame.mixer.music.get_busy():
            self.volume_slider.set_current_value(pygame.mixer.music.get_volume())
        else:
            self.volume_slider.set_current_value(0)
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
                        break

                    elif event.ui_object_id == "#help-button":
                        done = True
                        next_page = self.game_window.help_screen
                        break

                    elif event.ui_object_id == "#credits-button":
                        done = True
                        next_page = self.game_window.credits_screen
                        break
                    
                    elif event.ui_object_id == "#exit-button":
                        done = True
                        break

                elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_object_id == "#volume-slider":
                        self.audio.set_volume(self.volume_slider.get_current_value())

                self.ui_manager.process_events(event)

            time_delta = math.ceil(time.time()) - time_delta
            self.game_window.redraw_elements(self.managers, time_delta)
        return next_page