# Author : Adrien Pillou
# Date : 02/11/2020
import time

# Alarm class
# Similar to GameMaker alarm block
class alarm():

    # Alarm constructor (delay in s)
    def __init__(self, delay, on_awake=True):
        self.delay = delay
        self.start_time = time.time()
        self.ended = False
        self.remaining_time = delay

    # Check if the alarm ended
    def is_ended(self):
        if self.start_time is None:
            return False
        elif self.start_time + self.delay <= time.time():
            self.ended = True
            return True

    # Return the remaining time (ms)
    def get_remaining_time(self):
        if self.ended:
            return 0
        else:
            return (self.start_time + self.delay) - time.time()

    # End callback
    def end(self):
        self.ended = True
        self.delay = 0
        self.remaining_time = 0

    # Start the alarm
    def start(self):
        self.start_time = time.time()

    # Reset the alarm
    def reset(self, delay):
        self.delay = delay
        self.start_time = time.time()
        self.ended = False
