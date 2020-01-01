import pygame.display
import pygame.image
import pygame.mouse
import pygame
import time
import json

# Custom imports
# Load settings.json and apply custom configs to game
import global_variables as GMvar

with open("settings.json", "r", encoding="utf-8") as file:
    jsonFile = json.loads( file.read() )

    GMvar.resolution = jsonFile["resolution"]
GMvar.mainScreenBuffer = pygame.display.set_mode(GMvar.resolution)  # Set resolution from settings.json

import game_functions as GMfun
import room_manager as GMroom
import event_queue as GMque
import objects_manager as GMobj
import rooms.main_room

# Inits
pygame.init()
pygame.display.set_caption("Sim Macet")

GMvar.curRoom = GMroom.MainRoom
GMvar.curRoom.addObjectToQueue( rooms.main_room.Car([64, 64], pygame.image.load("images/sprites/CarExample.png"), GMvar.mainScreenBuffer) )

# Main Loop
while True:

    # Get time at the start of the frame
    startTime = time.time()

    # Reset background to black
    GMvar.mainScreenBuffer.fill( (0, 0, 0) )

    # Load all events to GMque.currentEvents list
    GMque.loadEvents()

    # Update and get mouse pos
    GMvar.update()
    GMvar.latestMouse = pygame.mouse.get_pos()

    # Update each object in current room
    GMvar.curRoom.updateRoom()

    # FPS Calculator
    # GMfun.displayFps(startTime)

    # Update display
    pygame.display.flip()

    # Delta Timing
    GMvar.deltaTime = GMfun.deltaTiming(startTime)