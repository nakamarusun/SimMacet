""" Manager for objects, controls scripts for every class """

import sound_manager as GMsnd
import game_functions as GMfun
import global_variables as GMvar

class Object:

    def __init__(self, coords=(0, 0), image=None, drawn=True, surface=GMvar.mainScreenBuffer):
        """ coords: (x, y) = object initial coordinates.
            image: pygame.Image = object's image, if exists.
            drawn: bool = whether object's image is drawn onto the surface or not. If image == none, then False
            surface: pygame.Surface = surface for image to be drawn onto """

        self.image = image  # Image if exists
        self.drawn = drawn if image != None else False             # Draw self every frame if true
        
        self.x = coords[0]  # X coords
        self.y = coords[1]  # Y coords

        self.width = self.image.get_rect()[2] if image != None else 0   # Image width
        self.height = self.image.get_rect()[3] if image != None else 0  # Image height
        
        self.direction = 0  # Object direction

        self.surface = surface  # Surface to be drawn on, default is mainScreenBuffer

    def update(self):
        
        # If drawn == true, then draw to designated surface
        if self.drawn:
            self.surface.blit(self.image, (self.x, self.y))