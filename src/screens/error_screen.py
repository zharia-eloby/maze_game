import pygame, pygame_gui, os, math, time, webbrowser
from src.screens.screen import Screen
from pygame_gui.core import ObjectID

class ErrorScreen(Screen):
    def __init__(self, game_window):
        super().__init__(game_window, None)
        theme_file = os.path.realpath("src/themes/error/theme.json")
        self.ui_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), theme_file)
        self.background_manager = pygame_gui.UIManager((self.settings.screen_width, self.settings.screen_height), theme_file)
        self.managers = [self.background_manager, self.ui_manager]

        self.error_text_box = None

    def setup(self):
        self.log_setup_start()

        self.background_rect = pygame.Rect(0, 0, self.settings.screen_width, self.settings.screen_height)
        pygame_gui.elements.UIPanel(
            relative_rect=self.background_rect,
            manager=self.background_manager
        )

        button_height = math.floor(self.settings.drawable_area.height/10)
        exit_button_rect = pygame.Rect(
            self.settings.drawable_area.left,
            self.settings.drawable_area.bottom - button_height,
            self.settings.drawable_area.width,
            button_height
        )
        pygame_gui.elements.UIButton(
            relative_rect=exit_button_rect, 
            text="Close Window",
            manager=self.ui_manager,
            object_id=ObjectID("#exit-button", class_id="@small-text")
        )

        report_button_rect = pygame.Rect(
            exit_button_rect.left,
            exit_button_rect.top - button_height - self.settings.line_spacing,
            exit_button_rect.width,
            button_height
        )
        self.report_button = pygame_gui.elements.UIButton(
            relative_rect=report_button_rect, 
            text="Report An Issue",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#report-button", class_id="@small-text")
        )

        error_heading_rect = pygame.Rect(
            self.settings.drawable_area.left,
            self.settings.drawable_area.top,
            self.settings.drawable_area.width,
            (self.settings.drawable_area.height - button_height*2 - self.settings.line_spacing)/2
        )
        self.error_text_box = pygame_gui.elements.UITextBox(
            relative_rect=error_heading_rect, 
            html_text="<p>Uh oh! An error occurred.</p>",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#error-heading", class_id="@large-text")
        )
        error_text_rect = pygame.Rect(
            error_heading_rect.left,
            error_heading_rect.bottom,
            self.settings.drawable_area.width,
            report_button_rect.top-error_heading_rect.bottom
        )
        self.error_text_box = pygame_gui.elements.UITextBox(
            relative_rect=error_text_rect, 
            html_text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#error-text", class_id="@small-text")
        )

        self.log_setup_success()

    def set_error_text(self, error_text):
        if (os.name == "nt"): # for windows devices
            help_text = "<a href=''>See full error log</a>"
        else:
            help_text = "See error log at '{file_path}'".format(file_path=os.path.realpath(self.settings.log_filename))
        html_text = "<p>Error ({error_text})</p><p>{help_text}</p>".format(error_text=error_text, help_text=help_text)
        self.error_text_box.set_text(html_text)

    def show(self):
        self.log_display_screen()

        pygame.mixer.music.stop()
        time_delta = math.ceil(time.time())
        self.redraw_elements(self.managers, 0)

        done = False
        while not done:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    self.log_exit_screen()
                    return

                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                elif event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
                    os.startfile(os.path.realpath(self.settings.log_filename))
                
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "#report-button":
                        webbrowser.open("https://docs.google.com/forms/d/e/1FAIpQLSchHIjMhzE13S0FutPxqLsUEoATb8NTOlnoPVz7oxOZajTKPA/viewform?usp=sf_link")
                    elif event.ui_object_id == "#exit-button":
                        done = True

                self.ui_manager.process_events(event)

            time_delta = math.ceil(time.time()) - time_delta
            self.redraw_elements(self.managers, time_delta)