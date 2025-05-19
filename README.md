# charlieplex-pi-led-driver
These examples utilize the `LED Charlieplexed Matrix - 9x16 LEDs` and the `Adafruit 16x9 Charlieplexed PWM LED Matrix Driver - IS31FL3731`, which are both available from https://www.adafruit.com. The driver uses I2C to send pixel draw messages from the Raspberry Pi. In order to use these examples, you have to run these commands on your Raspberry Pi:

```sh
# Installs the python libraries needed by the IS31FL3731 driver
sudo pip3 install adafruit-circuitpython-is31fl3731
sudo pip3 install adafruit-circuitpython-framebuf

# Installs libraries that can be used to troubleshoot I2C comms on the Pi
sudo apt-get install -y i2c-tools libgpiod-dev python3-libgpiod

# To test:
ls /dev/i2c* /dev/spi*

# Output should be something like:
# /dev/i2c-1  /dev/i2c-20  /dev/i2c-21  /dev/spidev0.0  /dev/spidev0.1
```

# Code structure
The main data structure of this application is the PiFrame, defined in piframe.py. The main loop in charlieplex-driver.py loops over all the frames. For each frame, runNonBufferedPiFrame() is called. If the "repeating" value is set in the config .json file, the frames loop will continue forever until the entire program is halted (Ctrl-C on a Linux system to kill the program). After all the frames have been executed in a loop, the reset() function is called on each frame. This gives frames a chance to reset their internal data structures to their original values in preparation for the next frame iteration. This comes in handy because animation frames tend to increment internal variables to implement a certain animation.

# Static frames vs animations
Some of the example programs use a matrix of static data for a frame. The static data is defined in a "background" field in the .json file. A transform is then configured in the background to cause the background to "move" across the screen as needed. The transform is applied to each frame to implement the background's movement.

Other example programs extend the Animation class in animation.py. Extending classes implement the `draw_frame()` function, and are passed a `adafruit_is31fl3731.matrix.Matrix` object (the object is called "display" in the calling function). With this display object, you can add any pixels that are needed to implement one frame of animation. You will have to keep track of what you have displayed in internal variables, so that you can properly update the animation on the next frame.

# Combining animation elements
One of the handy features of these programs is that you can combine a background, one or more sprites, and custom drawn pixels onto the same animation frame. See the `background` and `sprite_data` sections in the config file examples below.

# Hardware buffering
The Adafruit Charlieplexed IS31FL3731 driver has support for multiple hardware frames. This means that data could be written to one display frame while a different display frame is displayed. In reality, it was found that that using multiple display frames on the IS31FL3731 seemed to produce a lot of flickering and "ghost" pixels to be displayed. Thus, these examples all write to pixels in a single device frame. This does cause more work for the animation code, as pixels that are currently lit may need to have their brightness set to 0 when a new frame is displayed (to produce the illusion of movement).

# Config file properties
Every program in the programs folder holds a .json file, which defines how the frames are configured. This .json file is supplied as a command line argument when starting charlieplex-driver.py. The .json file is read by jsonloader.py.

## json file example 1
```json
{
    "repeating": false,
    "frames": [
        {
            "enabled": true,
            "background": {
                "data": [ 
                    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
                    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
                    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
                    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
                    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
                    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
                    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
                    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
                    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0]
                ],
                "transform": {
                    "display_before_transform": true,
                    "translate_x": 1,
                    "translate_y": 0,
                    "loop_static_data": true
                }
            },
            "duration_ms": 100,
            "iterations": 30
        }
    ]   
}
```

## json file example 2
```json
{
    "repeating": false,
    "frames": [
        {
            "enabled": true,
            "duration_ms": 100,
            "animations": [
                {
                    "name": "bouncy ball",
                    "init_x": 1,
                    "init_y": -1,
                    "sprites": [
                        {
                            "name": "static sprite",
                            "init_x": 10,
                            "init_y": 6,
                            "sprite_data": [ 
                            [50,  50,  50],
                            [50,   0,  50],
                            [50,  50,  50]
                            ]
                        }
                    ] 
                }
            ]
        }
    ]
}
```

