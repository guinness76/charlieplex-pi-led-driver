
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