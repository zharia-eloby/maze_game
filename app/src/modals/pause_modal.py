import pygame, pygame_gui, math, time, sys
from pygame_gui.core import ObjectID
from src.modals.modal import Modal

class PauseModal(Modal):
    def setup(self):
        self.log_setup_start()

        overlay_rect = pygame.Rect(
            0,
            0,
            self.settings.screen_width,
            self.settings.screen_height
        )
        pygame_gui.elements.UIPanel(
            relative_rect=overlay_rect,
            manager=self.overlay_manager,
            object_id=ObjectID(object_id="#screen-overlay")
        )

        background_rect = pygame.Rect(
            self.settings.drawable_area.centerx - self.settings.modal_width/2, 
            self.settings.drawable_area.centery - self.settings.modal_height/2, 
            self.settings.modal_width, 
            self.settings.modal_height
        )
        pygame_gui.elements.UIPanel(
            relative_rect = background_rect,
            manager=self.background_manager,
            object_id=ObjectID(object_id="#modal-background")
        )

        resume_button_rect = pygame.Rect(
            background_rect.centerx - self.settings.small_sq_button_width/2,
            background_rect.bottom - self.settings.modal_margin - self.settings.small_sq_button_height,
            self.settings.small_sq_button_width,
            self.settings.small_sq_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=resume_button_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#play-square-button")
        )

        exit_button_rect = pygame.Rect(
            resume_button_rect.left - self.settings.line_spacing - self.settings.small_sq_button_height,
            background_rect.bottom - self.settings.modal_margin - self.settings.small_sq_button_height,
            self.settings.small_sq_button_width,
            self.settings.small_sq_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=exit_button_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#home-button")
        )

        settings_button_rect = pygame.Rect(
            resume_button_rect.right + self.settings.line_spacing,
            background_rect.bottom - self.settings.modal_margin - self.settings.small_sq_button_height,
            self.settings.small_sq_button_width,
            self.settings.small_sq_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=settings_button_rect,
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#settings-cog-button")
        )

        paused_text_rect = pygame.Rect(
            background_rect.left + self.settings.modal_margin, 
            background_rect.top + self.settings.modal_margin,
            self.settings.modal_width - self.settings.modal_margin*2, 
            resume_button_rect.top - background_rect.top - self.settings.modal_margin
        )
        pygame_gui.elements.UILabel(
            relative_rect=paused_text_rect,
            text="Paused",
            manager=self.background_manager,
            object_id=ObjectID(class_id="@medium-text")
        )

        self.log_setup_success()

    def show(self, parent_managers):
        self.log_display_screen()

        next_action = None
        time_delta = math.ceil(time.time())
        self.redraw_elements([self.overlay_manager, self.background_manager, self.ui_manager], 0)
        while next_action == None:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    next_action = "exit_game"

                elif event.type == pygame_gui.UI_BUTTON_PRESSED and len(event.__dict__) > 0:
                    self.log_button_press(event.ui_object_id)
                    self.audio.play_sound_effect()
                    
                    if event.ui_object_id == "#home-button":
                        next_action = "home"

                    elif event.ui_object_id == "#play-square-button":
                        next_action = "resume"

                    elif event.ui_object_id == "#settings-cog-button":
                        settings_next_action = self.game_window.settings_screen.show()
                        if settings_next_action == "exit_game":
                            next_action = "exit_game"
                        else:
                            self.redraw_elements(parent_managers + [self.overlay_manager], time_delta)

                self.ui_manager.process_events(event)

            if next_action == None:
                time_delta = math.ceil(time.time()) - time_delta
                self.redraw_elements([self.background_manager, self.ui_manager], time_delta)

        self.log_exit_screen()

        return next_action
    