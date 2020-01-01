import pygame.surface
import pygame.image
import pygame.draw

import sys
sys.path.append('..')

import global_variables as GMvar
from objects_manager import Object

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

    slider = pygame.image.load("images/sprites/Slider.png")
    sliderRect = slider.get_rect()

    guiHeight = 75
    sliderHeight = sliderRect[3] + 30
    guiOpen = False
    guiHeightChange = GMvar.resolution[1] - sliderHeight

    initOpenSpeed = 50
    openSpeed = 50
    increment = 500

    surfGui = pygame.Surface((GMvar.resolution[0], guiHeight + sliderHeight))
    
    def update(): # pylint: disable=fixme, no-method-argument

        sliderX = GMvar.resolution[0]/2 - bottomGui.sliderRect[2]/2

        if GMvar.mouseStateSingle[0]:
            if GMvar.latestMouse[0] > (sliderX) and GMvar.latestMouse[0] < (sliderX + bottomGui.sliderRect[2]):
                if GMvar.latestMouse[1] > bottomGui.guiHeightChange and GMvar.latestMouse[1] < (bottomGui.guiHeightChange + bottomGui.sliderRect[3]):
                    bottomGui.guiOpen = not bottomGui.guiOpen
                    bottomGui.openSpeed = bottomGui.initOpenSpeed

        if bottomGui.guiOpen:
            if bottomGui.guiHeightChange > (GMvar.resolution[1] - bottomGui.guiHeight - bottomGui.sliderHeight):
                bottomGui.openSpeed += bottomGui.increment * GMvar.deltaTime
                bottomGui.guiHeightChange -= bottomGui.openSpeed * GMvar.deltaTime
        else:
            if bottomGui.guiHeightChange < (GMvar.resolution[1] - bottomGui.sliderHeight):
                bottomGui.openSpeed += bottomGui.increment * GMvar.deltaTime
                bottomGui.guiHeightChange += bottomGui.openSpeed * GMvar.deltaTime

        bottomGui.surfGui.blit(bottomGui.slider, (sliderX, 0))
        pygame.draw.rect(bottomGui.surfGui, (100, 100, 100), (0, bottomGui.sliderHeight, GMvar.resolution[0], bottomGui.guiHeight))
        GMvar.mainScreenBuffer.blit(bottomGui.surfGui, (0, bottomGui.guiHeightChange ))