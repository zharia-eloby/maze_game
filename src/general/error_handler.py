import os, traceback

class ErrorHandler:
    def handle_error(error, debug_mode, error_screen):
        if debug_mode: print(traceback.format_exc())

        # write the error to the erorr log file
        folder_path = os.path.realpath("./logs")
        file_path = os.path.join(folder_path, "error_log.txt")

        if not os.path.exists(folder_path): 
            os.mkdir(folder_path)

        with open(file_path, 'w') as f: 
            traceback.print_exc(file=f)

        # set error text for error screen
        if (type(error) == FileNotFoundError):
            filename = error.__str__().rsplit('\\')[-1].rstrip("\'\.")
            error_screen.set_error_text('Missing file: {filename}'.format(filename=filename))
        else:
            error_screen.set_error_text(error.__class__.__name__)