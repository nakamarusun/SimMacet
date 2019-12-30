import pygame.display
import pygame.image
import pygame
import time
import json

# Custom imports
import game_functions as GMfun
import room_manager as GMroom
import event_queue as GMque
import global_variables as GMvar
import objects_manager as GMobj

# Load settings.json and apply custom configs to game
with open("settings.json", "r", encoding="utf-8") as file:
    jsonFile = json.loads( file.read() )

    GMvar.resolution = jsonFile["resolution"]
    

# Inits
pygame.init()
pygame.display.set_caption("Sim Macet")
GMvar.mainScreenBuffer = pygame.display.set_mode(GMvar.resolution)  # Set resolution from settings.json

GMvar.curRoom = GMroom.Room()
GMvar.curRoom.addObjectToQueue( GMobj.Car([64, 64], pygame.image.load("images/sprites/CarExample.png"), GMvar.mainScreenBuffer) )

# Main Loop
while True:

    # Get time at the start of the frame
    startTime = time.time()

    # Reset background to black
    GMvar.mainScreenBuffer.fill( (0, 0, 0) )

    # Load all events to GMque.currentEvents list
    GMque.loadEvents()

    # Update each object in current room
    GMvar.curRoom.updateRoom()

    # FPS Calculator
    GMfun.displayFps(startTime)

    # Update display
    pygame.display.flip()

    # Delta Timing
    GMvar.deltaTime = GMfun.deltaTiming(startTime)