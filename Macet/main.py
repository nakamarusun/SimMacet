import pygame.display
import pygame
import time
import json

# Custom imports
import game_functions as GMfun
import room_manager as GMroom
import event_queue as GMque
import global_variables as GMvar

# Load settings.json and apply custom configs to game
with open("settings.json", "r", encoding="utf-8") as file:
    jsonFile = json.loads( file.read() )

    GMvar.resolution = jsonFile["resolution"]
    

# Inits
pygame.init()
pygame.display.set_caption("Sim Macet")
GMvar.mainScreenBuffer = pygame.display.set_mode(GMvar.resolution)  # Set resolution from settings.json

# Main Loop
while True:

    # Get time at the start of the frame
    startTime = time.time()

    # Load all events to GMque.currentEvents list
    GMque.loadEvents()

    # FPS Calculator
    GMfun.displayFps(startTime)

    # Delta Timing
    GMvar.deltaTime = GMfun.deltaTiming()