# The street nodes can be visualized as network nodes. one node can be connected to multiple nodes at the same time.
# Each node object has a list of nodes that the node connects to.
# Be noted that the connections are only one-way, Meaning that line draw events are much more efficient.

import sys
sys.path.append('..')

import pygame.math
import pygame.surface
import pygame.transform
import game_functions as GMfun
import numpy as np
import math

class StreetNodes:

    def __init__(self, coords: list, connectedNodes: list, backNodes: list, nodeType: int, width=16):
        self.coords = coords
        self.backNodes = backNodes
        self.connectedNodes = {}
        for nodes in connectedNodes:
            self.connectTo(nodes, width=width)
        self.nodeType = nodeType

        self.doneChange = True

    # Change the width of thhe image
    def connectTo(self, newNode, width=16, color=(50,50,50)):
        vector = pygame.math.Vector2([ newNode.coords[i] - self.coords[i] for i in range(2) ])
        length = vector.length()
        image = pygame.Surface( (int(round(length)), width), pygame.SRCALPHA )
        image.fill((0))
        image.fill((50, 50, 50))
        angle = 360 - (np.arctan2( *vector[::-1] ) * 180/math.pi)
        image = pygame.transform.rotate(image, angle)
        self.connectedNodes[newNode] = [ vector, angle, length, image, width, color ] # This is the vector from self to all connected newNode.

    def disconnectFrom(newNode):
        pass

    def changeWidth(self, node, width):
        self.connectedNodes[node][3] = pygame.surface(self.connectedNodes[node][2], width)

    def changeColorWidth(self, node, color=(50, 50, 50), width=16):
        image = pygame.Surface( (int(round(self.connectedNodes[node][2])), width), pygame.SRCALPHA )
        image.fill((0))
        image.fill(color)
        angle = self.connectedNodes[node][1]
        image = pygame.transform.rotate(image, angle)
        self.connectedNodes[node][3] = image
        self.connectedNodes[node][4] = width
        self.connectedNodes[node][5] = color

    def drawSelf(self, surface, coords=[0, 0], width=16, color=(50, 50, 50)):
        for node in self.connectedNodes:
            if self.connectedNodes[node][4] != width or self.connectedNodes[node][5] != color:
                self.changeColorWidth(node, color, width)
        for connectedNodes in list(self.connectedNodes.values()):
            addition = ( -math.cos(connectedNodes[1] * math.pi/180) * 16 , math.sin(connectedNodes[1] * math.pi/180) * 16 )
            surface.blit(connectedNodes[3], [ a + b + c + d if b < 0 else a + c for a, b, c, d in zip(self.coords, connectedNodes[0], coords, addition) ] ) # 16nya dikaliin berdasarkan direction sin whatever lah..

    # We would want to project the self node vector onto the chosen road node.