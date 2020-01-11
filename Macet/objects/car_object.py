import sys
sys.path.append('..')

import pygame.surface
from objects_manager import Object

class Car(Object):
    
    def __init__(self, coords=[0,0]):
        super().__init__(coords=coords, image=None, drawn=False, surface=None)
        carImage = pygame.Surface()

    def update(self):
        super().update()