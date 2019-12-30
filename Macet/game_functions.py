"""Custom Game Functions"""

import time
import event_queue as GMque


class Timer:
    def __init__(self, endTime: float):
        # This is in miliseconds
        self.endTime = endTime

    def checkDone(self) -> bool:
        if time.time() > self.endTime:
            return True
            del self
        else:
            return False

# Debugs
def displayFps(startTime: float):
    try:
        FPS = 1/(time.time() - startTime)
    except:
        FPS = "TOO HIGH"
    print(FPS)