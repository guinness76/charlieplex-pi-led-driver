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
        self.debug = True
        self.trace = True
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
         

    def draw_frame(self, display, hardware_buffering):
        head = len(self.pos)-1

        # Remember that we are starting from opposite side of the origin coordinates and working our
        # way backwards. Thus, the origin coordinates actually specify the tail.
        for i in range(head, -1, -1):
            mixel = self.pos[i]

            # Undraw the tail
            if (i == 0):
                display.pixel(mixel.pos_x, mixel.pos_y, 0)

            # Update the coordinates to reflect the next position
            next_x = mixel.pos_x + mixel.translate_x
            next_y = mixel.pos_y + mixel.translate_y

            dir_changes = mixel.upcoming_dir_changes
            for upcoming_dir_change in dir_changes:
                if upcoming_dir_change.x == next_x and upcoming_dir_change.y == next_y:
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

                    if i == 0:
                        # We are on the tail. The oldest dir change should have been applied to all mixels at this point,
                        # so clear the dir change.
                        for j in range(head, -1, -1):
                            old_id = self.pos[j].pop_dir_change()
                            if self.debug:
                                print("On the tail. Cleared upcoming dir change %d from mixel[%s]." % (old_id, self.pos[j].id))

            updated_translation = None
            if i == head:
                # See if the head needs to change direction on the next iteration
                updated_translation = self.handleHead(mixel, next_x, next_y, display.width, display.height)

                if updated_translation is not None:
                    # Adjust the direction of the head mixel
                    mixel.translate_x = updated_translation.new_translate_x
                    mixel.translate_y = updated_translation.new_translate_y

                    # When the head is about to hit a wall or a corner, all the mixels need to be informed so that 
                    # they can turn at the edge of the wall/corner. We do this by adding a dir_change to the mixel.
                    # All the mixels will adjust their direction when their next coordinates matches the 
                    # coordinates of one of the dir_changes.
                    for j in range(head, -1, -1):
                        next_mixel = self.pos[j]
                        next_dir_change = next_mixel.add_dir_change(next_x, next_y, \
                            updated_translation.new_translate_x, updated_translation.new_translate_y)   

                        if self.debug:
                            print("""Upcoming dir change %s applied to mixel[%s]. Dir change should happen on coordinates (%d, %d)""" \
                                % (next_dir_change.to_string(), next_mixel.id, next_x, next_y))

            mixel.set_pos_x(next_x)
            mixel.set_pos_y(next_y)                                                                 

            # Draw the current pixel
            if mixel.pos_x < 0 or mixel.pos_x > 15 or mixel.pos_y < 0 or mixel.pos_y > 9:
                print("Some kind of problem here. mixel.id=%s, mixel.pos_x=%d, mixel.pos_y=%d, next_x=%d, next_y=%d" \
                      % (mixel.id, mixel.pos_x, mixel.pos_y, next_x, next_y))
                deadbeef = 0

            if self.trace:
                print("Drawing mixel[%s] at (%d,%d)" % (mixel.id, mixel.pos_x, mixel.pos_y))
            
            brightness = mixel.brightness
            if (i == head):
                brightness = 150
            display.pixel(mixel.pos_x, mixel.pos_y, brightness)
        return False

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
            return self.handleLeftRightWall(mixel)
        elif mixel.pos_y == 0 or mixel.pos_y == top_wall:
            return self.handleBottomTopWall(mixel)
        else:
            # For a potential direction change, we can't let the snake loop back on itself in the opposite direction
            left_ok = mixel.translate_x != 1
            right_ok = mixel.translate_x != -1
            up_ok = mixel.translate_y != -1
            down_ok = mixel.translate_y != 1
            if self.trace:
                print("handleHead calling maybeNewDirection()")
            return self.maybeNewDirection(up_ok=up_ok, down_ok=down_ok, left_ok=left_ok, right_ok=right_ok, translate_x=mixel.translate_x, translate_y=mixel.translate_y)
        
    def maybeNewDirection(self, up_ok, down_ok, left_ok, right_ok, translate_x, translate_y):
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
                        print("maybeNewDirection(): returning (0,-1)")
                    return self.TranslationChange(0, -1)
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
                        print("maybeNewDirection(): returning (0, 1)")
                    return self.TranslationChange(0, 1)
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
                        print("maybeNewDirection(): returning (-1,0)")
                    return self.TranslationChange(-1, 0)
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
                        print("maybeNewDirection(): returning (1,0)")
                    return self.TranslationChange(1, 0)
        else:
            if self.trace:
                print("maybeNewDirection(): no direction change due to random number being too high")

    def handleBottomLeft(self, mixel):
        if mixel.translate_x == -1:
            ## Go up
            if self.trace:
                print("handleBottomLeft() called, going up")
            return self.TranslationChange(0, 1)
        else:
            ## Go right
            if self.trace:
                print("handleBottomLeft() called, going right")
            return self.TranslationChange(1, 0)

    def handleBottomRight(self, mixel):
        if mixel.translate_x == 1:
            # Go up
            if self.trace:
                print("handleBottomRight() called, going down")
            return self.TranslationChange(0, 1)
        else:
            # Go left
            if self.trace:
                print("handleBottomRight() called, going left")
            return self.TranslationChange(-1, 0)

    def handleTopLeft(self, mixel):
        if mixel.translate_x == -1:
            # Go up
            if self.trace:
                print("handleTopLeft() called, going up")
            return self.TranslationChange(0, -1)
        else:
            # Go right
            if self.trace:
                print("handleTopLeft() called, going right")
            return self.TranslationChange(1, 0)

    def handleTopRight(self, mixel):
        if mixel.translate_x == 1:
            # Go down
            if self.trace:
                print("handleTopRight() called, going down")
            return self.TranslationChange(0, -1)
        else:
            # Go left
            if self.trace:
                print("handleTopRight() called, going left")
            return self.TranslationChange(-1, 0)

    def handleLeftRightWall(self, mixel):
        if mixel.translate_x != 0:
            # We are about to hit the left or right wall. Adjust direction to go vertical.
            new_y = self.getRandomTranslation()

            if self.debug:
                print("handleLeftRight() called, new y direction is %d" % new_y)
            return self.TranslationChange(0, new_y)
        else:
            # If on the left, you can go up, down or right. But you can't loop back on yourself.
            # If on the right, you can go up, down or left. But you can't loop back on yourself.
            left_ok = mixel.translate_x != 1
            right_ok = mixel.translate_x != -1
            up_ok = mixel.translate_y != -1
            down_ok = mixel.translate_y != 1
            if self.trace:
                print("handleLeftRightWall() calling maybeNewDirection(up_ok=%s, down_ok=%s, left_ok=%s, right_ok=%s, translate_x=%d, translate_y=%d)" \
                      % (up_ok, down_ok, left_ok, right_ok, mixel.translate_x, mixel.translate_y))
            return self.maybeNewDirection(up_ok=up_ok, down_ok=down_ok, left_ok=left_ok, right_ok=right_ok, \
                                          translate_x=mixel.translate_x, translate_y=mixel.translate_y)

    def handleBottomTopWall(self, mixel):
        if mixel.translate_y != 0:
            # We are about to hit the top or bottom wall. Adjust direction to go horizontal
            new_x = self.getRandomTranslation()
            if self.debug:
                print("handleBottomTopWall() called, new x direction is %d" % new_x)
            return self.TranslationChange(new_x, 0)
        else:
            # If on the bottom, you can go up, left or right. But you can't loop back on yourself.
            # If on the top, you can go down, left or right. But you can't loop back on yourself.
            left_ok = mixel.translate_x != 1
            right_ok = mixel.translate_x != -1
            up_ok = mixel.translate_y != 1
            down_ok = mixel.translate_y != -1
            if self.trace:
                print("handleBottomTopWall() calling maybeNewDirection(up_ok=%s, down_ok=%s, left_ok=%s, right_ok=%s, translate_x=%d, translate_y=%d)" \
                      % (up_ok, down_ok, left_ok, right_ok, mixel.translate_x, mixel.translate_y))

            return self.maybeNewDirection(up_ok=up_ok, down_ok=down_ok, left_ok=left_ok, right_ok=right_ok, \
                                          translate_x=mixel.translate_x, translate_y=mixel.translate_y)

    def getRandomTranslation(self):
        random_direction = random.randint(0, 1) % 2
                
        if random_direction == 0:
            return -1
        else:
            return 1

    class TranslationChange():
        def __init__(self, new_translate_x, new_translate_y):
            self.new_translate_x = new_translate_x
            self.new_translate_y = new_translate_y
