
class Transform:
    def __init__(self, type, width, height, static_data):
        self.type = type
        self.width = width
        self.height = height
        self.static_data = static_data
        self.transformed_data = None
        self.reset()

    def getType(self):
        return self.type

    def do_transform(self):
        pass

    def reset(self):
        # Clone the static data
        self.transformed_data = []
        for row in self.static_data:
            new_row = []
            for j in range(0, len(row)):
                new_row.append(row[j])

            self.transformed_data.append(new_row)
            

# loop_static_data: if True, this will cause the supplied static data to loop around itself
#   when the end of the static data is reached. If False, the program will just provide rows
#   of 0 brightness to the area vacated by the transform.
class Translation(Transform):
    def __init__(self, width, height, translate_x, translate_y, static_data, loop_static_data):
        super().__init__("translation", width, height, static_data)
        self.translate_x = translate_x
        self.translate_y = translate_y
        self.loop_static_data = loop_static_data

    def do_transform(self):
        # Translate each row along the x axis
        for i in range(0, self.height):
            original = self.transformed_data[i]
            overflow = []

            if self.translate_x > 0:
                begin = len(self.transformed_data[i]) - self.translate_x
                end = begin + self.translate_x
                # Shift items to the right
                for k in range(begin, end):
                    # If we are looping, capture the items that are about to be knocked off the end.
                    # We will add them back to the beginning of the row.
                    if self.loop_static_data:
                        overflow.append(self.transformed_data[i][k])
                    else:
                        original.insert(0, 0)

                if self.loop_static_data:
                    self.transformed_data[i] = overflow + original[:self.width-1]
                else:
                    self.transformed_data[i] = original[:self.width]

            elif self.translate_x < 0:
                begin = 0
                end = -(self.translate_x)
                # Shift items to the left
                for k in range(begin, end):
                    # If we are looping, capture the items that are about to be knocked off the 
                    # beginning. We will add them back to the end of the row.
                    if self.loop_static_data:
                        overflow.append(self.transformed_data[i][k])
                    else:
                        original.append(0)
                        
                if self.loop_static_data:        
                    self.transformed_data[i] = original[1:self.width] + overflow
                else:
                    self.transformed_data[i] = original[1:]
    
        # Fill an empty row with 0's. This is used to insert empty rows
        empty = []
        for i in range(0, self.width):
            empty.append(0)

        # Translate the rows along the y axis
        if self.translate_y > 0:
            # Shift all the rows "down"
            overflow = []
            for i in range(self.height-self.translate_y, self.height):
                if self.loop_static_data:
                    overflow.append(self.transformed_data[i])
                else:
                    overflow.append(empty)

            self.transformed_data = overflow + self.transformed_data[0:self.height-self.translate_y]
                
        elif self.translate_y < 0:
            # Shift all the rows "up"
            overflow = []
            for i in range(0, (-self.translate_y)):
                if self.loop_static_data:
                    overflow.append(self.transformed_data[i])
                else:
                    overflow.append(empty)

            self.transformed_data = self.transformed_data[-self.translate_y:self.height] + overflow

        return self.transformed_data 