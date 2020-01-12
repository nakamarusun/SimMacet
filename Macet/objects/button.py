import pygame.image
import pygame.surface
import game_functions as GMfun
import global_variables as GMvar

class Button:

    def __init__(self, surface, coords, imageIdle, imageClicked, rect: list):
        self.idleState = pygame.image.load(imageIdle).convert_alpha() # Button image when not clicked
        self.clickedState = pygame.image.load(imageClicked).convert_alpha() # Button image when mouse is over the image and is clicked
        
        # Image is the current image of the button
        self.image = self.idleState
        self.coords = coords # Image coordinates
        self.rect = [ a + b for a, b in zip(rect[:2], coords)] + list(rect[2:]) # Rect is (x, y, width, height)

        self.surface = surface

    def update(self, xoffset=0, yoffset=0):
        if GMfun.mouseHoldArea(0, self.rect[0]+xoffset, self.rect[2]+xoffset+self.rect[0], self.rect[1]+yoffset, self.rect[3]+yoffset+self.rect[1]):
            if id(self.image) != id(self.clickedState):
                self.image = self.clickedState
        else:
            if id(self.image) != id(self.idleState):
                self.image = self.idleState
        
        self.surface.blit(self.image, self.coords)

    def checkState(self) -> bool:
        # This is magic
        if self.image == self.clickedState and GMvar.mouseState[0] == False:
            return True
        return False

class ToggleButton(Button):

    def __init__(self, surface, coords, imageIdle, imageClicked, rect):
        super().__init__(surface, coords, imageIdle, imageClicked, rect)
        self.clicked = False
        self.newlyClicked = False
        self.conflictButtons = []

    def update(self, xoffset=0, yoffset=0):
        self.newlyClicked = False
        if GMfun.mouseClickedArea(0, self.rect[0]+xoffset, self.rect[2]+xoffset+self.rect[0], self.rect[1]+yoffset, self.rect[3]+yoffset+self.rect[1]):
            self.clicked = not self.clicked
            if self.clicked:
                self.newlyClicked = True

        if self.clicked:
            if id(self.image) != id(self.clickedState):
                self.image = self.clickedState
        else:
            if id(self.image) != id(self.idleState):
                self.image = self.idleState

        if self.newlyClicked:
            for buttons in self.conflictButtons:
                buttons.clicked = False

        self.surface.blit(self.image, self.coords)

    def checkState(self) -> bool:
        return self.clicked

    def checkNewlyClicked(self) -> bool:
        return self.newlyClicked

    def addConflictButtons(self, buttons: list):
        self.conflictButtons += buttons
