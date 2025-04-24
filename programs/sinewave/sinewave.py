from animation import Animation
import math

class Sinewave(Animation):
    def __init__(self, init_x, init_y, max_x, max_y, invert):
        self.name = "sinewave"
        self.init_x = init_x
        self.init_y = init_y
        self.current_x = init_x
        self.acc_x = 0
        self.acc_xmax = max_x - init_x
        self.current_y = init_y
        self.max_x = max_x
        self.max_y = max_y
        self.invert = invert # Inverts the curve

    def reset(self):
        super().reset()
        self.current_x = self.init_x
        self.acc_x = 0   
        self.current_y = self.init_y

    def draw_frame(self, display, hardware_buffering):
        # Undraw the current pixel
        if (self.current_x-1 >= 0):
            display.pixel(self.current_x-1, self.current_y, 0)
        else:
            display.pixel(0, self.current_y, 0)

        y = math.sin(((self.acc_x)/self.acc_xmax) * math.pi)
        plottable_y = y * self.max_y

        if self.invert:
            # "8 -" inverts from "top" to "bottom"
            self.current_y = 8 - int(round(plottable_y))
        else:
            self.current_y = int(round(plottable_y))

        # print("current_x=%d, y=%f, plottable_y=%f, current_y=%d" 
        #       % (self.current_x, y, plottable_y, self.current_y))
        
        
        display.pixel(self.current_x, self.current_y, 50)

        self.acc_x = self.acc_x + 1
        self.current_x = self.current_x + 1
        # self.current_y = self.current_y + 1

        if self.current_x > self.max_x:
            return True
        else:
            return False