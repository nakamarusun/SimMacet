"""Custom Game Functions"""

import time
import event_queue as GMque
import pygame.transform
import pygame
import global_variables as GMvar
import math

#######################################################################################
# General game object functions

# Rotation anchor
def rotationAnchor(image, angle: float, anchor: list):
    # Anchor is the rotation point. (0, 0) is top left, while (1, 1) is bottom right.

    center = [ a*b for a,b in zip(image.get_size(), anchor) ]
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = center)

    return rotated_image, new_rect

def cosInterpolation(value: float, mutiplier: float) -> float:
    return (1 - ( 0.5 + ( math.cos( mutiplier*math.pi )/2 ) ) ) * value

# Timer for timing in game
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
# If mouse is clicked once in an area
def mouseClickedArea(mouseButton: int, left: float, right: float, top: float, bottom: float):
    if GMvar.mouseStateSingle[mouseButton]:
        if GMvar.latestMouse[0] > left and GMvar.latestMouse[0] < right:
            if GMvar.latestMouse[1] > top and GMvar.latestMouse[1] < bottom:
                return True
    return False
# If mouse is held in an area
def mouseHoldArea(mouseButton: int, left: float, right: float, top: float, bottom: float):
    if GMvar.mouseState[mouseButton]:
        if GMvar.latestMouse[0] > left and GMvar.latestMouse[0] < right:
            if GMvar.latestMouse[1] > top and GMvar.latestMouse[1] < bottom:
                return True
    return False

def insertDrawTopMostQueue(image, coords):
    GMvar.drawTopMost.append( (image, coords) )

def drawTopMost():
    for image, coords in GMvar.drawTopMost:
        GMvar.mainScreenBuffer.blit(image, coords)

########################################################################################
# Specialized functions

# Delta timing
def deltaTiming(startTime: float) -> float:
    """ Returns time took to finish a frame """
    return time.time() - startTime

# Debugs
def displayFps(startTime: float):
    try:
        FPS = " " + str(round(1/(time.time() - startTime)))
    except:
        FPS = ">1000"
    GMvar.mainScreenBuffer.blit(GMvar.defFont.render(("FPS:" + FPS), True, (0, 0, 0) ), (5, 5))
    return int(FPS[1:])

fpsCostTime = 0
def fpsCost():
    global fpsCostTime
    fpsCostTime = time.time()

def endFpsCost():
    global fpsCostTime
    fpsCostTime = time.time() - fpsCostTime