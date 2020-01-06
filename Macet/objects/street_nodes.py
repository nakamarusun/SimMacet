# The street nodes can be visualized as network nodes. one node can be connected to multiple nodes at the same time.
# Each node object has a list of nodes that the node connects to.
# Be noted that the connections are only one-way, Meaning that line draw events are much more efficient.

import pygame.math

class StreetNodes:

    def __init__(self, coords: list, connectedNodes: list, backNodes: list, nodeType: int):
        self.coords = coords
        self.backNodes = backNodes
        self.connectedNodes = {}
        for nodes in connectedNodes:
            # self.connectedNodes: {nodeObject: vector}
            self.connectedNodes[nodes] = pygame.math.Vector2([ nodes.coords[i] - self.coords[i] for i in range(2) ]) # This is the vector from self to all connected notes
        self.nodeType = nodeType

    # We would want to project the self node vector onto the chosen road node.