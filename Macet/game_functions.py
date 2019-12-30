"""Custom Game Functions"""

import time
import event_queue as GMque

def displayFps(startTime: float):
    try:
        FPS = 1/(time.time() - startTime)
    except:
        FPS = "TOO HIGH"
    print(FPS)