class Animation():
    def __init__(self, name):
        self.name = name
        self.current_iteration = 0

    # Resets all position values in the Animation to the state they were in at the beginning of
    # the program. Used to implement endless loop frames in a program.
    def reset(self):
        self.current_iteration = 0

    # Passes the adafruit_is31fl3731.matrix.Matrix as the display. All you have to do is add the pixels.
    #
    # Returns True if the program has internally fulfilled all the conditions to exit. Some programs will exit
    # after certain conditions have been met (such as x number of lines have been drawn). All the animations
    # in the current frame will execute, but a new frame will not be started. The program will exit instead.
    def draw_frame(display):
        pass

class Sprite():
    def __init__(self, sprite_data, init_x, init_y):
        # todo throw error if sprite is empty
        self.sprite_data = sprite_data
        self.sprite_width = len(sprite_data[0])
        self.sprite_height = len(sprite_data)
        self.init_x = init_x
        self.init_y = init_y