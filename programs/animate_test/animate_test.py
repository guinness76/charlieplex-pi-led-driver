# Simple program that displays some lines on the display. The lines to display are configured in the .json file.
from animation import Animation
import piutils

class AnimateTest(Animation):
    def __init__(self, lines):
        self.name = "animate_test"
        self.lines = lines

    def reset(self):
        super().reset()
         

    def draw_frame(self, display):
        for line in self.lines:
            init_x = line['init_x']
            init_y = line['init_y']
            max_x = line['max_x']
            max_y = line['max_y']
            brightness = line['brightness']
            piutils.draw_line(display, init_x, init_y, max_x, max_y, brightness)
        
        return False