import math
from classes.screen import Screen

class Modal(Screen):
    def __init__(self, game_window):
        super().__init__(game_window)
        self.width = math.floor(self.drawable_area.width * 0.66)
        self.height = math.floor(self.drawable_area.height * 0.5)
        self.margin = 40
        self.line_spacing = 10