import pygame, pygame_gui, math, time, webbrowser
from pygame_gui.core import ObjectID
from src.screens.screen import Screen

class SettingsScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window, audio)
        self.volume_slider = None
        self.managers = [self.background_manager, self.ui_manager]

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

        content_area_rect = pygame.Rect(
            self.settings.drawable_area.left,
            back_button_rect.bottom,
            self.settings.drawable_area.width,
            self.settings.drawable_area.bottom - back_button_rect.bottom
        )

        settings_title_rect = pygame.Rect(
            content_area_rect.left, 
            content_area_rect.bottom - self.settings.small_text_height,
            content_area_rect.width, 
            self.settings.small_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=settings_title_rect, 
            text=self.settings.version_info,
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text")
        )

        settings_title_rect = pygame.Rect(
            content_area_rect.left, 
            content_area_rect.top,
            content_area_rect.width, 
            self.settings.medium_text_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=settings_title_rect, 
            text="Game Settings",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@medium-text")
        )

        volume_label_rect = pygame.Rect(
            content_area_rect.left, 
            settings_title_rect.bottom + self.settings.line_spacing,
            content_area_rect.width * 0.5, 
            self.settings.slider_height
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
            self.settings.slider_height
        )
        self.volume_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=volume_slider_rect,
            manager=self.ui_manager,
            value_range=(0.0, 1.0),
            start_value=self.audio.background_volume,
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

        sound_fx_label_rect = pygame.Rect(
            content_area_rect.left, 
            volume_label_rect.bottom + self.settings.line_spacing,
            volume_label_rect.width, 
            self.settings.slider_height
        )
        pygame_gui.elements.UILabel(
            relative_rect=sound_fx_label_rect, 
            text="Sound FX",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text")
        )
        sound_fx_slider_rect = pygame.Rect(
            sound_fx_label_rect.right + slider_label_width,
            sound_fx_label_rect.top,
            content_area_rect.width - sound_fx_label_rect.width - slider_label_width*2,
            self.settings.slider_height
        )
        self.sound_fx_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=sound_fx_slider_rect,
            manager=self.ui_manager,
            value_range=(0.0, 1.0),
            start_value=self.audio.background_volume,
            object_id=ObjectID(object_id="#sound-fx-slider")
        )
        slider_minus_label_rect = pygame.Rect(
            sound_fx_label_rect.right, 
            sound_fx_label_rect.top,
            slider_label_width, 
            sound_fx_slider_rect.height
        )
        pygame_gui.elements.UILabel(
            relative_rect=slider_minus_label_rect, 
            text="-",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text")
        )
        slider_add_label_rect = pygame.Rect(
            sound_fx_slider_rect.right, 
            sound_fx_slider_rect.top,
            slider_label_width, 
            sound_fx_slider_rect.height
        )
        pygame_gui.elements.UILabel(
            relative_rect=slider_add_label_rect, 
            text="+",
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@small-text")
        )
        
        credits_button_rect = pygame.Rect(
            content_area_rect.centerx - self.settings.wide_button_width/2,
            sound_fx_slider_rect.bottom + self.settings.line_spacing,
            self.settings.wide_button_width,
            self.settings.thin_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=credits_button_rect,
            text="Credits",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#credits-button", class_id="@thin-wide-button")
        )

        report_button_rect = pygame.Rect(
            content_area_rect.centerx - self.settings.wide_button_width/2,
            credits_button_rect.bottom + self.settings.line_spacing,
            self.settings.wide_button_width,
            self.settings.thin_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=report_button_rect,
            text="Give Feedback",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#feedback-button", class_id="@thin-wide-button")
        )

        exit_game_button_rect = pygame.Rect(
            content_area_rect.centerx - self.settings.wide_button_width/2,
            report_button_rect.bottom + self.settings.line_spacing,
            self.settings.wide_button_width,
            self.settings.thin_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=exit_game_button_rect,
            text="Exit Game",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#exit-button", class_id="#ui-button")
        )

        self.log_setup_success()

    def set_slider_values(self):
        if self.audio.background_audio_channel.get_busy():
            self.volume_slider.set_current_value(self.audio.background_audio_channel.get_volume())
        else:
            self.volume_slider.set_current_value(0)

        self.sound_fx_slider.set_current_value(self.audio.sound_fx_channel.get_volume())

    def show(self):
        self.log_display_screen()

        self.set_slider_values()
        self.redraw_elements(self.managers, 0)

        time_delta = math.ceil(time.time())
        done = False
        action = "back"
        while not done:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    action = "exit_game"

                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()
                    
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if "#sliding_button" not in event.ui_object_id: 
                        self.log_button_press(event.ui_object_id)
                        self.audio.play_sound_effect()

                    if event.ui_object_id == "#back-button":
                        done = True

                    elif event.ui_object_id == "#credits-button":
                        self.game_window.credits_screen.show()
                    
                    elif event.ui_object_id == "#exit-button":
                        done = True
                        action = "exit_game"

                    elif event.ui_object_id == "#feedback-button":
                        webbrowser.open(self.settings.feedback_link)

                elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_object_id == "#volume-slider":
                        self.audio.set_background_volume(self.volume_slider.get_current_value())

                    elif event.ui_object_id == "#sound-fx-slider":
                        self.audio.set_sound_fx_volume(self.sound_fx_slider.get_current_value())

                self.ui_manager.process_events(event)

            if not done:
                time_delta = math.ceil(time.time()) - time_delta
                self.redraw_elements(self.managers, time_delta)
        
        self.log_exit_screen()
        
        return action
    