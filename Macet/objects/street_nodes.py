# The street nodes can be visualized as network nodes. one node can be connected to multiple nodes at the same time.
# Each node object has a list of nodes that the node connects to.
# Be noted that the connections are only one-way, Meaning that line draw events are much more efficient.

class StreetNodes:

    def __init__(self, coords: list, connectedNodes: list):
        self.coords = coords
        self.connectedNodes = connectedNodes