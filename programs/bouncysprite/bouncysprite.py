import random
from animation import Animation

# Bounces a single sprite across the display. Configure multiple bouncy sprites in the .json file to
# display more than 1 moving sprite on the display at once.
class BouncySprite(Animation):
    def __init__(self, init_x, init_y, the_sprite):
        self.name = "bouncy sprite"
        self.current_x = init_x
        self.current_y = init_y
        self.delta_x = 0
        self.delta_y = 0
        self.sprite = the_sprite

        self.trapx_min = 10
        self.trapx_max = 12
        self.trapy_min = 6
        self.trapy_max = 8

        if init_x == -1:
            self.current_x = random.randint(0, 13)

        if init_y == -1:
            self.current_y = random.randint(2, 6)

    def draw_frame(self, display):
        if (self.delta_x == 0 and self.delta_y == 0):
            self.draw_sprite(display, False)
            # Just starting out. Send the ball bouncing down and to the right 
            self.delta_x = 1
            self.delta_y = 1

            return False
        else:
            # Clear out the pixels of the old sprite before drawing the new one
            self.draw_sprite(display, True)

            # Update the sprite to the next position
            self.current_x = self.current_x + self.delta_x
            self.current_y = self.current_y + self.delta_y

            if self.current_x+2 > display.width-1 or self.current_x-2 < 0:
                self.delta_x = -self.delta_x
                self.current_x = self.current_x + self.delta_x

            if self.current_y+2 > display.height-1 or self.current_y-2 < 0:
                self.delta_y = -self.delta_y
                self.current_y = self.current_y + self.delta_y

            # Finally, draw the sprite
            self.draw_sprite(display, False)

            return False


    def draw_sprite(self, display, do_undraw):
        # The current_x and current_y coordinates should hold the current center of the sprite.
        # We will translate the sprite data based on that
        min_x = self.current_x - int(self.sprite.sprite_width / 2)
        max_x = self.current_x + int(self.sprite.sprite_width / 2)
        min_y = self.current_y - int(self.sprite.sprite_height / 2)
        max_y = self.current_y + int(self.sprite.sprite_height / 2)

        sprite_current_x = 0
        sprite_current_y = 0

        for i in range(min_y, max_y+1):
            for j in range(min_x, max_x+1):
                brightness = 0
                if not do_undraw:
                    # Grab brightness of pixel at the sprite's coordinates.
                    brightness = self.sprite.sprite_data[sprite_current_y][sprite_current_x]

                display.pixel(j, i, brightness)
                sprite_current_x = sprite_current_x + 1

            sprite_current_x = 0
            sprite_current_y = sprite_current_y + 1  
    