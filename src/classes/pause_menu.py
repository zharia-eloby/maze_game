import pygame, pygame_gui, math, time, sys
from pygame_gui.core import ObjectID
from classes.modal import Modal
from helpers.redraw import redraw_elements
from helpers.debugging import resize_image

class PauseMenu(Modal):
    def __init__(self, game_window):
        super().__init__(game_window)
        # all interactive elements will have this manager
        self.interactive_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)
        # all non-interactive elements will have this manager
        self.menu_background_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)
        self.overlay_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)


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
            self.drawable_area.centerx - self.width/2, 
            self.drawable_area.centery - self.height/2, 
            self.width, 
            self.height
        )
        pygame_gui.elements.UIPanel(
            relative_rect = background_rect,
            manager=self.menu_background_manager,
            object_id=ObjectID(object_id="#modal-background")
        )

        button_height = 70
        button_width = background_rect.width-self.margin*2
        exit_button_rect = pygame.Rect(
            self.drawable_area.centerx - button_width/2,
            background_rect.bottom - self.margin - button_height,
            button_width,
            button_height
        )
        exit_button = pygame_gui.elements.UIButton(
            relative_rect=exit_button_rect,
            text="exit to home screen",
            manager=self.interactive_manager,
            object_id=ObjectID(object_id="#exit-button", class_id="@modal-large-button")
        )
        resize_image('@modal-large-button', button_width, button_height)

        resume_button_rect = pygame.Rect(
            background_rect.left + self.margin,
            exit_button_rect.top - button_height - self.line_spacing,
            button_width,
            button_height
        )
        resume_button = pygame_gui.elements.UIButton(
            relative_rect=resume_button_rect,
            text="resume",
            manager=self.interactive_manager,
            object_id=ObjectID(object_id="#resume-button", class_id="@modal-large-button")
        )

        paused_text_rect = pygame.Rect(
            background_rect.left + self.margin, 
            background_rect.top + self.margin,
            self.width - self.margin*2, 
            resume_button_rect.top - background_rect.top - self.margin
        )
        pygame_gui.elements.UILabel(
            relative_rect=paused_text_rect,
            text="paused",
            manager=self.menu_background_manager,
            object_id=ObjectID(class_id="@medium-text")
        )

    def show(self):
        paused = True
        resume = True
        time_delta = math.ceil(time.time())
        redraw_elements(self.game_window.window, [self.overlay_manager, self.menu_background_manager, self.interactive_manager], 0)
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

                self.interactive_manager.process_events(event)

            time_delta = math.ceil(time.time()) - time_delta
            redraw_elements(self.game_window.window, [self.menu_background_manager, self.interactive_manager], time_delta)
        return resume