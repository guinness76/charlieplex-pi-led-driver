# Displays a 6-pixel-long snake roaming across the display and randomly changing directions.
import random
from animation import Animation
from piutils import Mixel

class Snake(Animation):
    def __init__(self, init_x, init_y, length):
        self.name = "snake"
        self.init_x = init_x
        self.init_y = init_y
        self.length = length
        self.pos = []
        self.debug = False
        self.trace = False
        if init_x < 0:
            # Random value
            self.init_x = random.randint(0, 8)

        if init_y < 0:
            # Random value
            self.init_y = random.randint(0, 8)
        
        self.new_snake()
        
    def new_snake(self):
        self.pos = []

        # Snake will start out being a straight line
        for i in range(0, self.length):
            id = str(i)
            if i == self.length-1:
                id = "head"
            elif i == 0:
                id = "tail"

            mixel = Mixel(id, i + self.init_x, self.init_y, 1, 0, 20)
            self.pos.append(mixel)


    def reset(self):
        super().reset()
         

    def draw_frame(self, display):
        head = len(self.pos)-1

        # Remember that we are starting from opposite side of the origin coordinates and working our
        # way backwards. Thus, the origin coordinates actually specify the tail.
        for i in range(head, -1, -1):
            mixel = self.pos[i]

            # Undraw the tail
            if (i == 0):
                display.pixel(mixel.pos_x, mixel.pos_y, 0)

            # Calculate the next position
            next_x = mixel.pos_x + mixel.translate_x
            next_y = mixel.pos_y + mixel.translate_y

            if self.trace:
                print("draw_frame() after calculating next position: mixel.id=[%s], mixel.pos_x=%d, mixel.pos_y=%d, next_x=%d ,next_y=%d" \
                      % (mixel.id, mixel.pos_x, mixel.pos_y, next_x, next_y)) 

            dir_changes = mixel.upcoming_dir_changes
            dir_change_applied = False
            for upcoming_dir_change in dir_changes:
                if upcoming_dir_change.x == next_x and upcoming_dir_change.y == next_y:
                    self.applyDirectionChange(mixel, upcoming_dir_change, head, i == 0)
                    dir_change_applied = True   

            if not dir_change_applied:
                mixel_change = None
                if i == head:
                    # See if the head needs to change direction on the next iteration
                    mixel_change = self.handleHead(mixel, next_x, next_y, display.width, display.height)

                    if mixel_change is not None:
                        if (self.debug):
                            print("handleHead() results: %s" % mixel_change.to_string())

                        # When the head is about to hit a wall or a corner, all the other mixels need to be informed so that 
                        # they can turn at the edge of the wall/corner. We do this by adding a dir_change to the mixel.
                        # All the mixels will adjust their direction when their next coordinates matches the 
                        # coordinates of one of the dir_changes.
                        for j in range(head-1, -1, -1):
                            next_mixel = self.pos[j]
                            next_dir_change = next_mixel.add_dir_change(mixel.pos_x, mixel.pos_y, \
                                mixel_change.new_translate_x, mixel_change.new_translate_y)   

                            if self.debug:
                                print("""Upcoming dir change %s applied to mixel[%s]. Dir change should happen on coordinates (%d, %d)""" \
                                    % (next_dir_change.to_string(), next_mixel.id, mixel.pos_x, mixel.pos_y))
                                
                        # Adjust the location and the direction of the head mixel as needed, as the next coordinates may be 
                        # beyond the walls
                        next_x = mixel_change.updated_x
                        next_y = mixel_change.updated_y
                        mixel.translate_x = mixel_change.new_translate_x
                        mixel.translate_y = mixel_change.new_translate_y

                mixel.set_pos_x(next_x)
                mixel.set_pos_y(next_y)                                                                 

            # Draw the current pixel
            if mixel.pos_x < 0 or mixel.pos_x > 15 or mixel.pos_y < 0 or mixel.pos_y > 9:
                print("Some kind of problem here. mixel.id=%s, mixel.pos_x=%d, mixel.pos_y=%d, next_x=%d, next_y=%d" \
                      % (mixel.id, mixel.pos_x, mixel.pos_y, next_x, next_y))
                # A debug breakpoint is placed here as needed
                deadbeef = 0

            if self.trace:
                print("Drawing mixel[%s] at (%d,%d)" % (mixel.id, mixel.pos_x, mixel.pos_y))
            
            brightness = mixel.brightness
            if (i == head):
                brightness = 150
            display.pixel(mixel.pos_x, mixel.pos_y, brightness)
        return False

    def applyDirectionChange(self, mixel, upcoming_dir_change, head, is_tail):
        # Dir change is in effect. Apply it to the next translation of the current mixel.
        # But apply the existing translation first, so that this mixel is still placed in the correct
        # position for this iteration
        if self.debug:
            print("About to apply direction change %s to mixel[%s]. Old coordinates:(%d, %d)" \
                % (upcoming_dir_change.to_string(), mixel.id, mixel.pos_x, mixel.pos_y))
 
        mixel.set_pos_x(mixel.pos_x + mixel.translate_x)
        mixel.set_pos_y(mixel.pos_y + mixel.translate_y)

        mixel.translate_x = upcoming_dir_change.translate_x
        mixel.translate_y = upcoming_dir_change.translate_y

        if self.debug:
            print("Applied direction change %s to mixel[%s]. New coordinates:(%d, %d). translate_x=%d, translate_y=%d" \
                % (upcoming_dir_change.to_string(), mixel.id, mixel.pos_x, mixel.pos_y, mixel.translate_x, \
                    mixel.translate_y))

        if is_tail:
            # We are on the tail. The oldest dir change should have been applied to all mixels at this point,
            # so clear the dir change.
            for j in range(head-1, -1, -1):
                old_id = self.pos[j].pop_dir_change()
                if self.debug:
                    print("On the tail. Cleared upcoming dir change %d from mixel[%s]." % (old_id, self.pos[j].id))

    def handleHead(self, mixel, next_x, next_y, display_width, display_height):
        if self.debug:
            print("handleHead() called for mixel[%s]: mixel.pos=(%d, %d), mixel.translate=[%d, %d], next_x=%d, next_y=%d)" % \
                (mixel.id, mixel.pos_x, mixel.pos_y, mixel.translate_x, mixel.translate_y, next_x, next_y))
            
        right_wall = display_width-1
        top_wall = display_height-1
        
        if mixel.pos_x == 0 and mixel.pos_y == 0 and (mixel.translate_x == -1 or mixel.translate_y == -1):
            return self.handleBottomLeft(mixel)
        elif mixel.pos_x == 0 and mixel.pos_y == top_wall and (mixel.translate_x == -1 or mixel.translate_y ==1):
            return self.handleTopLeft(mixel)
        elif mixel.pos_x == right_wall and mixel.pos_y == 0 and (mixel.translate_x == 1 or mixel.translate_y == -1):
            return self.handleBottomRight(mixel)
        elif mixel.pos_x == right_wall and mixel.pos_y == top_wall and (mixel.translate_x == 1 or mixel.translate_y == 1):
            return self.handleTopRight(mixel)
        elif mixel.pos_x == 0 or mixel.pos_x == right_wall:
            return self.handleLeftRightWall(mixel, next_x, next_y)
        elif mixel.pos_y == 0 or mixel.pos_y == top_wall:
            return self.handleBottomTopWall(mixel, next_x, next_y)
        else:
            # For a potential direction change, we can't let the snake loop back on itself in the opposite direction
            left_ok = mixel.translate_x != 1
            right_ok = mixel.translate_x != -1
            up_ok = mixel.translate_y != -1
            down_ok = mixel.translate_y != 1
            if self.trace:
                print("handleHead calling maybeNewDirection()")
            return self.maybeNewDirection(up_ok=up_ok, down_ok=down_ok, left_ok=left_ok, right_ok=right_ok, \
                                          next_x=next_x, next_y=next_y, mixel=mixel)
        
    def maybeNewDirection(self, up_ok, down_ok, left_ok, right_ok, next_x, next_y, mixel):
        translate_x = mixel.translate_x
        translate_y = mixel.translate_y
        if self.trace:
            print("maybeNewDirection() start: up_ok=%s, down_ok=%s, left_ok=%s, right_ok=%s, translate_x=%d, translate_y=%d" % \
                  (up_ok, down_ok, left_ok, right_ok, translate_x, translate_y))

        random_direction = random.randint(0, 16)
        if random_direction <= 3:
            # Time to randomly change direction 90 degrees

            if random_direction == 0:
                # Start going down if not at the bottom
                if not down_ok:
                    if self.trace:
                        print("maybeNewDirection(): returning None 1")
                    return None
                elif translate_y == -1:
                    # Mixel is already going down, don't interfere
                    if self.trace:
                        print("maybeNewDirection(): returning None 2")
                    return None
                else:
                    # Start going down
                    if self.trace:
                        print("maybeNewDirection(): going down")
                    return self.MixelChange(mixel.pos_x, mixel.pos_y-1, 0, -1)
            elif random_direction == 1:
                # Start going up if not at the top
                if not up_ok:
                    if self.trace:
                        print("maybeNewDirection(): returning None 3")
                    return None
                elif translate_y == 1:
                    # Mixel is already going up, don't interfere
                    if self.trace:
                        print("maybeNewDirection(): returning None 4")
                    return None
                else:
                    if self.trace:
                        print("maybeNewDirection(): going up")
                    return self.MixelChange(mixel.pos_x, mixel.pos_y+1, 0, 1)
            elif random_direction == 2:
                # Start going left if not at the left wall
                if not left_ok:
                    if self.trace:
                        print("maybeNewDirection(): returning None 5")
                    return None
                elif translate_x == -1:
                    # Mixel is already going left, don't interfere
                    if self.trace:
                        print("maybeNewDirection(): returning None 6")
                    return None
                else:
                    if self.trace:
                        print("maybeNewDirection(): going left")
                    return self.MixelChange(mixel.pos_x-1, mixel.pos_y, -1, 0)
            else:
                # Start going right if not at the right wall
                if not right_ok:
                    if self.trace:
                        print("maybeNewDirection(): returning None 7")
                    return None
                elif translate_x == 1:
                    # Mixel is already going right, don't interfere
                    if self.trace:
                        print("maybeNewDirection(): returning None 8")
                    return None
                else:
                    if self.trace:
                        print("maybeNewDirection(): going right")
                    return self.MixelChange(mixel.pos_x+1, mixel.pos_y, 1, 0)
        else:
            if self.trace:
                print("maybeNewDirection(): no direction change due to random number being too high")

    def handleBottomLeft(self, mixel):
        if mixel.translate_x == -1:
            ## Go up
            if self.trace:
                print("handleBottomLeft() called, going up")
            return self.MixelChange(0, 1, 0, 1)
        else:
            ## Go right
            if self.trace:
                print("handleBottomLeft() called, going right")
            return self.MixelChange(1, 0, 1, 0)

    def handleBottomRight(self, mixel):
        if mixel.translate_x == 1:
            # Go up
            if self.trace:
                print("handleBottomRight() called, going up")
            return self.MixelChange(15, 1, 0, 1)
        else:
            # Go left
            if self.trace:
                print("handleBottomRight() called, going left")
            return self.MixelChange(14, 0, -1, 0)

    def handleTopLeft(self, mixel):
        if mixel.translate_x == -1:
            # Go down
            if self.trace:
                print("handleTopLeft() called, going down")
            return self.MixelChange(0, 7, 0, -1)
        else:
            # Go right
            if self.trace:
                print("handleTopLeft() called, going right")
            return self.MixelChange(1, 8, 1, 0)

    def handleTopRight(self, mixel):
        if mixel.translate_x == 1:
            # Go down
            if self.trace:
                print("handleTopRight() called, going down")
            return self.MixelChange(15, 7, 0, -1)
        else:
            # Go left
            if self.trace:
                print("handleTopRight() called, going left")
            return self.MixelChange(14, 8, -1, 0)

    def handleLeftRightWall(self, mixel, next_x, next_y):
        is_left_wall = mixel.pos_x == 0
        is_right_wall = mixel.pos_x == 15

        if mixel.translate_x != 0:
            # We have hit the left or right wall from traveling in a horizontal direction. Adjust direction to go vertical.
            new_translate_y = self.getRandomTranslation()

            new_x = next_x
            if new_x > 15:
                new_x = 15
            elif new_x < 0:
                new_x = 0

            new_y = next_y + new_translate_y
            if new_y > 8:
                new_y = 8
            elif new_y < 0:
                new_y = 0    

            if self.debug:
                print("handleLeftRight() called, new y direction is %d" % new_translate_y)
            return self.MixelChange(new_x, new_y, 0, new_translate_y)
        else:
            # We are on the left or right wall from traveling in a vertical direction.
            # If on the left, you can go up, down or right. But you can't loop back on yourself.
            # If on the right, you can go up, down or left. But you can't loop back on yourself.
            left_ok = mixel.translate_x != 1 and not is_left_wall
            right_ok = mixel.translate_x != -1 and not is_right_wall
            up_ok = mixel.translate_y != -1
            down_ok = mixel.translate_y != 1
            if self.trace:
                print("handleLeftRightWall() calling maybeNewDirection(up_ok=%s, down_ok=%s, left_ok=%s, right_ok=%s, translate_x=%d, translate_y=%d)" \
                      % (up_ok, down_ok, left_ok, right_ok, mixel.translate_x, mixel.translate_y))
            return self.maybeNewDirection(up_ok=up_ok, down_ok=down_ok, left_ok=left_ok, right_ok=right_ok, \
                                          next_x=next_x, next_y=next_y, mixel=mixel)

    def handleBottomTopWall(self, mixel, next_x, next_y):
        is_bottom_wall = mixel.pos_y == 0
        is_top_wall = mixel.pos_y == 8

        if mixel.translate_y != 0:
            if (mixel.translate_y == 1 and next_y > 8) or (mixel.translate_y == -1 and next_y < 0):
                # We have hit the top wall or bottom wall from traveling in a vertical direction. Adjust direction to go horizontal.
                new_translate_x = self.getRandomTranslation()

                new_x = next_x + new_translate_x
                if new_x > 15:
                    new_x = 8
                elif new_x < 0:
                    new_x = 0

                new_y = next_y
                if new_y > 8:
                    new_y = 8
                elif new_y < 0:
                    new_y = 0

                if self.debug:
                    print("handleBottomTopWall() called, new x direction is %d" % new_translate_x)
                return self.MixelChange(new_x, new_y, new_translate_x, 0)
            else:
                # We are on the top or bottom wall but are already traveling in the opposite vertical direction. Don't take any action.
                return self.MixelChange(mixel.pos_x, mixel.pos_y + mixel.translate_y, mixel.translate_x, mixel.translate_y)
        else:
            # We are on the top or bottom wall from traveling in a horizonal direction.
            # If on the bottom, you can go up, left or right. But you can't loop back on yourself.
            # If on the top, you can go down, left or right. But you can't loop back on yourself.
            left_ok = mixel.translate_x != 1
            right_ok = mixel.translate_x != -1
            up_ok = mixel.translate_y != 1 and not is_top_wall
            down_ok = mixel.translate_y != -1 and not is_bottom_wall
            if self.trace:
                print("handleBottomTopWall() calling maybeNewDirection(up_ok=%s, down_ok=%s, left_ok=%s, right_ok=%s, translate_x=%d, translate_y=%d)" \
                      % (up_ok, down_ok, left_ok, right_ok, mixel.translate_x, mixel.translate_y))

            return self.maybeNewDirection(up_ok=up_ok, down_ok=down_ok, left_ok=left_ok, right_ok=right_ok, \
                                          next_x=next_x, next_y=next_y, mixel=mixel)

    def getRandomTranslation(self):
        random_direction = random.randint(0, 1) % 2
                
        if random_direction == 0:
            return -1
        else:
            return 1

    class MixelChange():
        def __init__(self, updated_x, updated_y, new_translate_x, new_translate_y):
            self.updated_x = updated_x
            self.updated_y = updated_y
            self.new_translate_x = new_translate_x
            self.new_translate_y = new_translate_y

        def to_string(self):
            return "MixelChange[updated_x=%d, updated_y=%d, new_translate_x=%d, new_translate_y=%d]" \
                % (self.updated_x, self.updated_y, self.new_translate_x, self.new_translate_y)
