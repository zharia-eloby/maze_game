import pygame, pygame_gui
from pygame_gui.core import ObjectID
from classes.screens.screen import Screen

class LoadingScreen(Screen):
    def __init__(self, game_window):
        super().__init__(game_window)
        self.managers = [self.ui_manager]

    def setup(self):
        loading_text_rect = self.game_window.drawable_area
        pygame_gui.elements.UILabel(
            relative_rect=loading_text_rect, 
            text="Loading...",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@medium-text")
        )

    def show(self):
        POLL = pygame.USEREVENT + 1
        pygame.time.set_timer(POLL, 2000)
        self.game_window.redraw_elements(self.managers, 0)

        clock = pygame.time.Clock()
        done = False
        while not done:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    return
                
                elif event.type == POLL:
                    if self.game_window.finished_loading:
                        done = True
                        pygame.time.set_timer(POLL, 0)
                        return

                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                self.ui_manager.process_events(event)

            clock.tick(1)
            self.game_window.redraw_elements(self.managers, 1)