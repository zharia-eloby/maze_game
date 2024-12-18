import os, sys
from pathlib import Path

def get_file_path(relative_path, temp_file=True):
    # if running executable
    if hasattr(sys, "_MEIPASS"): 
        if temp_file:
            base_path = sys._MEIPASS
        else: 
            os.makedirs(os.path.dirname(relative_path), exist_ok=True)
            base_path = os.path.dirname(sys.executable)

        return os.path.join(base_path, relative_path)
    
    # if running from source
    base_path = Path(__file__).parent
    os.makedirs(os.path.dirname(relative_path), exist_ok=True)
    return os.path.join(os.path.realpath(base_path), os.path.realpath(relative_path))
    
def get_opposite_direction(direction):
    if direction == "left": return "right"
    elif direction == "right": return "left"
    elif direction == "up": return "down"
    elif direction == "down": return "up"