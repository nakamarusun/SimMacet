import pygame.surface
import pygame.image
import pygame.draw

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

    slider = pygame.image.load("./images/sprites/Slider.png")
    sliderRect = slider.get_rect()

    guiHeight = 75
    sliderHeight = sliderRect[3] + 30
    guiOpen = False
    guiHeightChange = GMvar.resolution - sliderHeight

    surfGui = pygame.Surface((GMvar.resolution[0], bottomGui.guiHeight + bottomGui.sliderHeight))

    def update():

        if bottomGui.guiOpen:
            if bottomGui.guiHeightChange > (GMvar.resolution[1] - bottomGui.guiHeight - bottomGui.sliderHeight):
                bottomGui.guiHeightChange -= 50 * GMvar.deltaTime
        else:
            if bottomGui.guiHeightChange < (GMvar.resolution[1] - bottomGui.sliderHeight):
                bottomGui.guiHeightChange += 50 * GMvar.deltaTime

        bottomGui.surfGui.blit(bottomGui.slider, (GMvar.resolution[0]/2 - bottomGui.sliderRect[2]/2, 0))
        pygame.draw.rect(bottomGui.surfGui, (100, 100, 100), (0, bottomGui.sliderHeight, GMvar.resolution[0], bottomGui.guiHeight))
        GMvar.mainScreenBuffer.blit(bottomGui.surfGui, (0, bottomGui.guiHeightChange ))