from animation import Animation

class Clock(Animation):
    def __init__(self, init_x, init_y):
        self.name = "clock"
        self.current_x = init_x
        self.current_y = init_y
        self.current_time = 11

    def draw_frame(self, display, hardware_buffering):
        brightness = 100
        display.pixel(self.current_x, self.current_y, brightness)

        # minutes hand
        for i in range(self.current_y-3, self.current_y):
            display.pixel(self.current_x, i, brightness)

        # hours hand
        if self.current_time == 1:
            display.pixel(self.current_x+1, self.current_y-1, brightness)
            display.pixel(self.current_x+1, self.current_y-2, brightness)
            self.current_time = 2
        elif self.current_time == 2:
            display.pixel(self.current_x+1, self.current_y-1, brightness)
            display.pixel(self.current_x+2, self.current_y-1, brightness)
            self.current_time = 3
        elif self.current_time == 3:
            # 3 o clock
            display.pixel(self.current_x+1, self.current_y, brightness)
            display.pixel(self.current_x+2, self.current_y, brightness)
            self.current_time = 4
        elif self.current_time == 4:
            display.pixel(self.current_x+1, self.current_y+1, brightness)
            display.pixel(self.current_x+2, self.current_y+1, brightness)
            self.current_time = 5
        elif self.current_time == 5:
            display.pixel(self.current_x+1, self.current_y+1, brightness)
            display.pixel(self.current_x+1, self.current_y+2, brightness)
            self.current_time = 6
        elif self.current_time == 6:
            # 6 o clock
            display.pixel(self.current_x, self.current_y+1, brightness)
            display.pixel(self.current_x, self.current_y+2, brightness)
            self.current_time = 7
        elif self.current_time == 7:
            display.pixel(self.current_x-1, self.current_y+1, brightness)
            display.pixel(self.current_x-1, self.current_y+2, brightness)
            self.current_time = 8
        elif self.current_time == 8:
            display.pixel(self.current_x-1, self.current_y+1, brightness)
            display.pixel(self.current_x-2, self.current_y+1, brightness)
            self.current_time = 9
        elif self.current_time == 9:
            display.pixel(self.current_x-1, self.current_y, brightness)
            display.pixel(self.current_x-2, self.current_y, brightness)
            self.current_time = 10
        elif self.current_time == 10:
            display.pixel(self.current_x-1, self.current_y-1, brightness)
            display.pixel(self.current_x-2, self.current_y-1, brightness)
            self.current_time = 11
        elif self.current_time == 11:
            display.pixel(self.current_x-1, self.current_y-1, brightness)
            display.pixel(self.current_x-1, self.current_y-2, brightness)
            self.current_time = 12
        else:
            # default to noon
            display.pixel(self.current_x, self.current_y-1, brightness)
            display.pixel(self.current_x, self.current_y-2, brightness)
            self.current_time = 1