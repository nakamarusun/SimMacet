import sys
sys.path.append('..')

import pygame.surface
import pygame.image
import pygame.math
import random

from objects_manager import Object
from objects.street_nodes import StreetNodes

class Car(Object):
    
    carSprites = [ i for i in range(1, 10) ]

    def __init__(self, node: StreetNodes, nodeDest: StreetNodes, speed: int, coords=[0,0], surface=None):
        # Speed is in pixels
        super().__init__(coords=coords, image=None, drawn=False, surface=surface)
        self.image = Car.carSprites[ random.randint(0, len(Car.carSprites) - 1 ) ]
        self.nodeAnchor = node
        self.nodeDestination = nodeDest
        self.curSpeed = speed

    def update(self):
        vector: pygame.math.Vector2 = self.nodeAnchor.connectedNodes[self.nodeDestination][0] # Define variables for vector from nodeAnchor to destination
        carVector: pygame.math.Vector2 = pygame.math.Vector2( [ b - a for a, b in zip(self.coords, self.nodeDestination.coords) ] ) # variable vector from nodeAnchor to car

        if carVector.length_squared() >= vector.length_squared(): # if length to car from nodeAnchor is more than length to destination,
            # set the destinationNode as node anchor, and pick one random nodeDestination from the list of the new nodeAnchor
            self.nodeAnchor = self.nodeDestination
            self.nodeDestination = self.nodeAnchor.connectedNodes[ random.randint(0, len(self.nodeAnchor.connectedNodes) - 1 ) ]
            change = True # Then change the original from nodeAnchor to destination vector.

        if change:
            vector: pygame.math.Vector2 = self.nodeAnchor.connectedNodes[self.nodeDestination][0]
        normalized = vector.normalize()

        self.speed = [ speed * vec for vec in normalized ]
        super().update()

        self.surface.blit(self.image, self.coords)