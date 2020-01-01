import pygame.surface
import pygame.image
import pygame.draw
import pygame.transform

import sys
sys.path.append('..')

import global_variables as GMvar
from objects_manager import Object
import game_functions as GMfun

class Car(Object):

    def __init__(self, coords=[0,0], image=None, surface=GMvar.mainScreenBuffer):
        super().__init__(coords=coords, image=image, drawn=True, surface=surface)

    def update(self):
        self.speed = [0, 0]
        super().update()

class RoadCreator(Object):

    def __init__(self):
        pass

        # Init all roads
    
    def update(self):
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

    surfGui = pygame.Surface((GMvar.resolution[0], guiHeight + sliderHeight)) # an isolated Surface in which to draw the GUI
    
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
                bottomGui.sliderDirection += 360 * GMvar.deltaTime
        else:
            if bottomGui.guiHeightChange < (GMvar.resolution[1] - bottomGui.sliderHeight):
                bottomGui.openSpeed -= bottomGui.increment * GMvar.deltaTime
                bottomGui.guiHeightChange += bottomGui.openSpeed * GMvar.deltaTime
            else:
                # Reset everything
                bottomGui.openSpeed = 50
                bottomGui.guiHeightChange = GMvar.resolution[1] - bottomGui.sliderHeight
            if bottomGui.sliderDirection > 0:
                bottomGui.sliderDirection -= 360 * GMvar.deltaTime

        # Clear surface
        bottomGui.surfGui.set_alpha(0)
        bottomGui.surfGui.fill((0, 0, 0))
        bottomGui.surfGui.set_alpha(255)

        slider, rect = GMfun.rotationAnchor(bottomGui.slider, bottomGui.sliderDirection, (0.5, 0.5)) # Get rotation

        # Draw and blit to main screen buffer
        bottomGui.surfGui.blit( slider, [ a + b for a, b in zip((rect.x, rect.y), (bottomGui.sliderX, bottomGui.sliderYOffset))  ] )
        pygame.draw.rect(bottomGui.surfGui, (100, 100, 100), (0, bottomGui.sliderHeight, GMvar.resolution[0], bottomGui.guiHeight))
        GMvar.mainScreenBuffer.blit(bottomGui.surfGui, (0, bottomGui.guiHeightChange ))