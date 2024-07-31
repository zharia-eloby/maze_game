import pygame, pygame_gui, math, time, sys
from pygame_gui.core import ObjectID
from classes.modals.modal import Modal

class ShowSolutionModal(Modal):
    def __init__(self, game_window):
        super().__init__(game_window)
        self.menu_background_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)
        
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
            self.game_window.drawable_area.centerx - self.width/2, 
            self.game_window.drawable_area.centery - self.height/2, 
            self.width, 
            self.height
        )
        pygame_gui.elements.UIPanel(
            relative_rect = background_rect,
            manager=self.menu_background_manager,
            object_id=ObjectID(object_id="#modal-background")
        )

        yes_button_rect = pygame.Rect(
            background_rect.centerx - self.modal_wide_button_width/2,
            background_rect.bottom - self.margin - self.modal_wide_button_height,
            self.modal_wide_button_width,
            self.modal_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=yes_button_rect,
            text="yes, i give up",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#yes-button", class_id="@modal-wide-button")
        )

        no_button_rect = pygame.Rect(
            background_rect.centerx - self.modal_wide_button_width/2,
            yes_button_rect.top - self.line_spacing - self.modal_wide_button_height,
            self.modal_wide_button_width,
            self.modal_wide_button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=no_button_rect,
            text="no, i'll keep trying",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#no-button", class_id="@modal-wide-button")
        )

        modal_title_text_1_rect = pygame.Rect(
            background_rect.left + self.margin, 
            background_rect.top + self.margin,
            self.width - self.margin*2,
            (no_button_rect.top - background_rect.top - self.margin - self.line_spacing)/2
        )
        pygame_gui.elements.UILabel(
            relative_rect=modal_title_text_1_rect,
            text="reveal",
            manager=self.menu_background_manager,
            object_id=ObjectID(class_id="@medium-text")
        )
        modal_title_text_2_rect = pygame.Rect(
            background_rect.left + self.margin, 
            modal_title_text_1_rect.bottom,
            self.width - self.margin*2, 
            (no_button_rect.top - background_rect.top - self.margin - self.line_spacing)/2
        )
        pygame_gui.elements.UILabel(
            relative_rect=modal_title_text_2_rect,
            text="solution?",
            manager=self.menu_background_manager,
            object_id=ObjectID(class_id="@medium-text")
        )

    def show(self):
        give_up = None
        time_delta = math.ceil(time.time())
        self.game_window.redraw_elements([self.overlay_manager, self.menu_background_manager, self.ui_manager], 0)
        while give_up is None:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame_gui.UI_BUTTON_PRESSED and len(event.__dict__) > 0:
                    if event.ui_object_id == "#yes-button":
                        give_up = True

                    elif event.ui_object_id == "#no-button":
                        give_up = False

                self.ui_manager.process_events(event)

            time_delta = math.ceil(time.time()) - time_delta
            self.game_window.redraw_elements([self.menu_background_manager, self.ui_manager], time_delta)
        return give_up