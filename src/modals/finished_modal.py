import pygame, pygame_gui, math, time, sys
from pygame_gui.core import ObjectID
from modals.modal import Modal

class FinishedModal(Modal):
    def __init__(self, game_window, settings):
        super().__init__(game_window, settings)

    def setup(self):
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
            relative_rect=background_rect,
            manager=self.background_manager,
            object_id=ObjectID(object_id="#modal-background")
        )
        
        exit_button_rect = pygame.Rect(
            background_rect.centerx - self.settings.modal_wide_button_width/2,
            background_rect.bottom - self.settings.modal_margin - self.settings.modal_wide_button_height,
            self.settings.modal_wide_button_width,
            self.settings.modal_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=exit_button_rect,
            text="Back To Home",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#exit-button", class_id="@modal-wide-button")
        )

        play_button_rect = pygame.Rect(
            background_rect.centerx - self.settings.modal_wide_button_width/2,
            exit_button_rect.top - self.settings.line_spacing - self.settings.modal_wide_button_height,
            self.settings.modal_wide_button_width,
            self.settings.modal_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=play_button_rect,
            text="Play Again",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#play-again", class_id="@modal-wide-button")
        )

        finished_message_rect = pygame.Rect(
            background_rect.left + self.settings.modal_margin,
            background_rect.top + self.settings.modal_margin,
            background_rect.width - self.settings.modal_margin*2,
            play_button_rect.top - (background_rect.top+self.settings.modal_margin)
        )
        pygame_gui.elements.UILabel (
            relative_rect=finished_message_rect,
            text="You Did It!",
            manager=self.background_manager,
            object_id=ObjectID(class_id="@medium-text")
        )

    def show(self):
        self.game_window.redraw_elements([self.overlay_manager, self.background_manager, self.ui_manager], 0)
    
        done = False
        restart = False
        time_delta = math.ceil(time.time())
        while not done:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "#exit-button":
                        done = True
                    elif event.ui_object_id == "#play-again":
                        done = True
                        restart = True
                self.ui_manager.process_events(event)
            
            time_delta = math.ceil(time.time()) - time_delta
            self.game_window.redraw_elements([self.background_manager, self.ui_manager], time_delta)
        
        return restart