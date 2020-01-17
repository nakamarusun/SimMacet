# Script to read from .json file and load it into canvas

import json
import sys

from global_variables import mainScreenBuffer

from objects.street_nodes import StreetNodes
from objects.car_spawner import CarSpawner
from objects.stop_light import StopLight

from tkinter.filedialog import *
from tkinter import *

def openFile(Room) -> bool:

    root = Tk()
    root.withdraw()
    root.update()
    
    try:
        with askopenfile(mode="r", defaultextension=".json", initialdir=sys.path[0], filetypes=(("JSON save file", "*.json"), ("All Files", "*.*")) ) as file:
            
            jsonFile = json.loads( file.read() )
            root.destroy()

            del Room.roadNodes[:]
            del Room.stopLights[:]
            del Room.carSpawners[:]

            # Load from street nodes to room
            streetNodes = jsonFile["StreetNodes"]

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
            stopLights = jsonFile["StopLights"]

            for lights in stopLights:
                for nodes in Room.roadNodes:
                    if nodes.id == stopLights[lights][1]:
                        node = nodes
                        break
                
                Room.stopLights.append(
                    StopLight(node, mainScreenBuffer, stopLights[lights][0], stopLights[lights][2], stopLights[lights][3])
                )

            # And car spawners
            carSpawners = jsonFile["CarSpawners"]

            for spawners in carSpawners:
                for nodes in Room.roadNodes:
                    if nodes.id == carSpawners[spawners][1]:
                        node = nodes
                        break
                
                Room.carSpawners.append(
                    CarSpawner(node, carSpawners[spawners][0], carSpawners[spawners][2], carSpawners[spawners][3])
                )

            return True
    except AttributeError:
        return False