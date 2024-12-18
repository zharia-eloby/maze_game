import logging

class ErrorHandler:
    def handle_error(error, error_screen):
        logging.exception("{error_class}:".format(error_class=error.__class__.__name__))

        # set error text for error screen
        if (type(error) == FileNotFoundError):
            filename = error.__str__().rsplit('\\')[-1].rstrip("\'.")
            error_screen.set_error_text('Missing file: {filename}'.format(filename=filename))
        else:
            error_screen.set_error_text(error.__class__.__name__)