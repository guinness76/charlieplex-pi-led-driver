# Uses the resources/characters.json file to display a moving marquee of text. This example also combines
# an image of a cat and some animation, before displaying the scrolling message about the bad kitty.
from time import sleep
from animation import Animation
from transform import Translation

class Marquee(Animation):
    def __init__(self, message, other_sprites, trigger_sprites_on_x, character_map):
        self.name = "marquee"
        self.message = message
        self.acc_x = 0
        self.max_x = 0
        self.trigger_sprites_on_x = trigger_sprites_on_x
        self.poo_sprite_x = -1
        self.poo_sprite_y = -1

        if len(other_sprites) > 0:
            self.poo_sprite_x = other_sprites[0].init_x
            self.poo_sprite_y = other_sprites[0].init_y
            self.poo_translate = Translation(1, 3, 0, 1, other_sprites[0].sprite_data, False)
        else:
            self.poo_translate = None

        self.character_map = character_map
        self.message_sprites = []
        self.other_sprites = other_sprites
        self.translation = None

        self.load_char_sprites()

    def load_char_sprites(self):
        total_len = 0
        sprites = []    

        expression_started = False
        expression_chars = ""

        for the_char in self.message:
            expression_finished = the_char == '}'
            if the_char == '{':
                expression_started = True
                continue
            elif expression_started and not expression_finished:
                expression_chars = expression_chars + the_char
                continue
            elif expression_finished:
                expression_started = False
                expression_finished = False
                the_char = expression_chars
                expression_chars = ""

            if not the_char in self.character_map:
                raise KeyError("Character(s) '%s' is not in the map" % the_char)

            the_sprite = self.character_map[the_char]
            sprites.append(the_sprite)
            total_len = total_len + len(the_sprite[0])

        # Each row from all the sprites must be stitched together.
        for i in range(0, 9):
            current_row = 0
            full_row = []
            for sprite in sprites:
                sprite_row = sprite[i]

                for j in range(0, len(sprite_row)):
                    full_row.append(sprite_row[j])

            current_row = current_row + 1
            self.message_sprites.append(full_row)

        self.max_x = total_len
        self.translation = Translation(self.max_x, 9, -1, 0, self.message_sprites, False)

    def reset(self):
        super().reset()
        self.acc_x = 0  
        self.translation.reset()

    def draw_frame(self, display):        
        self.acc_x = self.acc_x + 1
        if self.poo_translate is not None and self.trigger_sprites_on_x > 0 and self.acc_x > self.trigger_sprites_on_x:
            # Draw and animate the "other" sprites here that were specified in the json file
            poo_sprite = self.other_sprites[0]

            if poo_sprite.init_y == self.poo_sprite_y:
                self.draw_other_sprite(display, poo_sprite, self.poo_translate.static_data)
                self.poo_sprite_y = self.poo_sprite_y + 1
                return False
            elif self.poo_sprite_y - poo_sprite.init_y == 1 or self.poo_sprite_y - poo_sprite.init_y == 2:
                self.draw_other_sprite(display, poo_sprite, self.poo_translate.do_transform())
                self.poo_sprite_y = self.poo_sprite_y + 1
                return False
            else:
                # Draw the plop. This is also the "animation is done" condition.
                plop_sprite = self.other_sprites[1]
                self.draw_other_sprite(display, plop_sprite, plop_sprite.sprite_data)
                sleep(0.5)  # Allow a bit of time to gasp in horror at the poop
                return True
        elif self.acc_x >= self.max_x:
            return True
        else:
            # Draw the kitty
            data = self.translation.do_transform()

            # i is rows, j is values within that row
            for i in range(0, len(data)):
                row = data[i]
                for j in range(0, len(row)):
                    brightness = data[i][j]

                    display.pixel(j, i, brightness)

            return False
        
    def draw_other_sprite(self, display, sprite, data):
        for i in range(0, len(data)):
            row = data[i]
            for j in range(0, len(row)):
                brightness = data[i][j]

                display.pixel(j+sprite.init_x, i+sprite.init_y, brightness)