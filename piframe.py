# Each Json object in the data file makes up a PiFrame object. A PiFrame object will set up
# at least one hardware frame to display the static data. More hardware frames will be
# used (up to 8 total) to pre-draw transformations and animations.
import time
from time import sleep
from bufferthread import BufferThread

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

    def incrementCurrentFrameId(self):
        self.current_frame_id = self.current_frame_id + 1

        if self.current_frame_id > 7:
            self.current_frame_id = 0

    def incrementNextFrameId(self):
        self.next_frame_id = self.next_frame_id + 1

        if self.next_frame_id > 7:
            self.next_frame_id = 0

    def showBufferedFrame(self, frame_id):
        # self.display.sleep(True)
        # print("Displaying hardware frame %d" % frame_id)
        self.display.frame(frame_id, True)

        # Frame has been delivered to hardware, so indicate that a spot is now open
        # if self.buffered_frame_count > 0:
        #     self.buffered_frame_count = self.buffered_frame_count -1
        self.display.sleep(False)

    def runBufferThread(self, piframe):
        daemon = BufferThread(piframe)
        daemon.start()


    # This function is called only once (externally) for each PiFrame object.
    def runPiFrame(self):
        while self.current_iteration <= self.iterations or self.iterations == -1:
            self.showBufferedFrame(self.current_frame_id)
            self.incrementCurrentFrameId()

            # Display the frame for the specified number of milliseconds
            if (self.duration_ms < 0):
                # Sleep forever until being interrupted
                while(True):
                    sleep(1)
            else:
                # daemon = Thread(target=self.loadHwFrame, daemon=True, name='LoadHwFrame')
                # self.runBufferThread(self)
                begin = time.perf_counter()
                # print("Generating hardware frame %d" % self.current_frame_id)
                self.buildBufferedFrame(self.current_frame_id)
                end = time.perf_counter()
                elapsedMillis = 1000 * (end - begin)
                # print("Generated hardware frame %d in %.0f milliseconds" 
                #       % (self.current_frame_id, elapsedMillis))
                
                remainingMillis = self.duration_ms - elapsedMillis 
                if (remainingMillis > 0):
                    sleep(remainingMillis / 1000)
                # print("Sleep finished for runPiFrame()")

    # This function is called only once (externally) for each PiFrame object.
    def runNonBufferedPiFrame(self):
        while self.current_iteration <= self.iterations or self.iterations == -1:
            if len(self.animations) > 0:
                # First, fill the background if applicable
                if self.background is not None:
                    self.drawUsingFrameData(self.background)

                endPiFrame = False
                for animation in self.animations:
                    if endPiFrame:
                        animation.draw_frame(self.display, False)
                    else:
                        endPiFrame = animation.draw_frame(self.display, False)
                        
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

    
    # Builds the hardware frame from the supplied data and displays the hardware frame.
    # This function may be called multiple times.
    def buildBufferedFrame(self, frame_id):
        endPiFrame = False

        # Set the hardware frame to fill
        self.display.frame(frame_id, show=False)
        self.display.fill(0)

        if len(self.animations) > 0:
            # First, fill the background if applicable
            if self.background is not None:
                self.drawUsingFrameData(self.background)

            for animation in self.animations:
                if endPiFrame:
                    animation.draw_frame(self.display, True)
                else:
                    endPiFrame = animation.draw_frame(self.display, True)

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
     
        self.incrementNextFrameId()

    def drawUsingFrameData(self, frame_data):
        # Add the pixels to the hardware frame
        for i in range(0, self.height):
            for j in range(0, self.width):
                # print("%d, %d = %s" % (i, j, str(transformed_data[i][j])))
                brightness = frame_data[i][j]
                self.display.pixel(j, i, brightness)
            
