import pygame, pygame_gui

class Screen():
    def __init__(self, game_window, audio):
        self.audio = audio
        self.settings = game_window.settings
        self.game_window = game_window
        self.ui_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme.theme_file)
        self.background_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), self.settings.theme.theme_file)
    
    def set_background(self):
        background_rect = pygame.Rect(
            0,
            0,
            self.settings.screen_width,
            self.settings.screen_height
        )
        
        img_file = self.settings.theme.background_image_file
        pygame_gui.elements.UIImage(
            relative_rect=background_rect,
            image_surface=pygame.image.load(img_file).convert(),
            manager=self.background_manager
        )

    def redraw_elements(self, managers, time_delta):
        for m in managers:
            m.update(time_delta)
            m.draw_ui(pygame.display.get_surface())
        pygame.display.update()
    