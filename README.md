# charlieplex-pi-led-driver
TODO

The main data structure of this application is the PiFrame, defined in piframe.py. The main loop in charlieplex-driver.py loops over all the frames. For each frame, runPiFrame() or runNonBufferedPiFrame() is called (see the Hardware buffering section below for the differences between these functions). If the "repeating" value is set in the config .json file, the frames loop will continue forever until the entire program is halted (Ctrl-C on a Linux system to kill the program). After all the frames have been executed in a loop, the reset() function is called on each frame. This gives frames a chance to reset their internal data structures to their original values in preparation for the next frame iteration. This comes in handy because animation frames tend to increment internal variables to implement a certain animation.

## Hardware buffering
The Adafruit Charlieplexed IS31FL3731 driver has support for multiple hardware frames. This means that data can be written to one frame while a different frame is displayed. To support this, the PiFrame class is coded to write to these hardware frames if XXX TODO is set to True. The class manages displaying one hardware frame will allowing other classes to write to another hardware frame that is currently invisible. When a new iteration of frames is started, the previously invisible hardware frame will be displayed, and the class will move on to allow other classes to write to a different invisible hardware frame.

In reality, it was found that that using hardware frames seemed to produce a lot more flickering than was expected for some programs. In fact, some programs looked a lot better when multiple hardware frames was *not* used. TODO This is still WIP.

## Config file properties
{
    "repeating": "true" or "false". If set to "true", all the frames in the .json file will be run sequentially in a repeating loop. If set to "false", all the frames will be executed once sequentially and then the program exits. Note that an animation controls its own flow when called as part of a frame. An animation can choose to loop in its own, which means that the program is locked onto a single frame while the animation loops on itself.
    "frames": {
        "enabled": "true" or "false". When set to "false", the frame will not be executed by the program. This is useful when you don't want to display a certain frame, but you also don't want to lose the frame's configuration.
        "duration_ms": integer value in milliseconds. TODO.
        "iterations": integer value. TODO.
        "background". Holds a matrix of brightness data that acts as a map of which LEDs to light when the program runs. 
        "transform": {
            "type": Current the only transform type is "translation". At some point, "rotation" and "scaling" transforms should be added.
            "display_before_transform": "true" or "false". TODO.
            "loop_static_data": "true" or "false". If "true", this will cause the transform's static data to loop around itself when the end of the static data is reached. If "false", the program will just provide rows of 0 brightness to the area vacated by the transform. Useful if the transform's static data is sized to be able to produce a perfect loop.
            "translate_x": integer value. TODO.
            "translate_y": integer value. TODO.
        }
        "animations": [
            {
                "name": The name of the animation. This name must be defined in jsonloader.py.
                "init_x". An integer value. TODO.
                "init_y". An integer value. TODO.
                "sprites" [
                    {
                        "name": Used for labeling only within the json file. This can be any string value.
                        "sprite_width": integer value from 1 to 16. TODO.
                        "sprite_height": integer value from 1 to 9. TODO.
                        "init_x": integer value from 0 to 15. Set to -1 to set the value to a random value on startup.
                        "init_y": integer value from 0 to 9. Set to -1 to set the value to a random value on startup.
                        "sprite_data": TODO.
                    }
                ]  
            }
        ]
        
    }
}


