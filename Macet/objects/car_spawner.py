import sys
sys.path.append('..')

import random
import math

from objects.car_object import Car
from game_math.displacement_functions import kmhToPixels
from objects.street_nodes import StreetNodes
from game_functions import Timer

class CarSpawner:

    def __init__(self, nodeAnchor: StreetNodes, coords: list, spawnerSpeed: float, spawnerInterval: float, intervalDeviation: float):
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
        
        self.timer: Timer = Timer( random.randint( *[ math.ceil(time * 1000) for time in self.interval ] ) )

    def update(self):
        if self.timer.checkDone():
            # Do actions here:
            # Spawn cars here
            
            # Reset timer
            self.timer = Timer( random.randint( *[ math.ceil(time * 1000) for time in self.interval ] ) )