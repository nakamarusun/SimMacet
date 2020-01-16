# Script to store road data to Json file

import json

from objects.street_nodes import StreetNodes
from objects.stop_light import StopLight
from objects.car_spawner import CarSpawner
from rooms.main_room import Canvas
from game_math.displacement_functions import pixelsToKmh

from tkinter.filedialog import *

def saveFile() -> bool:

    jsonFile = {
        "StreetNodes": {},
        "StopLights": {},
        "CarSpawners": {}
    }

    for nodes in Canvas.roadNodes:
        jsonFile["StreetNodes"][nodes.id] = [
            nodes.coords,
            [ backNode.id for backNode in nodes.backNodes],
            [ connectedNodes.id for connectedNodes in list(connectedNodes.keys()) ]
        ]
    
    for lights in Canvas.stopLights:
        jsonFile["StopLights"][lights.id] = [
            lights.coords,
            lights.nodeAnchor.id,
            lights.greenDuration / 1000,
            lights.redDuration / 1000
        ]

    for spawners in Canvas.carSpawners:
        jsonFile["CarSpawners"][spawners.id] = [
            spawners.coords,
            spawners.nodeAnchor.id,
            spawners.originalSpeed,
            spawners.originalInterval
        ]

    with askopenfile(mode='w', defaultextension='.json') as file:
        file.write( json.dumps(jsonFile, indent=4) )
        file.close()