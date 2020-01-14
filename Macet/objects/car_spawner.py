import sys
sys.path.append('..')

import pygame.draw

import random
import math

from shapely.geometry import Point, LineString

from global_variables import mainScreenBuffer
from objects.car_object import Car
from game_math.displacement_functions import kmhToPixels
from objects.street_nodes import StreetNodes
from game_functions import Timer

class CarSpawner:

    def __init__(self, nodeAnchor: StreetNodes, coords: list, spawnerSpeed: float, spawnerInterval: float, intervalDeviation: float=0):
        # Spawned car's speed is in km/h, spawnerInterval is how often it spawns new car. (car/minute)
        self.coords: list = coords
        self.nodeAnchor: StreetNodes = nodeAnchor
        self.speed: float = kmhToPixels(spawnerSpeed)
        # This is interval for spawning car. defined as second/car
        perSecondInterval = (60 / spawnerInterval)

        # initialize timer. Timer is randomized if there is an interval deviation. ranges from:
        # [second/car - second/car * deviation, second/car + second/car * deviation]
        self.interval: list = [ perSecondInterval + intervalDeviation * perSecondInterval * i for i in range(-1, 2, 2) ]
        self.pause: bool = False

        self.nextNodeList: list = []

        # Search for the absolute end of the road (curEndNode)
        longestLength = 0
        curEndNode: StreetNodes = None
        for connected in self.nodeAnchor.connectedNodes:
            curLength = self.nodeAnchor.connectedNodes[connected][0].length_squared()
            if curLength > longestLength:
                curEndNode = connected
                longestLength = curLength

        # Define start point and end point
        lineToCheck = LineString( [ [*self.coords], [*curEndNode.coords] ] )
        
        for connected in self.nodeAnchor.connectedNodes:
            if Point(connected.coords).intersects(lineToCheck):
                self.nextNodeList.append(connected)
        
        self.timer: Timer = Timer( random.randint( *[ math.ceil(time * 1000) for time in self.interval ] ) )

    def update(self, carList: list, surface, offset: list):
        if self.timer.checkDone():
            # Do actions here:
            # Spawn cars here
            if not self.pause:
                carList.append( Car(self.nodeAnchor, self.nextNodeList[ random.randint(0, len(self.nextNodeList) - 1 ) ], self.speed * 1, self.coords * 1, mainScreenBuffer) )
            # Reset timer
            self.timer = Timer( random.randint( *[ math.ceil(time * 1000) for time in self.interval ] ) )
        pygame.draw.rect(surface, (20, 170, 20), (*[ a - b + 6 for a, b in zip(self.coords, offset) ], 4, 4))