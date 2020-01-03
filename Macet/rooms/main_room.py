import pygame.surface
import pygame.image
import pygame.draw
import pygame.transform

import sys
sys.path.append('..')

import global_variables as GMvar
from objects_manager import Object
from objects.street_nodes import StreetNodes
import game_functions as GMfun

class MainCameraSurface:
    # This is the surface in which every object that needs to be movable

    objectsQueue = []   # Objects to be loaded in the camera

    mainSurface = pygame.Surface(GMvar.resolution, pygame.SRCALPHA)     # Main surface of the camera, need to have transparency enabled
    cameraCoords = [0, 0]   # Current coordinates of the camera

    cellSize = (32, 32) # Grid cell size for the game

    # for gridSize can't use list comprehension, will throw an error because of class
    gridSize = [0, 0] # Cell total for width and height
    gridSize[0] = GMvar.resolution[0] // cellSize[0] + 1
    gridSize[1] = GMvar.resolution[1] // cellSize[1] + 2

    def getRealMouseCoords() -> list:
        return [ a + b for a, b in zip(MainCameraSurface.cameraCoords, GMvar.latestMouse) ]

    def update():

        # If mouse is clicked and dragged
        if GMvar.mouseState[0]:
            MainCameraSurface.cameraCoords = [ a - b for a, b in zip(MainCameraSurface.cameraCoords, GMvar.mouseDelta) ]  # Substract cameracoords by delta mouse movements

        # Draw grid by considering camera movements. Size is constant and the grid is drawn directly on the main buffer.
        gridOffset = [ (MainCameraSurface.cameraCoords[i] % MainCameraSurface.cellSize[i]) for i in range(len(MainCameraSurface.cellSize)) ]    # Grid offset based on the camera coordinates
        newCoords = [0, 0]  # Coordinates for individual grids
        for i in range(MainCameraSurface.gridSize[0]):
            newCoords[0] = i * MainCameraSurface.cellSize[0] - gridOffset[0] # Change x coordinates
            for j in range(MainCameraSurface.gridSize[1]):
                newCoords[1] = j * MainCameraSurface.cellSize[1] - gridOffset[1] # Change y coordinates
                pygame.draw.rect( GMvar.mainScreenBuffer, (235, 235, 235), (newCoords, MainCameraSurface.cellSize), 1 ) # Draw square

        # Clear surface
        MainCameraSurface.mainSurface.fill((0, 0, 0, 0))

        # For every object in the camera queue, do their respective update event, and put them in their new coordinates
        for objects in MainCameraSurface.objectsQueue:
            objects.update()
            newSurfCoords = [ a - b for a, b in zip(objects.coords, MainCameraSurface.cameraCoords) ] # Calculate new object coordinates based on camera coords
            MainCameraSurface.mainSurface.blit(objects.image, newSurfCoords) # Blit objects to camera surface

        GMvar.mainScreenBuffer.blit(MainCameraSurface.mainSurface, (0, 0) ) # Blit to main buffer

class Car(Object):

    def __init__(self, coords=[0,0], image=None, drawn=True, surface=GMvar.mainScreenBuffer):
        super().__init__(coords=coords, image=image, drawn=drawn, surface=surface)
        MainCameraSurface.objectsQueue.append(self)

    def update(self):
        self.speed = [10, 0]
        super().update()

class RoadCreator:
    

    def update():
        pass

class bottomGui:

    # image for the slider
    slider = pygame.image.load("images/sprites/Slider.png")
    sliderDirection = 0 # Slider's image direction
    sliderRect = slider.get_rect() # Slider rect

    guiHeight = 75 # The height of the rectangle part of the gui
    sliderHeight = sliderRect[3] + 50 # The height of the slider's image plus some breathing room
    guiOpen = False # State whether gui is open or nah
    guiHeightChange = GMvar.resolution[1] - sliderHeight # Current gui's position on the screen.
    sliderX = GMvar.resolution[0]/2 - sliderRect[2]/2 # Middle point of the slider
    sliderYOffset = 15 # Offset of slider button from the top of the surface

    openSpeed = 50 # Initial speed to open the GUI
    increment = 500 # Speed acceleration

    surfGui = pygame.Surface((GMvar.resolution[0], guiHeight + sliderHeight),pygame.SRCALPHA) # an isolated Surface in which to draw the GUI
    surfGui = surfGui.convert_alpha()
    
    def update(): # pylint: disable=fixme, no-method-argument

        # If mouse is clicked on the button then open/close gui
        if GMvar.mouseStateSingle[0]:
            if GMvar.latestMouse[0] > (bottomGui.sliderX) and GMvar.latestMouse[0] < (bottomGui.sliderX + bottomGui.sliderRect[2]):
                if GMvar.latestMouse[1] > (bottomGui.guiHeightChange + bottomGui.sliderYOffset) and GMvar.latestMouse[1] < (bottomGui.guiHeightChange + bottomGui.sliderRect[3] + bottomGui.sliderYOffset):
                    bottomGui.guiOpen = not bottomGui.guiOpen

        # If open and not in position, set the coordinates
        if bottomGui.guiOpen:
            if bottomGui.guiHeightChange > (GMvar.resolution[1] - bottomGui.guiHeight - bottomGui.sliderHeight):
                bottomGui.openSpeed += bottomGui.increment * GMvar.deltaTime
                bottomGui.guiHeightChange -= bottomGui.openSpeed * GMvar.deltaTime
            if bottomGui.sliderDirection < 180:
                bottomGui.sliderDirection += 450 * GMvar.deltaTime
            else:
                bottomGui.sliderDirection = 180
        else:
            if bottomGui.guiHeightChange < (GMvar.resolution[1] - bottomGui.sliderHeight):
                bottomGui.openSpeed -= bottomGui.increment * GMvar.deltaTime
                bottomGui.guiHeightChange += bottomGui.openSpeed * GMvar.deltaTime
            else:
                # Reset everything so the numbers are not weird
                bottomGui.openSpeed = 50
                bottomGui.guiHeightChange = GMvar.resolution[1] - bottomGui.sliderHeight
            if bottomGui.sliderDirection > 0:
                bottomGui.sliderDirection -= 450 * GMvar.deltaTime
            else:
                bottomGui.sliderDirection = 0

        bottomGui.sliderDirection = round(bottomGui.sliderDirection)

        # Clear surface
        bottomGui.surfGui.fill((0, 0, 0, 0))

        slider, rect = GMfun.rotationAnchor(bottomGui.slider, bottomGui.sliderDirection, (0.5, 0.5)) # Get rotation

        # Draw and blit to main screen buffer
        bottomGui.surfGui.blit( slider, [ a + b for a, b in zip((rect.x, rect.y), (bottomGui.sliderX, bottomGui.sliderYOffset)) ] )     # Blit slider button to surface
        pygame.draw.rect(bottomGui.surfGui, (100, 100, 100), (0, bottomGui.sliderHeight, GMvar.resolution[0], bottomGui.guiHeight + 1)) # Plus 1 to fix the weird 1 pixel
        GMvar.mainScreenBuffer.blit(bottomGui.surfGui, (0, bottomGui.guiHeightChange + 1 )) # Finally, draw everything to main buffer