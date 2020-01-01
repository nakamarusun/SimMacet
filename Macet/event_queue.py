""" Event collector for inputs e.g. Keyboard, Mouse """

import pygame.event

# Current input events in a single frame
currentEvents = []

def loadEvents():
    for events in pygame.event.get():

        del currentEvents[:]
        if events.type == pygame.QUIT: quit()   # Quit game if event is called
        currentEvents.append(events)