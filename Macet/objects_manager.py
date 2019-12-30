""" Manager for objects, controls scripts for every class """

import sound_manager as GMsnd
import game_functions as GMfun
import global_variables as GMvar

class Object:

    def __init__(self, coords=[0, 0], image=None, drawn=True, surface=GMvar.mainScreenBuffer):
        """ coords: [x, y] = object initial coordinates.
            image: pygame.Image = object's image, if exists.
            drawn: bool = whether object's image is drawn onto the surface or not. If image == none, then False
            surface: pygame.Surface = surface for image to be drawn onto """

        self.image = image  # Image if exists
        self.drawn = drawn if image != None else False             # Draw self every frame if true
        
        self.coords = coords

        # The following speeds have been altered according to their delta timings
        # WARNING: Speed is defined as pixels traveled per second.
        self.speed = [0, 0]

        self.width = self.image.get_rect()[2] if image != None else 0   # Image width
        self.height = self.image.get_rect()[3] if image != None else 0  # Image height
        
        self.direction = 0  # Object direction

        self.surface = surface  # Surface to be drawn on, default is GMvar.mainScreenBuffer

    def update(self):
        
        for i in range(len(self.speed)):
            if self.speed[i] != 0:
                self.coords[i] += self.speed[i] * GMvar.deltaTime     # Consistent movement with deltatiming

        # If drawn == true, then draw to designated surface
        if self.drawn:
            self.surface.blit(self.image, self.coords)

class Car(Object):

    def __init__(self, coords=[0,0], image=None, surface=GMvar.mainScreenBuffer):
        super().__init__(coords=coords, image=image, drawn=True, surface=surface)

    def update(self):
        self.speed = [64, 0]
        super().update()