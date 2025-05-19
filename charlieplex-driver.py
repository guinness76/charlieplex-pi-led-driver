# Installation:
# sudo pip3 install adafruit-circuitpython-is31fl3731
# sudo pip3 install adafruit-circuitpython-framebuf
#
# sudo raspi-config nonint do_i2c 0
# sudo raspi-config nonint do_spi 0
# sudo raspi-config nonint do_serial_hw 0
# sudo raspi-config nonint do_ssh 0
# sudo raspi-config nonint do_camera 0
# sudo raspi-config nonint disable_raspi_config_at_boot 0
#
# sudo apt-get install -y i2c-tools libgpiod-dev python3-libgpiod
# pip3 install --upgrade adafruit-blinka
#
# To test:
# ls /dev/i2c* /dev/spi*
#
# Output should be something like:
# /dev/i2c-1  /dev/i2c-20  /dev/i2c-21  /dev/spidev0.0  /dev/spidev0.1

import sys
from jsonloader import JsonLoader
        
pwm = JsonLoader()
gt = 'programs/gradient-test/gradient-test.json'
ft = 'programs/full-test/full-test.json'
bb = 'programs/bouncyball/bouncyball.json'
bs = 'programs/bouncysprite/bouncysprite.json'
qt = 'programs/quick-test/quick-test.json'
at = 'programs/animate_test/animate-test.json'
mq = 'programs/marquee-test/marquee.json'

if len(sys.argv) > 1:
    arguments = sys.argv[1:]
    theFile = arguments[0]
    pwm.setup(theFile)
else:
    print("No arguments provided. Running full-test by default")
    pwm.setup(ft)

config = pwm.loadFrames()
frames = config['piframes']
repeating = config['repeating']

try:
    pwm.display.sleep(True)
    pwm.display.frame(0, True)
    pwm.display.sleep(False)

    running = True
    
    while running:
        for frame in frames:
            frame.runNonBufferedPiFrame()

        running = repeating
        if repeating:
            for frame in frames:
                frame.reset()
        
finally:
    pwm.display.sleep(True)


