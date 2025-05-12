from adafruit_is31fl3731.matrix import Matrix as Display
import board
import busio
import json
from piframe import PiFrame
from transform import Translation
from animation import Sprite
from programs.bouncyball.bouncyball import BouncyBall
from programs.bouncysprite.bouncysprite import BouncySprite
from programs.animate_test.animate_test import AnimateTest
from programs.sinewave.sinewave import Sinewave
from programs.clock.clock import Clock
from programs.snake.snake import Snake
from programs.marquee.marquee import Marquee
from programs.digital_clock.digitalclock import DigitalClock

class JsonLoader:
    i2c = None
    display = None
    character_map = {}
    characters_file = "../resources/characters.json"

    def setup(self, filename):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.display = Display(self.i2c)
        self.filename = filename
        self.load_character_file()

    def load_character_file(self):
        with open(self.characters_file, 'r') as the_file:
            self.character_map = json.load(the_file)

    def loadFrames(self):
        with open(self.filename, 'r') as the_file:
            json_data = json.load(the_file)
            repeating = json_data["repeating"]
            frames_json = json_data["frames"]

        config = {}
        config["repeating"] = repeating 
        piFrames = []
        config["piframes"] = piFrames

        for frame in frames_json:
            if "enabled" in frame.keys():
                enabled = frame["enabled"]
                if not enabled:
                    continue

            piFrame = PiFrame(self.display)

            if "duration_ms" in frame.keys():
                piFrame.duration_ms = frame["duration_ms"]
            
            if "iterations" in frame.keys():
                piFrame.iterations = frame["iterations"]

            background_found = False 
            if "background" in frame.keys():
                piFrame.background = frame["background"]
                background_found = True
            
            animation_found = False
            if "animations" in frame.keys():
                animations = frame["animations"]
                self.load_animations(piFrame, animations)
                animation_found = True
            
            transform_found = False
            if "transform" in frame.keys():
                transform_json = frame["transform"]
                transform_found = True

                # Controls whether to display the actual pattern in the frame (0), or just
                # skip it and run the transform first before displaying anything (1)
                if transform_json["display_before_transform"]:
                    piFrame.set_first_iteration(0)
                else:
                    piFrame.set_first_iteration(1)

                if transform_json["type"] == "translation":
                    loop_backgrond = False
                    if "loop_static_data" in transform_json:
                        loop_backgrond = transform_json["loop_static_data"]

                    translation = Translation(piFrame.width, 
                                              piFrame.height, 
                                              transform_json["translate_x"], 
                                              transform_json["translate_y"],
                                              piFrame.background,
                                              loop_backgrond)
                    
                    piFrame.transform = translation

            if not background_found and not animation_found and not transform_found: 
                print("Warning! Neither a background nor a transform nor any animations were defined in json file.")

            piFrames.append(piFrame)    

        return config
    
    def load_animations(self, piFrame, animations):
        for animation_config in animations:
            sprites = []
            if "sprites" in animation_config.keys():
                json_sprites = animation_config["sprites"]

                for json_sprite in json_sprites:
                    json_sprite_width = json_sprite["sprite_width"]
                    json_sprite_height = json_sprite["sprite_height"]
                    json_sprite_data = json_sprite["sprite_data"]
                    init_x = json_sprite["init_x"]
                    init_y = json_sprite["init_y"]

                    sprite = Sprite(json_sprite_width, json_sprite_height, json_sprite_data, init_x, init_y)
                    sprites.append(sprite)
                    
            name = animation_config["name"]
            if "bouncy ball" == name:
                init_x = animation_config["init_x"]
                init_y = animation_config["init_y"]
                piFrame.animations.append(BouncyBall(init_x, init_y))  
            elif "bouncy sprite" == name:
                init_x = animation_config["init_x"]
                init_y = animation_config["init_y"]
                piFrame.animations.append(BouncySprite(init_x, init_y, sprites[0]))
            elif "sinewave" == name:
                init_x = animation_config["init_x"]
                init_y = animation_config["init_y"]
                max_x = animation_config["max_x"]
                max_y = animation_config["max_y"]
                invert = animation_config["invert"]
                piFrame.animations.append(Sinewave(init_x, init_y, max_x, max_y, invert))
            elif "animate_test" == name:
                lines = animation_config["lines"]
                piFrame.animations.append(AnimateTest(lines))
            elif "clock" == name:
                init_x = animation_config["init_x"]
                init_y = animation_config["init_y"]
                piFrame.animations.append(Clock(init_x, init_y))
            elif "digital-clock" == name:
                piFrame.animations.append(DigitalClock())
            elif "marquee" == name:
                message = animation_config["message"]
                
                trigger_sprites_on_x = -1
                if "trigger_sprites_on_x" in animation_config:
                    trigger_sprites_on_x = animation_config["trigger_sprites_on_x"]
                
                piFrame.animations.append(Marquee(message, sprites, trigger_sprites_on_x, self.character_map))
            elif "snake" == name:
                init_x = animation_config["init_x"]
                init_y = animation_config["init_y"]
                length = animation_config["length"]
                piFrame.animations.append(Snake(init_x, init_y, length))
            else:
                print("Warning! Animation '%s' was not found in jsonloader.py" % name)