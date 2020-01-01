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

