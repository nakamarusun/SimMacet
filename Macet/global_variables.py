""" Variables """

import pygame.display
import event_queue as GMque
import pygame

resolution = [800, 600] # Default resolution is 800 x 600
mainScreenBuffer = None
curRoom = None
deltaTime: float = 0
latestMouse = [0, 0]
mouseState = [False, False, False]  # left, middle, right respective to their index
mouseStateSingle = [False, False, False]    # Same as mouseState but, only for one frame
latestMouseLeft = [0, 0]
__mouseHandled = False

def update():
    global mouseState
    global __mouseHandled
    global mouseStateSingle
    global latestMouseLeft
    mouseState = [False, False, False]
    mouseStateSingle = [False, False, False]

    for event in GMque.currentEvents:
        if event.type == pygame.MOUSEBUTTONUP:
            __mouseHandled = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseState[event.button - 1] = True
            if not __mouseHandled:
                mouseStateSingle[event.button - 1] = True
            __mouseHandled = True

    if mouseStateSingle[0]:
        latestMouseLeft = latestMouse * 1