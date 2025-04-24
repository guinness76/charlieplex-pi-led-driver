from threading import Thread

class BufferThread(Thread):
    def __init__(self, pi_frame):
        super().__init__()
        self.setDaemon(True)
        self.setName("BufferThread")
        self.pi_frame = pi_frame

    def run(self):
        # print("Starting BufferThread...")
        next_frame_id = self.pi_frame.next_frame_id
        self.pi_frame.buildBufferedFrame(next_frame_id)
        # print("Finished BufferThread")