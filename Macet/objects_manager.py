""" Manager for objects, controls scripts for every class """

import math

import global_variables as GMvar

class Object:

    def __init__(self, coords=[0, 0], image=None, drawn=False, surface=GMvar.mainScreenBuffer):
        """ coords: [x, y] = object initial coordinates.
        image: pygame.Image = object's image, if exists.
        drawn: bool = whether object's image is drawn onto the surface or not. If image == none, then False
        surface: pygame.Surface = surface for image to be drawn onto """

        self.originalImage = image
        self.image = image  # Image if exists
        self.drawn = drawn if image != None else False             # Draw self every frame if true
        
        self.coords = coords

        # The following speeds have been altered according to their delta timings
        # WARNING: Speed is defined as pixels traveled per second. ##############
        self.speed = [0, 0]
        self.dirSpeed = 0   # If not 0, dirSpeed is translated to speed based on the direction

        width = self.image.get_rect()[2] if image != None else 0   # Image width
        height = self.image.get_rect()[3] if image != None else 0  # Image height

        self.size = [width, height]
        
        self.direction = 0  # Object direction

        self.surface = surface  # Surface to be drawn on, default is GMvar.mainScreenBuffer

    def update(self):
        
        # Sin is multiplied by -1 so that it will go up
        if self.dirSpeed != 0:
            radian = self.direction * math.pi/180
            self.speed[0] = math.cos( radian ) * self.dirSpeed
            self.speed[1] = -math.sin( radian ) * self.dirSpeed

        for i in range(len(self.speed)):
            if self.speed[i] != 0:
                self.coords[i] += self.speed[i] * GMvar.deltaTime     # Consistent movement with deltatiming

        # If drawn == true, then draw to designated surface
        if self.drawn:
            self.surface.blit(self.image, self.coords)