class Animation():
    def __init__(self, name):
        self.name = name
        self.current_iteration = 0

    # Resets all position values in the Animation to the state they were in at the beginning of
    # the program. Used to implement endless loop frames in a program.
    def reset(self):
        self.current_iteration = 0

    # Passes the adafruit_is31fl3731.matrix.Matrix as the display. The next hardware frame to draw has already
    # been configured. All you have to do is add the pixels. If 'hardware_buffering' is set to True, you can
    # assume you are working with an empty frame. But a value of False indicates that all the pixels from the
    # previous PiFrame are still on the current hardware frame of the display. Thus, you have to set some pixels
    # to 0 on the display to implement animation.
    def draw_frame(display, hardware_buffering):
        pass

class Sprite():
    def __init__(self, sprite_width, sprite_height, sprite_data, init_x, init_y):
        self.sprite_data = sprite_data
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.init_x = init_x
        self.init_y = init_y