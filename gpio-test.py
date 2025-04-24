# Simply tests the PWM GPIO pins. The program assumes that LEDs are attached to GPIO 12 and 13.

# import RPi.GPIO as GPIO
from time import sleep
from gpiozero import PWMOutputDevice

# GPIO.setmode(GPIO.BCM)

pwm0 = 12 # GPIO 12
pwm1 = 13 # GPIO 13

led0 = PWMOutputDevice(pwm0)
led1 = PWMOutputDevice(pwm1)

try:
    while True:
        # fade in
        for duty_cycle in range(0, 100, 1):
            new_value = duty_cycle/100.0
            led0.value = new_value
            led1.value = 1.0 - new_value
            sleep(0.01)

        # fade out
        for duty_cycle in range(100, 0, -1):
            new_value = duty_cycle/100.0
            led0.value = new_value
            led1.value = 1.0 - (new_value)
            sleep(0.01)

        sleep(.01)

finally:
    print("End program")
    led0.value = 0
    led1.value = 0