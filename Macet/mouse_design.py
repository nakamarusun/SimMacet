import pygame.mouse
import pygame.cursors

currentMouse = "Default"

mouseRoad = ((32, 32), (
    "..                              ",
    "...                             ",
    "....                            ",
    "..X..                           ",
    "..XX..                          ",
    "..XXX..                         ",
    "..XXXX..                        ",
    "..XXXXX..                       ",
    "..XXXXXX..XXXXXXX..XXXXXXX..    ",
    "..XXXXXX..XXXXXXX..XXXXXXX..    ",
    "..XXXXXX..XXXXXXX..XXXXXXX..    ",
    "..XXXXXX..XXXXXXXXXXXXXXXX..    ",
    "..XXXXXX..XXXXXXXXXXXXXXXX..    ",
    "..X...XX..XXXXXXXXXXXXXXXX..    ",
    ".... ..X..XXXXXXX..XXXXXXX..    ",
    "..   ..X..XXXXXXX..XXXXXXX..    ",
    "     ..X..XXXXXXX..XXXXXXX..    ",
    "      ....XXXXXXX..XXXXXXX..    ",
    "      ....XXXXXXX..XXXXXXX..    ",
    "       ...XXXXXXXXXXXXXXXX..    ",
    "       ...XXXXXXXXXXXXXXXX..    ",
    "        ..XXXXXXXXXXXXXXXX..    ",
    "        ..XXXXXXXXXXXXXXXX..    ",
    "        ..XXXXXXX..XXXXXXX..    ",
    "        ..XXXXXXX..XXXXXXX..    ",
    "        ..XXXXXXX..XXXXXXX..    ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                "))

def setMouse(name):
    global currentMouse
    compiled = pygame.cursors.compile(name[1])
    pygame.mouse.set_cursor(name[0], (0, 0), compiled[0], compiled[1])
    currentMouse = id(name)

def setDefaultMouse():
    global currentMouse
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    currentMouse = "Default"