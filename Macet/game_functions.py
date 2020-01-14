"""Custom Game Functions"""

import pygame.surface

import time
import event_queue as GMque
import pygame.transform
import pygame
import pygame.draw
import global_variables as GMvar
import math
import numpy as np

#######################################################################################
# General game object functions

# Rotation anchor
def rotationAnchor(image, angle: float, anchor: list):
    # Anchor is the rotation point. (0, 0) is top left, while (1, 1) is bottom right.

    center = [ a*b for a,b in zip(image.get_size(), anchor) ]
    rotated_image = pygame.transform.rotate(image, angle).convert_alpha()
    new_rect = rotated_image.get_rect(center = center)

    return rotated_image, new_rect

def cosInterpolation(value: float, mutiplier: float) -> float:
    return (1 - ( 0.5 + ( math.cos( mutiplier*math.pi )/2 ) ) ) * value

def clamp(value: float, minValue: float, maxValue: float) -> float:
    if value > maxValue:
        return maxValue
    if value < minValue:
        return minValue
    return value

def drawArrow(surface, coords: list, length: float, angle: float, direction: float, color: list=(0,0,0), width=1):
    # Angle is the angle of the arrows. the direction is the angle from the x+ axis.

    arrowDirection = [ (direction + 180 - angle/2) * math.pi/180, (direction + 180 + angle/2) * math.pi/180 ]
    for i in range(2):
        lineCoords = [ length * math.cos(arrowDirection[i]), length * math.sin(arrowDirection[i]) ]
        pygame.draw.line(surface, color, coords, [ a + b for a, b in zip(lineCoords, coords) ], width)

def addList(lists: list):
    newList = [0] * len(lists)
    for i in range(len(lists)):
        for j in range(len(lists[0])):
            newList[i] += lists[i][j]

    return newList

# Timer for timing in game
class Timer:
    def __init__(self, endTime: float):
        # This is in miliseconds
        self.originalStart = time.time() * 1000
        self.originalEndTime = endTime
        self.endTime = time.time() * 1000 + endTime

    def checkDone(self) -> bool:
        if time.time() * 1000 > self.endTime:
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

def drawBetterLine(surface, color, x1: float, y1: float, x2:float, y2:float, width = 1):
    # DOESNT WORK
    vector = pygame.math.Vector2(x2 - x1, y2 - y1)
    length = round( vector.length() )
    lineSurf = pygame.Surface((round(length), width), pygame.SRCALPHA)
    lineSurf.fill( list(color) + [0] )
    pygame.draw.rect(lineSurf, color, (0, 0, round(length), width))
    angle = 360 - (np.arctan2(vector[1], vector[0]) * 180/math.pi)

    lineSurf = pygame.transform.rotate(lineSurf, angle)

    surface.blit(lineSurf, [ a + b if b < 0 else a for a, b in zip([x1, y1], vector) ] )


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