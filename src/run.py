import pygame, sys, threading, logging
from src.general.settings import Settings
from src.general.game_window import GameWindow
from src.screens.loading_screen import LoadingScreen
from src.screens.error_screen import ErrorScreen
from src.general.audio import Audio
from src.general.error_handler import ErrorHandler

def load_content(game_window, audio, error_screen):
    try:
        game_window.loaded_percent = 0.11
        game_window.initialize_screens(audio)
        game_window.loaded_percent = 0.88
        audio.initialize()
        game_window.loaded_percent = 1
        game_window.finished_loading = True
        
        logging.info("Successfully loaded content")
    except Exception as e:
        game_window.error = True
        ErrorHandler.handle_error(e, error_screen)

def show_loading_screen(game_window, error_screen):
    try:
        loading_screen = LoadingScreen(game_window)
        loading_screen.setup()
        loading_screen.show()
    except Exception as e:
        game_window.error = True
        ErrorHandler.handle_error(e, error_screen)

def run():
    settings = Settings()

    logging.info("APPLICATION START ({version})".format(version=settings.version_info))

    try:
        settings.load_settings()

        gw = GameWindow(settings)
        gw.initialize()

        error_screen = ErrorScreen(gw)
        error_screen.setup()

        audio = Audio(settings)
    except Exception as e:
        logging.exception("Error while performing inital setup ({error_class})".format(error_class=e.__class__.__name__))
        pygame.quit()
        sys.exit()

    load_content_thread = threading.Thread(target=load_content, args=(gw,audio,error_screen))
    loading_screen_thread = threading.Thread(target=show_loading_screen, args=(gw,error_screen))
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

            audio.update_audio_settings()
            settings.save_settings()
        except Exception as e:
            gw.error = True
            ErrorHandler.handle_error(e, error_screen=error_screen)
            pygame.event.clear()
            error_screen.show()

    logging.info("APPLICATION END")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run()
