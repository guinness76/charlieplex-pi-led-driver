from datetime import datetime
import json
from animation import Animation
import piutils

class DigitalClock(Animation):
    def __init__(self):
        self.name = "digital_clock"
        self.current_time = "0000"
        self.seconds_brightness = 10

        characters_file = "../resources/small-numbers.json"
        with open(characters_file, 'r') as the_file:
            self.character_map = json.load(the_file)

    def draw_frame(self, display, hardware_buffering):
        now = datetime.now()
        the_time = now.strftime("%H%M")
        seconds = now.strftime("%S")

        # Clear the seconds area on the bottom
        piutils.fill_area(display, 0, 7, 15, 8, 0)
        indicator = int(seconds)

        if indicator == 0:
            pass
        elif indicator >= 1 and indicator <= 30:
            self.render_seconds_increment(display, indicator)
        elif indicator > 30:
            self.render_seconds_decrement(display, indicator)
            
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

    def render_seconds_increment(self, display, indicator):
        if indicator >= 1 and indicator <= 15:
            x = indicator-1
            piutils.draw_line(display, 0, 7, x, 7, self.seconds_brightness)
        else:
            x = indicator-16
            piutils.draw_line(display, 0, 7, 14, 7, self.seconds_brightness)
            piutils.draw_line(display, 0, 8, x, 8, self.seconds_brightness)    

    def render_seconds_decrement(self, display, indicator):
        if indicator >= 31 and indicator <= 44:
            # '15-' inverts the line
            x = 15-(45-indicator)
            piutils.draw_line(display, x, 7, 14, 7, self.seconds_brightness)
            piutils.draw_line(display, 0, 8, 14, 8, self.seconds_brightness)
        else:
            # '15-' inverts the line
            x = 15-(60-indicator)
            piutils.draw_line(display, x, 8, 14, 8, self.seconds_brightness)
    
    def render_current_time(self):
        sprites = []

        for the_char in self.current_time:
            if not the_char in self.character_map:
                raise KeyError("Character(s) '%s' is not in the map" % the_char)

            the_sprite = self.character_map[the_char]
            sprites.append(the_sprite)

        return sprites