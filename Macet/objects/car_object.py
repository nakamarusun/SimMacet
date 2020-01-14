import sys
sys.path.append('..')

import pygame.surface
import pygame.image
import pygame.math
import random
import numpy as np
import math

import game_functions as GMfun

import global_variables as GMvar

from objects_manager import Object
from objects.street_nodes import StreetNodes

class Car(Object):
    
    carSprites = [ pygame.image.load("images/sprites/Cars/8.png") ]
    
    collisionGridSize = (160, 160)
    # carCollisionGrid: { [gridNumberx, gridNumbery]: [Cars list] }
    carCollisionGrid: dict = {}

    def __init__(self, node: StreetNodes, nodeDest: StreetNodes, speed: int, coords=[0,0], surface=None):
        # Speed is in pixels
        super().__init__(coords=coords, image=None, drawn=False, surface=surface)
        self.originalImage = Car.carSprites[ random.randint(0, len(Car.carSprites) - 1 ) ]

        self.nodeAnchor: StreetNodes = node
        self.nodeDestination: StreetNodes = nodeDest
        self.maxSpeed = speed
        self.acceleration = 16
        self.scalarSpeed = 0

        self.direction = 360 - (np.arctan2(*self.nodeAnchor.connectedNodes[self.nodeDestination][0][::-1]) * 180/math.pi)
        self.image, self.rect = GMfun.rotationAnchor(self.originalImage, self.direction, [0.28, 0.5])

        # Add the car to collision grid.
        self.gridPos = tuple( [ int(self.coords[i] // Car.collisionGridSize[i]) for i in range(2) ] )
        try:
            Car.carCollisionGrid[self.gridPos].append(self)
        except KeyError:
            Car.carCollisionGrid[self.gridPos] = [self]

    def update(self, coordsOffset):
        vector: pygame.math.Vector2 = self.nodeAnchor.connectedNodes[self.nodeDestination][0] # Define variables for vector from nodeAnchor to destination
        carVector: pygame.math.Vector2 = pygame.math.Vector2( [ b - a for a, b in zip(self.coords, self.nodeDestination.coords) ] ) # variable vector from nodeAnchor to car

        # Change the direction of the car if reached the end of the road
        change = False
        if carVector.length_squared() < 2: # if length to car from nodeAnchor is more than length to destination,
            # set the destinationNode as node anchor, and pick one random nodeDestination from the list of the new nodeAnchor
            self.nodeAnchor = self.nodeDestination
            numOfConnectedRoads = len(self.nodeAnchor.connectedNodes)
            # Change the coords
            self.coords = self.nodeAnchor.coords * 1

            # Issue object deletion
            if numOfConnectedRoads == 0:
                Car.carCollisionGrid[self.gridPos].pop(  Car.carCollisionGrid[self.gridPos].index( self )  )
                del self
                return True

            nodeDestinationIndex = random.randint( 0 , numOfConnectedRoads - 1)
            self.nodeDestination = list(self.nodeAnchor.connectedNodes.keys())[ nodeDestinationIndex ]
            change = True # Then change the original from nodeAnchor to destination vector.

        if change:
            vector: pygame.math.Vector2 = self.nodeAnchor.connectedNodes[self.nodeDestination][0]
            self.direction = 360 - (np.arctan2(*vector[::-1]) * 180/math.pi) # Fix this
            self.image, self.rect = GMfun.rotationAnchor(self.originalImage, self.direction, [0.28, 0.5])

        #################################################### GridPos repositioning ####################################################
        currentGridPos = tuple( [ int(self.coords[i] // Car.collisionGridSize[i]) for i in range(2) ] )
        if currentGridPos != self.gridPos:
            # Pop current car from the previous collisionGrid
            Car.carCollisionGrid[self.gridPos].pop(  Car.carCollisionGrid[self.gridPos].index( self )  )

            # Add current car to new grid, and assign new gridPos to self
            self.gridPos = currentGridPos
            try:
                Car.carCollisionGrid[self.gridPos].append(self)
            except KeyError:
                Car.carCollisionGrid[self.gridPos] = [self]
        
        #################################################### Collision checking ####################################################

        normalized = vector.normalize()
        self.scalarSpeed += GMvar.deltaTime * self.acceleration if self.scalarSpeed < self.maxSpeed else 0
        self.speed = [ self.scalarSpeed * vec for vec in normalized ]
        super().update()

        self.surface.blit(self.image, [ a - b + c for a, b, c in zip(self.coords, coordsOffset, self.rect) ] )
        return False