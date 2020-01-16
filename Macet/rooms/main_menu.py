import global_variables as GMvar

import pygame.surface
import pygame.image

class MovieShower:
    pass

class Text:

    logoSize =  pygame.image.load("images/Logo.png").convert_alpha().get_rect()[2:]
    reScaled = (sum(GMvar.resolution) / 2) / (sum(logoSize) / 2) * 2/5
    logo = pygame.transform.scale( pygame.image.load("images/Logo.png").convert_alpha(), (int(logoSize[0] * reScaled), int(logoSize[1] * reScaled)) ).convert_alpha()

    logoSurface = pygame.Surface(logo.get_rect()[2:])

    fadeUi = pygame.image.load("images/Faded.png").convert_alpha()

    fadeSurface = pygame.Surface(fadeUi.get_rect()[2:])

    def update():

        logoSurface = pygame.Surface(Text.logo.get_rect()[2:]).convert()
        fadeSurface = pygame.Surface(Text.fadeUi.get_rect()[2:])

        logoSurface.set_alpha(50)
        fadeSurface.set_alpha(50)

        logoSurface.blit(Text.logo, (0, 0) )
        fadeSurface.blit(Text.fadeUi, (0, 0) )

        GMvar.mainScreenBuffer.blit(logoSurface, ( GMvar.resolution[0]/2 - Text.logo.get_rect()[2]/2, GMvar.resolution[1] * 0.25 - Text.logo.get_rect()[3]/2))
        GMvar.mainScreenBuffer.blit(fadeSurface, ( GMvar.resolution[0]/2 - Text.fadeUi.get_rect()[2]/2, GMvar.resolution[1] * 0.75 - Text.fadeUi.get_rect()[3]/2 ))