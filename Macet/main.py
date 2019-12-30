import pygame.display
import pygame
import time

# Custom imports
import game_functions as GMfun
import room_manager as GMroom
import event_queue as GMque
import global_variables as GMvar

# Inits
pygame.init()
pygame.display.set_caption("Sim Macet")
pygame.display.set_mode((800, 600))

# Main Loop
while True:

    # Get time at the start of the frame
    startTime = time.time()

    # Load all events to GMque.currentEvents list
    GMque.loadEvents()

    # FPS Calculator
    GMfun.displayFps(startTime)