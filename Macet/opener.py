# Script to read from .json file and load it into canvas

import json
import sys

from global_variables import mainScreenBuffer

from objects.street_nodes import StreetNodes
from objects.car_spawner import CarSpawner
from objects.stop_light import StopLight
from rooms.main_room import Canvas as Room

from tkinter.filedialog import *

def openFile() -> bool:

    with askopenfile(mode="r", defaultextension=".json", initialdir=sys.path[0]) as file:
        
        jsonFile = json.loads(file.read())

        # Load from street nodes to room
        with jsonFile["StreetNodes"] as streetNodes:

            newNodesList = []
            for nodes in streetNodes:
                newNodesList.append( StreetNodes(
                    streetNodes[nodes][0],
                    {},
                    [],
                    0,
                    id=nodes
                ) )

            for nodes in newNodesList:

                for backNodesId in streetNodes[nodes.id][1]:
                    for checkNodes in newNodesList:
                        if checkNodes.id == backNodesId:
                            nodes.backNodes.append(checkNodes)

                for frontNodesId in streetNodes[nodes.id][2]:
                    for checkNodes in newNodesList:
                        if checkNodes.id == frontNodesId:
                            nodes.connectTo(checkNodes)

            Room.roadNodes += newNodesList
            del newNodesList

        # Now stop lights
        with jsonFile["StopLights"] as stopLights:

            for lights in stopLights:
                for nodes in Room.roadNodes:
                    if nodes.id == stopLights[lights][1]:
                        node = nodes
                        break
                
                Room.stopLights.append(
                    StopLight(node, mainScreenBuffer, stopLights[lights][0], stopLights[lights][2], stopLights[lights][3])
                )

        # And car spawners
        with jsonFile["CarSpawners"] as carSpawners:

            for spawners in carSpawners:
                for nodes in Room.roadNodes:
                    if nodes.id == carSpawners[spawners][1]:
                        node = nodes
                        break
                
                Room.stopLights.append(
                    CarSpawner(node, carSpawners[spawners][0], carSpawners[spawners][2], carSpawners[spawners][3])
                )

        return True