import pygame, pygame_gui, math, sys, time
from pygame_gui.core import ObjectID
from classes.screen import Screen
from helpers.redraw import redraw_elements
from helpers.debugging import resize_image

class PickSizeScreen(Screen):
    def __init__(self, game_window, audio):
        super().__init__(game_window)
        self.ui_manager = pygame_gui.UIManager((self.game_window.screen_width, self.game_window.screen_height), self.game_window.theme_file)
        self.audio = audio
        self.managers = [self.ui_manager]

    def setup(self):
        bg = self.get_background()
        self.managers.insert(0, bg['background_manager'])

        self.audio.create_audio_buttons(self, self.ui_manager)

        # back button
        button_width = 45
        button_height = 45
        back_button_rect = pygame.Rect(
            self.drawable_area.left,
            self.drawable_area.top,
            button_width,
            button_height
        )
        back_button = pygame_gui.elements.UIButton(
            relative_rect=back_button_rect, 
            text="",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#back-button")
        )
        resize_image('#back-button', back_button_rect.width, back_button_rect.height)
        
        num_buttons = 4
        space_between_buttons = 50
        button_width = self.drawable_area.width * 0.6
        all_buttons_height = self.drawable_area.height - back_button_rect.height
        button_height = (all_buttons_height + space_between_buttons)/num_buttons - space_between_buttons
        
        easy_button_rect = pygame.Rect(
            self.drawable_area.centerx - button_width/2,  # x
            back_button_rect.bottom,        # y
            button_width,                   # width
            button_height                   # height
        )
        easy_button = pygame_gui.elements.UIButton(
            relative_rect=easy_button_rect, 
            text="easy",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#easy-button", class_id="@large-button")
        )
        
        medium_button_rect = pygame.Rect(
            self.drawable_area.centerx - button_width/2,
            easy_button_rect.bottom + space_between_buttons,
            button_width,
            button_height
        )
        medium_button = pygame_gui.elements.UIButton(
            relative_rect=medium_button_rect, 
            text="medium",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#medium-button", class_id="@large-button")
        )
        
        hard_button_rect = pygame.Rect(
            self.drawable_area.centerx - button_width/2,
            medium_button_rect.bottom + space_between_buttons,
            button_width,
            button_height
        )
        hard_button = pygame_gui.elements.UIButton(
            relative_rect=hard_button_rect, 
            text="hard",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#hard-button", class_id="@large-button")
        )

        custom_button_rect = pygame.Rect(
            self.drawable_area.centerx - button_width/2,
            hard_button_rect.bottom + space_between_buttons,
            button_width,
            button_height
        )
        custom_button = pygame_gui.elements.UIButton(
            relative_rect=custom_button_rect, 
            text="custom",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#custom-button", class_id="@large-button")
        )
        resize_image('@large-button', custom_button_rect.width, custom_button_rect.height)

    def show(self):
        redraw_elements(self.game_window.window, self.managers, 0)

        ready = False
        time_delta = math.ceil(time.time())
        while not ready:
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                
                # redraw window upon reopening after minimizing
                elif event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return self.game_window.title_screen

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "#easy-button":
                        ready = True
                        rows = 10
                        columns = 10
                        self.game_window.play_screen.set_maze_dimensions(rows, columns)
                        self.game_window.play_screen.setup()
                        return self.game_window.play_screen

                    elif event.ui_object_id == "#medium-button":
                        ready = True
                        rows = 20
                        columns = 20
                        self.game_window.play_screen.set_maze_dimensions(rows, columns)
                        self.game_window.play_screen.setup()
                        return self.game_window.play_screen

                    elif event.ui_object_id == "#hard-button":
                        ready = True
                        rows = 30
                        columns = 30
                        self.game_window.play_screen.set_maze_dimensions(rows, columns)
                        self.game_window.play_screen.setup()
                        return self.game_window.play_screen

                    elif event.ui_object_id == "#custom-button":
                        ready = True
                        return self.game_window.custom_size_screen

                    elif event.ui_object_id == "#back-button":
                        return self.game_window.title_screen
                    
                    elif (event.ui_object_id == "#audio-button") or (event.ui_object_id == "#no-audio-button"):
                        self.audio.toggle_audio()

                elif event.type == pygame.WINDOWRESTORED: # redraw window upon reopening after minimizing
                    pygame.display.update()

                self.ui_manager.process_events(event)
            
            time_delta = math.ceil(time.time()) - time_delta
            redraw_elements(self.game_window.window, self.managers, time_delta)
