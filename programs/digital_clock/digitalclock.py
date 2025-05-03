from datetime import datetime
import json
from animation import Animation

class DigitalClock(Animation):
    def __init__(self):
        self.name = "digital_clock"
        self.current_time = "0000"

        characters_file = "../resources/small-numbers.json"
        with open(characters_file, 'r') as the_file:
            self.character_map = json.load(the_file)

    def draw_frame(self, display, hardware_buffering):
        now = datetime.now()
        the_time = now.strftime("%H%M")
        seconds = now.strftime("%S")

        # TODO Draw the seconds dots on the bottom
        indicator = int(seconds)
        
        # if indicator <= 15:
        #     display.pixel(indicator, 7, 25)
        # elif indicator > 15 and indicator <= 30:
        #     display.pixel(indicator-15, 8, 25)
        # elif indicator > 30 and indicator <= 45:
        #     display.pixel(indicator-30, 7, 0)
        # else:
        #     display.pixel(indicator-45, 8, 0)
        

        # Don't update the numbers if hours and minutes did not change
        if self.current_time == the_time:
            return False
        else:
            self.current_time = the_time

        # Start *near* the bottom left
        acc_x = 0
        acc_y = 1

        sprites = self.render_current_time()
        # i is rows, j is values within that row
        for i in range(0, len(sprites)):
            sprite = sprites[i]
            for j in range(0, len(sprite)):
                row = sprite[j]
                for k in range(0, len(row)):
                    brightness = row[k]
                    display.pixel(k+acc_x, j+acc_y, brightness)

            if (i == 1):
                # Leave a space between hours and minutes
                acc_x = acc_x + 5
            else:
                acc_x = acc_x + 4

        return False
    
    def render_current_time(self):
        sprites = []
        # sprite_rows = []    

        for the_char in self.current_time:
            if not the_char in self.character_map:
                raise KeyError("Character(s) '%s' is not in the map" % the_char)

            the_sprite = self.character_map[the_char]
            sprites.append(the_sprite)
            # sprite_rows.append(the_sprite)

        return sprites

        # Each row from all the sprites must be stitched together.
        # for i in range(0, 9):
        #     current_row = 0
        #     full_row = []
        #     for sprite in sprite_rows:
        #         sprite_row = sprite[i]

        #         for j in range(0, len(sprite_row)):
        #             full_row.append(sprite_row[j])

        #     current_row = current_row + 1
        #     sprites.append(full_row)

        # return sprites