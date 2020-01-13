import sys
sys.path.append('..')

import pygame.surface
import pygame.image
import pygame.math
import random
import numpy as np
import math

import game_functions as GMfun

from objects_manager import Object
from objects.street_nodes import StreetNodes

class Car(Object):
    
    carSprites = [ pygame.image.load("images/sprites/Cars/8.png") ]

    def __init__(self, node: StreetNodes, nodeDest: StreetNodes, speed: int, coords=[0,0], surface=None):
        # Speed is in pixels
        super().__init__(coords=coords, image=None, drawn=False, surface=surface)
        self.originalImage = Car.carSprites[ random.randint(0, len(Car.carSprites) - 1 ) ]
        self.nodeAnchor: StreetNodes = node
        self.nodeDestination: StreetNodes = nodeDest
        self.curSpeed = speed
        self.direction = 360 - (np.arctan2(*self.nodeAnchor.connectedNodes[self.nodeDestination][0][::-1]) * 180/math.pi)
        self.image, rect = GMfun.rotationAnchor(self.originalImage, self.direction, [0, 0])

    def update(self, coordsOffset):
        vector: pygame.math.Vector2 = self.nodeAnchor.connectedNodes[self.nodeDestination][0] # Define variables for vector from nodeAnchor to destination
        carVector: pygame.math.Vector2 = pygame.math.Vector2( [ b - a for a, b in zip(self.coords, self.nodeDestination.coords) ] ) # variable vector from nodeAnchor to car

        change = False
        if carVector.length_squared() < 2: # if length to car from nodeAnchor is more than length to destination,
            # set the destinationNode as node anchor, and pick one random nodeDestination from the list of the new nodeAnchor
            self.nodeAnchor = self.nodeDestination
            numOfConnectedRoads = len(self.nodeAnchor.connectedNodes)
            # Issue delete object
            if numOfConnectedRoads == 0:
                del self
                return True

            nodeDestinationIndex = random.randint( 0 , numOfConnectedRoads - 1)
            self.nodeDestination = list(self.nodeAnchor.connectedNodes.keys())[ nodeDestinationIndex ]
            change = True # Then change the original from nodeAnchor to destination vector.

        if change:
            vector: pygame.math.Vector2 = self.nodeAnchor.connectedNodes[self.nodeDestination][0]
            self.direction = 360 - (np.arctan2(*vector[::-1]) * 180/math.pi) # Fix this
            self.image, rect = GMfun.rotationAnchor(self.originalImage, self.direction, [0, 0])
        normalized = vector.normalize()

        self.speed = [ self.curSpeed * vec for vec in normalized ]
        super().update()

        self.surface.blit(self.image, [ a - b for a, b in zip(self.coords, coordsOffset) ] )
        return False