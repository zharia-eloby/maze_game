import pygame, pygame_gui, math, time
from pygame_gui.core import ObjectID
from src.screens.screen import Screen
from src.general.helpers import get_file_path

class LoadingScreen(Screen):
    def __init__(self, game_window):
        self.settings = game_window.settings
        self.game_window = game_window
        theme_file = get_file_path("app/src/assets/loading/theme.json")
        self.ui_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), theme_file)
        self.managers = [self.ui_manager]

    def setup(self):
        self.log_setup_start()

        self.background_rect = pygame.Rect(0, 0, self.settings.screen_width, self.settings.screen_height)
        pygame_gui.elements.UIPanel(
            relative_rect=self.background_rect,
            manager=self.ui_manager
        )

        loading_text_rect = self.settings.drawable_area
        pygame_gui.elements.UILabel(
            relative_rect=loading_text_rect, 
            text="Loading",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@medium-text")
        )

        loading_progress_bar_rect = pygame.Rect(
            self.background_rect.centerx - round((self.background_rect.width/3)/2),
            self.background_rect.centery + round(self.settings.medium_text_height/2),
            round(self.background_rect.width/3),
            20
        )
        self.loading_progress_bar = pygame_gui.elements.UIStatusBar(
            relative_rect=loading_progress_bar_rect,
            manager=self.ui_manager
        )

        self.log_setup_success()

    def show(self):
        self.log_display_screen()

        POLL = pygame.USEREVENT + 1
        ANIMATE = pygame.USEREVENT + 2
        
        time_delta = math.ceil(time.time())

        pygame.time.set_timer(POLL, 1000)
        pygame.time.set_timer(ANIMATE, 30)
        self.redraw_elements(self.managers, 0)

        done = False
        while not done:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                
                elif event.type == POLL:
                    if (self.game_window.finished_loading and self.loading_progress_bar.percent_full == 1) or (self.game_window.error):
                        done = True
                        pygame.time.set_timer(POLL, 0)
                        pygame.time.set_timer(ANIMATE, 0)
                        
                elif event.type == ANIMATE:
                    updated_percent = self.loading_progress_bar.percent_full + 0.05
                    if updated_percent > self.game_window.loaded_percent:
                        updated_percent = self.game_window.loaded_percent
                    self.loading_progress_bar.percent_full = updated_percent

                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                self.ui_manager.process_events(event)

            if not done:
                time_delta = math.ceil(time.time()) - time_delta
                self.redraw_elements(self.managers, time_delta)

        self.log_exit_screen()
        