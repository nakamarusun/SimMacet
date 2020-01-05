import pygame.image
import pygame.surface
import game_functions as GMfun

class Button:

    def __init__(self, surface, coords, imageIdle, imageClicked, rect: list):
        self.idleState = pygame.image.load(imageIdle).convert_alpha()
        self.clickedState = pygame.image.load(imageClicked).convert_alpha()
        
        self.image = self.idleState
        self.coords = coords
        self.rect = [ a + b for a, b in zip(rect, coords * 2)]

        self.surface = surface

    def update(self, xoffset=0, yoffset=0):
        if GMfun.mouseClickedArea(0, self.rect[0]+xoffset, self.rect[2]+xoffset, self.rect[1]+yoffset, self.rect[3]+yoffset):
            self.image = self.clickedState
        else:
            self.image = self.idleState

        self.surface.blit(self.image, self.coords)

    def checkState(self) -> bool:
        if self.image == self.idleState:
            return False
        return True