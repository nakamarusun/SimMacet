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

    GMvar.customMouse = jsonFile["customMouse"]
    GMvar.resolution = jsonFile["resolution"]
GMvar.mainScreenBuffer = pygame.display.set_mode(GMvar.resolution)  # Set resolution from settings.json

import game_functions as GMfun
import room_manager as GMroom
import event_queue as GMque
import objects_manager as GMobj

# Inits
pygame.init()
pygame.display.set_caption("Macet !")

GMvar.curRoom = GMroom.MainRoom

# Main Loop
while True:

    # Get time at the start of the frame
    startTime = time.time()

    # Clear screen buffer
    GMvar.mainScreenBuffer.fill( (255, 255, 255) )

    # Load all events to GMque.currentEvents list
    GMque.loadEvents()

    # Update and get mouse pos
    GMvar.latestMouse = pygame.mouse.get_pos()
    GMvar.mouseDelta = pygame.mouse.get_rel()
    GMvar.mouseState = pygame.mouse.get_pressed()
    GMvar.update()
    
    # Update each object in current room
    GMvar.curRoom.updateRoom()

    # Draw things that is top most
    GMfun.drawTopMost()

    # FPS Calculator
    FPS = GMfun.displayFps(startTime)

    # Copyright
    GMvar.mainScreenBuffer.blit(GMvar.credit, (GMvar.resolution[0] - 110, 2))

    # Update display
    pygame.display.flip()

    # Delta Timing
    GMvar.deltaTime = GMfun.deltaTiming(startTime)

    # print( (100 * GMfun.fpsCostTime / GMvar.deltaTime) ) # How many percentage of the FPS is it taking