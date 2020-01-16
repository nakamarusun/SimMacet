import sys
sys.path.append('..')

import pygame.image
import pygame.draw

from objects.street_nodes import StreetNodes
from game_functions import Timer

import global_variables as GMvar
import game_functions as GMfun

class StopLight:

    # Colors of the StopLight. index 0 - 2 is red - green.
    onColor = ( (226, 58, 58), (242, 217, 48), (66, 207, 59) )
    offColor = ( (121, 19, 19), (135, 114, 15), (22, 105, 19) )

    def __init__(self, nodeAnchor: StreetNodes, surface, coords: list, greenDuration: int, redDuration: int):
        # Duration must be in second.
        self.id = GMfun.generateRandomString(8, True, True, True)
        self.image = pygame.image.load("images/sprites/StopLight.png").convert_alpha()
        self.coords: list = coords
        self.nodeAnchor: StreetNodes = nodeAnchor
        self.surface = surface

        self.greenDuration = greenDuration * 1000
        self.redDuration = redDuration * 1000

        # If true, the light is green.
        self.go = True

        self.timer: Timer = Timer(greenDuration * 1000)

    def update(self, coordsOffset):

        # Adjust timer so it would fit gameSpeed
        self.timer.endTime = self.timer.originalStart + (self.timer.originalEndTime * 1 / GMvar.gameSpeed)
        if self.timer.checkDone():

            if self.go:
                self.timer = Timer(self.redDuration)
                self.go = False
            elif not self.go:
                self.timer = Timer(self.greenDuration)
                self.go = True

        # The range is weird is because it's the range between the lights
        for i in range(0, 35, 17):
            if not self.go and i/17 == 0:
                color = StopLight.onColor[i//17]
            elif self.go and i/17 == 2:
                color = StopLight.onColor[i//17]
            else:
                color = StopLight.offColor[i//17]

            if self.timer.currentTime + (1000 * 1/GMvar.gameSpeed) > self.timer.endTime:
                color = StopLight.offColor[i//17]
                if i//17 == 1:
                    color = StopLight.onColor[i//17]

            pygame.draw.circle(self.image, color, [ 10, 12 + i ], 13//2)
        
        self.surface.blit(self.image, [ a - b - 12 for a, b in zip(self.coords, coordsOffset) ] )