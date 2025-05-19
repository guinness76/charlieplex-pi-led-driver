from time import sleep

class PiFrame:
    width = 16
    height = 9

    def __init__(self, display):
        self.display = display
        self.background = None
        self.duration_ms = -1
        self.iterations = 1
        self.current_iteration = 0 # The number of times the transform has been run
        self.first_iteration = 0 
        self.current_frame_id = 0
        self.next_frame_id = 0
        self.transform = None
        self.animations = []

    def reset(self):
        self.current_iteration = self.first_iteration
        self.current_frame_id = 0
        self.next_frame_id = 0

        for animation in self.animations:
            animation.reset()

    def set_first_iteration(self, first_iteration):
        self.first_iteration = first_iteration
        self.current_iteration = first_iteration

    # This function is called only once for each PiFrame object.
    def runNonBufferedPiFrame(self):
        while self.current_iteration <= self.iterations or self.iterations == -1:
            if len(self.animations) > 0:
                # First, fill the background if applicable
                if self.background is not None:
                    self.drawUsingFrameData(self.background)

                endPiFrame = False
                for animation in self.animations:
                    if endPiFrame:
                        animation.draw_frame(self.display)
                    else:
                        endPiFrame = animation.draw_frame(self.display)
                        
                    if (endPiFrame):
                        # This should break the loop after the next frame is displayed
                        self.current_iteration = 2
                        self.iterations = 1
            elif self.transform is not None:                
                transformed_data = self.transform.do_transform()
                self.drawUsingFrameData(transformed_data)
                self.current_iteration = self.current_iteration + 1
            else:
                # Display the static background
                self.drawUsingFrameData(self.background)
                self.current_iteration = self.current_iteration + 1

            sleep(self.duration_ms / 1000)

    def drawUsingFrameData(self, frame_data):
        # Add the pixels to the hardware frame
        for i in range(0, self.height):
            for j in range(0, self.width):
                # print("%d, %d = %s" % (i, j, str(transformed_data[i][j])))
                brightness = frame_data[i][j]
                self.display.pixel(j, i, brightness)
            
