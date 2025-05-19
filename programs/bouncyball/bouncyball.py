# Simple animation that bounces a single pixel "ball" across the display until it contacts a square "trap"
# on the display. Then the program exits.
import random
from animation import Animation

class BouncyBall(Animation):
    def __init__(self, init_x, init_y):
        self.name = "bouncy ball"
        self.current_x = init_x
        self.current_y = init_y
        self.delta_x = 0
        self.delta_y = 0

        self.trapx_min = 10
        self.trapx_max = 12
        self.trapy_min = 6
        self.trapy_max = 8

        if init_x == -1:
            self.current_x = random.randint(0, 14)

        if init_y == -1:
            self.current_y = random.randint(0, 7)

    def draw_frame(self, display):
        if (self.delta_x == 0 and self.delta_y == 0):
            self.draw_ball(display)
            # Just starting out. Send the ball bouncing down and to the right 
            self.delta_x = 1
            self.delta_y = 1

            return False
        else:
            self.undraw_ball(display)
            
            # Update the ball to the next position
            self.current_x = self.current_x + self.delta_x
            self.current_y = self.current_y + self.delta_y

            if self.current_x > display.width -1 or self.current_x < 0:
                self.delta_x = -self.delta_x
                # Add delta_x twice, otherwise ball will appear to freeze for a moment
                self.current_x = self.current_x + self.delta_x + self.delta_x

            if self.current_y > display.height -1  or self.current_y < 0:
                self.delta_y = -self.delta_y
                # Add delta_y twice, otherwise ball will appear to freeze for a moment
                self.current_y = self.current_y + self.delta_y + self.delta_y

            # Draw the trap
            self.draw_trap(display)

            # Finally, draw the ball
            self.draw_ball(display)

            return self.in_trap(display)
        
    def undraw_ball(self, display):
        display.pixel(self.current_x, self.current_y, 0)
        display.pixel(self.current_x-1, self.current_y, 0)
        display.pixel(self.current_x+1, self.current_y, 0)
        display.pixel(self.current_x, self.current_y-1, 0)
        display.pixel(self.current_x, self.current_y+1, 0)    

    def draw_ball(self, display):
        debug = False

        display.pixel(self.current_x, self.current_y, 50)
        if debug:
            print("Drawing pixel 0 at (%d, %d) on frame %d" % (self.current_x, self.current_y, display._frame))

        if self.current_x-1 > -1:
            if debug:
                print("Drawing pixel 1 at (%d, %d) on frame %d" % (self.current_x-1, self.current_y, display._frame))
            display.pixel(self.current_x-1, self.current_y, 10)

        if self.current_x+1 < display.width:
            if debug:
                print("Drawing pixel 2 at (%d, %d) on frame %d" % (self.current_x+1, self.current_y, display._frame))
            display.pixel(self.current_x+1, self.current_y, 10)

        if self.current_y-1 > -1:
            if debug:
                print("Drawing pixel 3 at (%d, %d) on frame %d" % (self.current_x, self.current_y-1, display._frame))  
            display.pixel(self.current_x, self.current_y-1, 10)

        if self.current_y+1 < display.height:
            if debug:
                print("Drawing pixel 4 at (%d, %d) on frame %d" % (self.current_x, self.current_y+1, display._frame)) 
            display.pixel(self.current_x, self.current_y+1, 10)

    def draw_trap(self, display):
        for i in range(self.trapx_min, self.trapx_max + 1):
            display.pixel(i, self.trapy_min, 50)

        display.pixel(self.trapx_min, 7, 50)
        display.pixel(self.trapx_max, 7, 50)    

        for i in range(self.trapx_min, self.trapx_max + 1):
            display.pixel(i, self.trapy_max, 50)


    def in_trap(self, display):
        in_trap = False
        if (self.current_x >= self.trapx_min and self.current_x <= self.trapx_max):
            if (self.current_y >= self.trapy_min and self.current_y <= self.trapy_max):
                # Ball has fallen into trap. Stop the animation
                print("Ball has fallen into trap!")
                display.fill(0)
                in_trap = True

        return in_trap    
    