
class Mixel():
    def __init__(self, id, pos_x, pos_y, translate_x, translate_y, brightness):
        self.id = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.translate_x = translate_x
        self.translate_y = translate_y
        self.brightness = brightness
        self.upcoming_dir_changes = []
        self.next_dir_change_id = 0

    def add_dir_change(self, x, y, translate_x, translate_y):
        dir_change = UpcomingDirChange(self.next_dir_change_id, x, y, translate_x, translate_y)
        self.upcoming_dir_changes.append(dir_change)
        self.next_dir_change_id = self.next_dir_change_id + 1
        return dir_change

    def pop_dir_change(self):
        old_id = -1
        if len(self.upcoming_dir_changes) > 0:
            dir_change = self.upcoming_dir_changes.pop(0)
            old_id = dir_change.id

        return old_id
    
    def set_pos_x(self, new_x):
        self.pos_x = new_x

    def set_pos_y(self, new_y):
        self.pos_y = new_y

# A mixel needs to change direction (aka update its translation values) when it hits
# these coordinates.
class UpcomingDirChange():
    def __init__(self, id, x, y, translate_x, translate_y):
        self.id = id
        self.x = x
        self.y = y
        self.translate_x = translate_x
        self.translate_y = translate_y

    def to_string(self):
        return "'id=%d, x=%d, y=%d, translate_x=%d, translate_y=%d'" \
            % (self.id, self.x, self.y, self.translate_x, self.translate_y)
    

# Draws a one-pixel-wide line on the display. The line can be horizontal, vertical, or diagonal.
# https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
def draw_line(display, start_x, start_y, end_x, end_y, brightness):
    if abs(end_y - start_y) < abs(end_x - start_x):
        if start_x > end_x:
            draw_line_low(display, end_x, end_y, start_x, start_y, brightness)
        else:
            draw_line_low(display, start_x, start_y, end_x, end_y, brightness)
    else:
        if start_y > end_y:
            draw_line_high(display, end_x, end_y, start_x, start_y, brightness)
        else:
            draw_line_high(display, start_x, start_y, end_x, end_y, brightness)


# Handles line slopes that are between 0 and 1
def draw_line_low(display, start_x, start_y, end_x, end_y, brightness):
    dx = end_x - start_x
    dy = end_y - start_y

    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy

    # Multiply by 2 to keep everything as integers
    D = (2 * dy) - dx
    y = start_y    

    for x in range(start_x, end_x + 1):
        display.pixel(x, y, brightness)
        if D > 0:
            y = y + yi
            D = D + (2 * (dy - dx))
        else:
            D = D + (2 * dy)    

# Handles line slopes that are greater than 1
def draw_line_high(display, start_x, start_y, end_x, end_y, brightness):
    dx = end_x - start_x
    dy = end_y - start_y

    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx

    # Multiply by 2 to keep everything as integers
    D = (2 * dx) - dy
    x = start_x    

    for y in range(start_y, end_y + 1):
        display.pixel(x, y, brightness)
        if D > 0:
            x = x + xi
            D = D + (2 * (dx - dy))
        else:
            D = D + (2 * dx)  


# Fills in a rectangular area on the display
def fill_area(display, start_x, start_y, end_x, end_y, brightness):
    for i in range(start_x, end_x+1):
        for j in range(start_y, end_y+1):
            display.pixel(i, j, brightness)