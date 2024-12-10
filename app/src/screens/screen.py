import pygame, pygame_gui, logging

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

    def log_setup_start(self):
        logging.info("Setting up {class_name}".format(class_name=self.__class__.__name__))

    def log_setup_success(self):
        logging.info("Successfully set up {class_name}".format(class_name=self.__class__.__name__))

    def log_display_screen(self):
        logging.info("Navigated to {screen_name}".format(screen_name=self.__class__.__name__))

    def log_exit_screen(self):
        logging.info("Exiting {class_name}".format(class_name=self.__class__.__name__))

    def log_button_press(self, button_name):
        logging.info("{screen_name}: {button_name} button pressed".format(screen_name=self.__class__.__name__, button_name=button_name))

    def log_general_event(self, message):
        logging.info("{screen_name}: {message}".format(screen_name=self.__class__.__name__, message=message))

    def redraw_elements(self, managers, time_delta):
        for m in managers:
            m.update(time_delta)
            m.draw_ui(pygame.display.get_surface())
        pygame.display.update()
    