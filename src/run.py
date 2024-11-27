import pygame, sys, threading
from general.settings import Settings
from general.game_window import GameWindow
from screens.loading_screen import LoadingScreen
from screens.error_screen import ErrorScreen
from general.audio import Audio
from general.error_handler import ErrorHandler

def load_content(game_window, settings, error_screen):
    try:
        audio = Audio(settings)
        game_window.loaded_percent = 0.11
        game_window.initialize_screens(audio)
        game_window.loaded_percent = 0.88
        audio.initialize()
        game_window.loaded_percent = 1
        game_window.finished_loading = True
    except Exception as e:
        game_window.error = True
        ErrorHandler.handle_error(e, settings.debug_mode, error_screen)

def show_loading_screen(game_window, settings, error_screen):
    try:
        loading_screen = LoadingScreen(game_window)
        loading_screen.setup()
        loading_screen.show()
    except Exception as e:
        game_window.error = True
        ErrorHandler.handle_error(e, settings.debug_mode, error_screen)

def run():
    settings = Settings()
    settings.load_settings()

    gw = GameWindow(settings)
    gw.initialize()

    error_screen = ErrorScreen(gw)
    error_screen.setup()

    load_content_thread = threading.Thread(target=load_content, args=(gw,settings,error_screen))
    loading_screen_thread = threading.Thread(target=show_loading_screen, args=(gw,settings,error_screen))
    load_content_thread.start()
    loading_screen_thread.start()
    load_content_thread.join()
    loading_screen_thread.join()

    pygame.event.clear()

    if (gw.error):
        error_screen.show()
    else:
        try:
            next_page = gw.title_screen
            done = False
            while not done:
                next_page = next_page.show()
                if not next_page:
                    done = True
                pygame.event.clear()

            settings.user_settings["background_audio"]['volume'] = pygame.mixer.Channel(0).get_volume()
            settings.user_settings["sound_fx"]['volume'] = pygame.mixer.Channel(1).get_volume()
            settings.save_settings()
        except Exception as e:
            gw.error = True
            ErrorHandler.handle_error(e, True, error_screen=error_screen)
            pygame.event.clear()
            error_screen.show()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run()
