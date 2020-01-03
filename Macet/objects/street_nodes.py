# The street nodes can be visualized as network nodes. one node can be connected to multiple nodes at the same time.
# Each node object has a list of nodes that the node connects to.
# Be noted that the connections are only one-way, Meaning that line draw events are much more efficient.

import pygame.math

class StreetNodes:

    def __init__(self, coords: list, connectedNodes: list):
        self.coords = coords
        for nodes in connectedNodes:
            self.connectedNodes[nodes] = pygame.math.Vector2([ nodes.coords[i] - self.coords[i] for i in range(2) ])

    # We would want to project the self node vector onto the chosen road node.