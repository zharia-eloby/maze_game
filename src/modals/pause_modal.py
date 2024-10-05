import pygame, pygame_gui, math, time, sys
from pygame_gui.core import ObjectID
from modals.modal import Modal

class PauseModal(Modal):
    def __init__(self, game_window):
        super().__init__(game_window)
        
    def setup(self):
        overlay_rect = pygame.Rect(
            0,
            0,
            self.game_window.screen_width,
            self.game_window.screen_height
        )
        pygame_gui.elements.UIPanel(
            relative_rect=overlay_rect,
            manager=self.overlay_manager,
            object_id=ObjectID(object_id="#screen-overlay")
        )

        background_rect = pygame.Rect(
            self.game_window.drawable_area.centerx - self.game_window.modal_width/2, 
            self.game_window.drawable_area.centery - self.game_window.modal_height/2, 
            self.game_window.modal_width, 
            self.game_window.modal_height
        )
        pygame_gui.elements.UIPanel(
            relative_rect = background_rect,
            manager=self.background_manager,
            object_id=ObjectID(object_id="#modal-background")
        )

        exit_button_rect = pygame.Rect(
            background_rect.centerx - self.game_window.modal_wide_button_width/2,
            background_rect.bottom - self.game_window.modal_margin - self.game_window.modal_wide_button_height,
            self.game_window.modal_wide_button_width,
            self.game_window.modal_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=exit_button_rect,
            text="Back To Home",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#exit-button", class_id="@modal-wide-button")
        )
        
        resume_button_rect = pygame.Rect(
            background_rect.centerx - self.game_window.modal_wide_button_width/2,
            exit_button_rect.top - self.game_window.line_spacing - self.game_window.modal_wide_button_height,
            self.game_window.modal_wide_button_width,
            self.game_window.modal_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=resume_button_rect,
            text="Resume",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#resume-button", class_id="@modal-wide-button")
        )

        paused_text_rect = pygame.Rect(
            background_rect.left + self.game_window.modal_margin, 
            background_rect.top + self.game_window.modal_margin,
            self.game_window.modal_width - self.game_window.modal_margin*2, 
            resume_button_rect.top - background_rect.top - self.game_window.modal_margin
        )
        pygame_gui.elements.UILabel(
            relative_rect=paused_text_rect,
            text="Paused",
            manager=self.background_manager,
            object_id=ObjectID(class_id="@medium-text")
        )

    def show(self):
        paused = True
        resume = True
        time_delta = math.ceil(time.time())
        self.game_window.redraw_elements([self.overlay_manager, self.background_manager, self.ui_manager], 0)
        while paused:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame_gui.UI_BUTTON_PRESSED and len(event.__dict__) > 0:
                    if event.ui_object_id == "#exit-button":
                        paused = False
                        resume = False

                    elif event.ui_object_id == "#resume-button":
                        paused = False

                self.ui_manager.process_events(event)

            time_delta = math.ceil(time.time()) - time_delta
            self.game_window.redraw_elements([self.background_manager, self.ui_manager], time_delta)
        return resume