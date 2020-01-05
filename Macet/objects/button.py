import pygame.image
import pygame.surface
import game_functions as GMfun

class button:

    def __init__(self, surface, coords, imageIdle, imageClicked, rect: list):
        self.idleState = pygame.image.load(imageIdle).convert_alpha()
        self.clickedState = pygame.image.load(imageClicked).convert_alpha()
        
        self.image = self.idleState
        self.rect = rect
        self.coords = coords

        self.surface = surface

    def update(self):
        if GMfun.mouseClickedArea(0, rect[0], rect[2], rect[1], rect[3]):
            self.image = self.clickedState
        else:
            self.image = self.clickedState

        self.surface.blit(self.image, self.coords)