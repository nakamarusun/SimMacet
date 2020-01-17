# Script to store road data to Json file

import json
import sys

from objects.street_nodes import StreetNodes
from objects.stop_light import StopLight
from objects.car_spawner import CarSpawner

from tkinter.filedialog import *
from tkinter import *

def saveFile(Room) -> bool:

    jsonFile = {
        "StreetNodes": {},
        "StopLights": {},
        "CarSpawners": {}
    }

    for nodes in Room.roadNodes:
        jsonFile["StreetNodes"][nodes.id] = [
            nodes.coords,
            [ backNode.id for backNode in nodes.backNodes],
            [ connectedNodes.id for connectedNodes in list(nodes.connectedNodes.keys()) ]
        ]
    
    for lights in Room.stopLights:
        jsonFile["StopLights"][lights.id] = [
            lights.coords,
            lights.nodeAnchor.id,
            lights.greenDuration / 1000,
            lights.redDuration / 1000
        ]

    for spawners in Room.carSpawners:
        jsonFile["CarSpawners"][spawners.id] = [
            spawners.coords,
            spawners.nodeAnchor.id,
            spawners.originalSpeed,
            spawners.originalInterval
        ]

    root = Tk()
    root.withdraw()
    root.update()

    try:
        with asksaveasfile(mode='w', defaultextension='.json', initialdir=sys.path[0], filetypes=(("JSON save file", "*.json"), ("All Files", "*.*")) ) as file:
            file.write( json.dumps(jsonFile, indent=4) )
            file.close()
            root.destroy()

        return True
    except AttributeError:
        return False