## repeating
Set value to "true" or "false". If set to "true", all the frames in the .json file will be run sequentially in a repeating loop. If set to "false", all the frames will be executed once sequentially and then the program exits. Note that an animation controls its own flow when called as part of a frame. An animation can choose to loop in its own, which means that the program is locked onto a single frame while the animation loops on itself.

## enabled
Set value to "true" or "false. When set to "false", the frame will not be executed by the program. This is useful when you don't want to display a certain frame, but you also don't want to lose the frame's configuration.

## duration_ms
Integer value in milliseconds. After drawing a frame, the program will sleep for this number of milliseconds until drawing the next frame. The current frame is still visible on the display while the program is sleeping. Set to -1 to display the current frame forever (useful for a static display of 1 frame).

## iterations
Optional integer value. When set to a value > 1, this runs a loop within a frame for the specified number of durations. This is used with a background and a transform to produce a scrolling effect.
        
## background
Holds a matrix of brightness data that acts as a map of which LEDs to light when the program runs. The value in the (0, 0) position of the matrix corresponds to the (0, 0) position on the screen. The background is not needed when the frame is configured with an animation, although some animations do have a static background defined. Example background matrix:
```
[ 
    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0],
    [0,   5,  10,  25,  50, 100, 150, 200, 255,   0,   0,   0,  0,  0,  0, 0]
]
```                

## transform
A transform is applied to the background in a frame to move the frame in an 'x' or 'y' direction. A frame transform is useful when combined with a background. The transform can scroll the background in the x or y directions whenever a new frame is drawn.

### display_before_transform
Value can be set to "true" or "false". If set to "true", the static image set in the transform will display before the image is shifted in any direction. If "false", the static image will not be displayed until the transform has been run at least once. Useful when running frames with transforms that sweep to one edge of the screen, and then sweep back in the opposite direction.

### loop_static_data
Value can be set to "true" or "false". If set to "true", this will cause the transform's static data to loop around itself when the end of the static data is reached. If "false", the program will just provide rows of 0 brightness to the area vacated by the transform. Useful if the transform's static data is sized to be able to produce a perfect loop.

### translate_x
Integer value. When each frame is drawn, the transform will shift its static data on the screen by this amount in the x direction. The value can be positive, negative or 0.

### translate_y
Integer value.  When each frame is drawn, the transform will shift its static data on the screen by this amount in the y direction. The value can be positive, negative or 0.

## animations
An animation is used to animate pixels on a frame and uses the Animation and Sprite classes in animation.py. You can define static data inside multiple Sprites and then move them along the screen. In addition, you can draw pixels on the frame directly to create the animation effect. Any number of animations can be added to a frame.

### name
The name of the animation. This name must be defined in jsonloader.py.

### init_x
An optional integer value from 0 to 16. Allows an animation to begin displaying pixels in a specific location on a screen. Setting the value to -1 indicates to the animation that a random x value can be chosen.

### init_y
An optional integer value from 0 to 8.  Allows an animation to begin displaying pixels in a specific location on a screen. Setting the value to -1 indicates to the animation that a random y value can be chosen.

## sprites
Any number of sprite objects can be added to an animation frame. Each sprite can then be updated on the screen when the frame is drawn.

### name
Used for labeling only within the json file. This can be any string value.

### init_x
Integer value from 0 to 15. Set to -1 to set the value to a random value on startup.

### init_y
Integer value from 0 to 8. Set to -1 to set the value to a random value on startup.

### sprite_data
The static data matrix that graphically represents the sprite on the screen. The value in the (0, 0) position of the matrix corresponds to the init_x and init_y values when displayed on the screen. Each value in the matrix is a brightness value from 0 to 255. Example matrix:
```
[ 
    [  0,   5,  15,   5,   0],
    [  5,  50,  50,  50,   5],
    [ 15,  50, 150,  50,  15],
    [  5,  50,  50,  50,   5],
    [  0,   5,  15,   5,   0]
]
```                            


