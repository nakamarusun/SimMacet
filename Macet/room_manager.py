""" Rooms are defined here and objects are placed here with their respective coordinates """

import game_functions as GMfun
import sound_manager as GMsnd
import global_variables as GMvar

import pygame.surface

class Room:
    def __init__(self):
        self.objectsList = []

    def addObjectToQueue(self, objectToAdd):
        self.objectsList.append(objectToAdd)

    def updateRoom(self):
        for objects in self.objectsList:
            objects.update()

import rooms.main_room as MainRoomObjects

MainRoom = Room()

MainRoomObjects.MainCameraSurface.objectsQueue.append( MainRoomObjects.Car([64, 64], pygame.image.load("images/sprites/CarExample.png").convert_alpha(), False, GMvar.mainScreenBuffer) )
MainRoomObjects.MainCameraSurface.objectsQueue.append( MainRoomObjects.Car([-100, -100], pygame.image.load("images/sprites/CarExample.png").convert_alpha(), False, GMvar.mainScreenBuffer) )
MainRoom.addObjectToQueue( MainRoomObjects.MainCameraSurface )
MainRoom.addObjectToQueue( MainRoomObjects.Canvas )

MainRoom.addObjectToQueue( MainRoomObjects.bottomGui )