import sys
sys.path.append('..')

import pygame.image
import pygame.draw

from street_nodes import StreetNodes
from game_functions import Timer

class StopLight:

    # Colors of the StopLight. index 0 - 2 is red - green.
    onColor = ( (226, 58, 58), (242, 217, 48), (66, 207, 59) )
    offColor = ( (121, 19, 19), (135, 114, 15), (22, 105, 19) )

    def __init__(self, nodeAnchor: StreetNodes, surface, coords: list, greenDuration: int, redDuration: int):
        # Duration must be in second.
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

        if self.timer.checkDone():

            if self.state:
                self.timer = Timer(self.redDuration)
                self.state = False
            elif not self.state:
                self.timer = Timer(self.greenDuration)
                self.state = True

        # The range is weird is because it's the range between the lights
        for i in range(0, 35, 17):
            if not self.go and i/17 == 0:
                color = StopLight.onColor[i/17]
            elif self.go and i/17 == 2:
                color = StopLight.onColor[i/17]
            else:
                color = StopLight.offColor[i/17]

            if self.timer.currentTime + 1000 > self.timer.endTime:
                color = StopLight.offColor[i/17]
                if i/17 == 1:
                    color = StopLight.onColor[i/17]

            pygame.draw.circle(self.surface, color, (10, 12 + i), 13)

        self.surface.blit(self.image, [ a - b for a, b in zip(self.coords, coordsOffset) ] )