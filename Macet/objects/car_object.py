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

from game_math.custom_math_funcs import isPointInTriangle, triangleArea

class Car(Object):
    
    carSprites = [ pygame.image.load("images/sprites/Cars/8.png") ]
    
    collisionGridSize = (160, 160)
    # carCollisionGrid: { [gridNumberx, gridNumbery]: [Cars list] }
    carCollisionGrid: dict = {}

    # Collision cone definition
    fov = 75     # Direction
    triangleHeight = 50  # Pixels, This is also the start-brake distance Original = 87
    stopDistance = 32 # Must be more than 27, as that is the length of the car.
    triangleBase = math.tan( fov / 2 * math.pi/180 ) * triangleHeight * 2


    def __init__(self, node: StreetNodes, nodeDest: StreetNodes, speed: int, coords=[0,0], surface=None):
        # Speed is in pixels
        super().__init__(coords=coords, image=None, drawn=False, surface=surface)
        self.originalImage = Car.carSprites[ random.randint(0, len(Car.carSprites) - 1 ) ]

        self.nodeAnchor: StreetNodes = node
        self.nodeDestination: StreetNodes = nodeDest
        self.maxSpeed = speed
        self.acceleration = 16
        self.scalarSpeed = 0
        self.beforeBrakeSpeed = 0

        self.carInFront = False

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

        try:
            normalized = vector.normalize()        
        except ValueError:
            normalized = [0, 0]

        # Change the direction of the car if reached the end of the road
        change = False
        if normalized != carVector.normalize(): # if length to car from nodeAnchor is more than length to destination,
            # set the destinationNode as node anchor, and pick one random nodeDestination from the list of the new nodeAnchor
            self.nodeAnchor = self.nodeDestination
            numOfConnectedRoads = len(self.nodeAnchor.connectedNodes)

            # Issue object deletion
            if numOfConnectedRoads == 0:
                Car.carCollisionGrid[self.gridPos].pop(  Car.carCollisionGrid[self.gridPos].index( self )  )
                del self
                return True

            nodeDestinationIndex = random.randint( 0 , numOfConnectedRoads - 1)
            self.nodeDestination = list(self.nodeAnchor.connectedNodes.keys())[ nodeDestinationIndex ]
            # Change the coords
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
        self.carInFront = False # Collision stuff. True if a car is detected in front.
        collisionCheckList = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    collisionCheckList += Car.carCollisionGrid[ tuple( [ self.gridPos[0] + i, self.gridPos[1] + j ] ) ]
                except KeyError:
                    pass
        
        distanceFromNearestCar = 10000000000
        for cars in collisionCheckList:
            # Ignore if the car object is self, or if the nodeAnchor of self is not the same as other nodeAnchor 
            if cars == self:
                continue
            viewConeBase = [ (Car.triangleHeight * normalized[i]) + self.coords[i] + 8 for i in range(2) ]

            offsetVector1 = [ -normalized[1], normalized[0] ]
            viewConeBase1 = [ a + (Car.triangleBase / 2 * c) for a, c in zip(viewConeBase, offsetVector1) ]
            offsetVector2 = [ -vec for vec in offsetVector1 ]
            viewConeBase2 = [ a + (Car.triangleBase / 2 * c) for a, c in zip(viewConeBase, offsetVector2) ]

            carCoords = cars.coords
            # If the coords is within the cone
            if isPointInTriangle(carCoords, self.coords, viewConeBase1, viewConeBase2):
                distanceVector = pygame.math.Vector2( *[ b - a for a, b in  zip(self.coords, carCoords) ] )
                if distanceVector.length_squared() < distanceFromNearestCar:
                    distanceFromNearestCar = distanceVector.length()
                self.carInFront = not cars.go if type(cars).__name__ == "StopLight" and cars.nodeAnchor == self.nodeAnchor else True

            
        ################################################## END COLLISION CHECKING ##################################################

        accelAddition = GMvar.deltaTime * self.acceleration * GMvar.gameSpeed
        if distanceFromNearestCar < Car.triangleHeight and self.carInFront:
            self.scalarSpeed -= self.beforeBrakeSpeed * ( 1 - ( GMfun.clamp(distanceFromNearestCar + Car.stopDistance, 0, Car.triangleHeight) / Car.triangleHeight)) if self.scalarSpeed * 1 >= 0 else 0
        else:
            self.beforeBrakeSpeed = self.scalarSpeed * 1
            self.scalarSpeed += accelAddition if self.scalarSpeed * 1 <= self.maxSpeed else 0
        self.speed = [ self.scalarSpeed * vec * GMvar.gameSpeed for vec in normalized ]
        super().update()

        if change:
            self.coords = self.nodeAnchor.coords * 1

        self.surface.blit(self.image, [ a - b + c for a, b, c in zip(self.coords, coordsOffset, self.rect) ] )
        return False