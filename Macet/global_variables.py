""" Variables """

import pygame.display
import pygame.font
import event_queue as GMque
import pygame
import datetime

# Inits
pygame.font.init()

customMouse = False
resolution = [800, 600] # Default resolution is 800 x 600
mainScreenBuffer = None
curRoom = None
defFont = pygame.font.Font(pygame.font.get_default_font(), 14)
defFont12 = pygame.font.Font(pygame.font.get_default_font(), 12)

credit = pygame.font.Font(pygame.font.get_default_font(), 10).render("© {} Nakamarusun.".format(str(datetime.date.today().year)), True, (0, 0, 0))

drawTopMost = []

deltaTime: float = 0

latestMouse = [0, 0]
mouseState = [False, False, False]  # left, middle, right respective to their index
mouseStateSingle = [False, False, False]    # Same as mouseState but, only for one frame
latestMouseLeft = [0, 0]
mouseDelta = [0, 0]

keyboardPressedStates = []

__mouseHandled = False

def update():
    global mouseState
    global __mouseHandled
    global mouseStateSingle
    global latestMouseLeft
    global keyboardPressedStates
    global drawTopMost

    del drawTopMost [:]

    mouseStateSingle = [False, False, False]    # Same as mouseState but, only for one frame    

    mouseState = [ True if state == 1 else False for state in mouseState]
    for event in GMque.currentEvents:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if __mouseHandled != True:
                mouseStateSingle = [ True if state == 1 else False for state in mouseState]
            __mouseHandled = True
        else:
            __mouseHandled = False

    if mouseStateSingle[0]:
        latestMouseLeft = latestMouse * 1

    del keyboardPressedStates[:]
    for event in GMque.currentEvents:
        if event.type == pygame.KEYDOWN:
            keyboardPressedStates.append(event.key)