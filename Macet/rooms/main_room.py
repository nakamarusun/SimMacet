import pygame.surface
import pygame.image
import pygame.draw
import pygame.transform
import pygame.math

import math
import sys
sys.path.append('..')

import global_variables as GMvar
from objects_manager import Object
from objects.street_nodes import StreetNodes
import game_functions as GMfun
import objects.button as Button
import event_queue as EVque
import mouse_design
import game_math.custom_math_funcs as GMmat

class MainCameraSurfaceBlitter:
    def update():
        GMvar.mainScreenBuffer.blit(MainCameraSurface.mainSurface, (0, 0) ) # Blit to main buffer

class MainCameraSurface:
    # This is the surface in which every object that needs to be movable

    objectsQueue = []   # Objects to be loaded in the camera

    mainSurface = pygame.Surface(GMvar.resolution, pygame.SRCALPHA)     # Main surface of the camera, need to have transparency enabled
    cameraCoords = [0, 0]   # Current coordinates of the camera

    cellSize = (16, 16) # Grid cell size for the game

    # for gridSize can't use list comprehension, will throw an error because of class
    gridSize = [0, 0] # Cell total for width and height
    gridSize[0] = GMvar.resolution[0] // cellSize[0] + 1
    gridSize[1] = GMvar.resolution[1] // cellSize[1] + 2

    gridOffset = [0, 0]

    returnCamera = False # If true, return camera to [0, 0]
    returnCameraMultiplier = 1
    oldHomeCamCoords = [0, 0]

    def getRealMouseCoords() -> list:
        return [ a + b for a, b in zip(MainCameraSurface.cameraCoords, GMvar.latestMouse) ]

    def drawToMainCameraSurface(coords: list, objectToDraw):
        newSurfCoords = [ a - b for a, b in zip(coords, MainCameraSurface.cameraCoords) ] # Calculate new object coordinates based on camera coords
        MainCameraSurface.mainSurface.blit(objectToDraw, newSurfCoords) # Blit objects to camera surface

    def homeCamera(second: int):
        MainCameraSurface.returnCameraMultiplier -= GMvar.deltaTime * 1/second
        MainCameraSurface.cameraCoords = [ GMfun.cosInterpolation( i, MainCameraSurface.returnCameraMultiplier ) for i in MainCameraSurface.oldHomeCamCoords ]
        if MainCameraSurface.returnCameraMultiplier < 0:
            MainCameraSurface.returnCamera = False

    def update():

        # If return camera, the move the camera back to home using cos interpolation
        if MainCameraSurface.returnCamera:
            MainCameraSurface.homeCamera(1)
        else:
            MainCameraSurface.oldHomeCamCoords = MainCameraSurface.cameraCoords
            MainCameraSurface.returnCameraMultiplier = 1

        # If mouse is clicked and dragged
        if GMvar.mouseState[2]:
            MainCameraSurface.cameraCoords = [ a - b for a, b in zip(MainCameraSurface.cameraCoords, GMvar.mouseDelta) ]  # Substract cameracoords by delta mouse movements

        # Draw grid by considering camera movements. Size is constant and the grid is drawn directly on the main buffer.
        MainCameraSurface.gridOffset = [ (MainCameraSurface.cameraCoords[i] % MainCameraSurface.cellSize[i]) for i in range(2) ]    # Grid offset based on the camera coordinates
        for x in range(2):
            for i in range(MainCameraSurface.gridSize[x]):
                pointPosition = i * MainCameraSurface.cellSize[x] - MainCameraSurface.gridOffset[x] # Every node point to draw the line.
                startLine = (pointPosition, 0) if x == 0 else (0, pointPosition)
                endLine = (pointPosition, GMvar.resolution[::-1][x]) if x == 0 else (GMvar.resolution[::-1][x], pointPosition)
                pygame.draw.line( GMvar.mainScreenBuffer, (230, 230, 230), startLine, endLine) # Draw line

        # Clear surface
        MainCameraSurface.mainSurface.fill((0, 0, 0, 0))

        # For every object in the camera queue, do their respective update event, and put them in their new coordinates
        for objects in MainCameraSurface.objectsQueue:
            objects.update()
            newSurfCoords = [ a - b for a, b in zip(objects.coords, MainCameraSurface.cameraCoords) ] # Calculate new object coordinates based on camera coords
            MainCameraSurface.mainSurface.blit(objects.image, newSurfCoords) # Blit objects to camera surface

class Car(Object):

    def __init__(self, coords=[0,0], image=None, drawn=True, surface=GMvar.mainScreenBuffer):
        super().__init__(coords=coords, image=image, drawn=drawn, surface=surface)
        MainCameraSurface.objectsQueue.append(self)

    def update(self):
        self.speed = [10, 0]
        super().update()

class Canvas:
    
    addRoad = GMvar.defFont12.render("Press ESCAPE to discard and exit new road mode, LEFT CLICK to add road, and ENTER to confirm addition", True, (0, 0, 0))

    editRoad = False

    roadNodes: StreetNodes = []
    tempRoadNodes: StreetNodes = []

    temporaryLength: float = 0

    snapLength = 128

    # Mouse coordinates when snapped to grid.
    mouseCoords = [0, 0]

    def highlightGrid(cellWidth, cellHeight):
        # Highlight grid based on the data gathered from MainCameraSurface
        size = [ a * b for a, b in zip([cellWidth, cellHeight], MainCameraSurface.cellSize) ] # Size of the grid times the cellWidth and cellHeight
        pygame.draw.rect(MainCameraSurface.mainSurface, (0, 150, 0, 120), (*Canvas.mouseCoords, *size) ) # Draw highlight

    def drawRoads(fromList: list, color: list):
        for node in fromList:
            for connectedNodes in node.connectedNodes.keys():
                pygame.draw.line(MainCameraSurface.mainSurface, color, [ a - b for a, b in zip(node.coords, MainCameraSurface.cameraCoords) ], [ a - b for a, b in zip(connectedNodes.coords, MainCameraSurface.cameraCoords) ], 16)

    def update():

        if Canvas.editRoad:
            # Update mouse coords when snapped to grid
            Canvas.mouseCoords = [ (GMvar.latestMouse[i] - ( ( GMvar.latestMouse[i] + MainCameraSurface.gridOffset[i] ) % MainCameraSurface.cellSize[i] ) )  for i in range(2) ]
            Canvas.highlightGrid(1, 1) # Grid highlight size
            GMfun.insertDrawTopMostQueue(Canvas.addRoad, (5, 25) ) # Instructions

            if pygame.K_ESCAPE in GMvar.keyboardPressedStates:
                bottomGui.buttonBotRight.clicked = False
                del Canvas.tempRoadNodes[:]

            length = 0  # Road length for now
            canDrawRoad = True # If can draw road, not intersecting with others
            lengthFromIntersection = Canvas.snapLength + 1 # The length from the intersection point to the road to the mouse. (This is just the default valie)
            snap = False # If the length fo intersection is lower than constant snap. it means the road is snapped to another road.
            # Draw road estimation
            if len(Canvas.tempRoadNodes) > 0:
                startLine = [ a - b for a, b in zip(Canvas.tempRoadNodes[-1].coords, MainCameraSurface.cameraCoords) ]
                endLine = Canvas.mouseCoords

                length = math.sqrt( sum([ (b - a) ** 2 for a, b in zip(startLine, endLine) ]) ) * 1.875 # Road length in meters
                
                # If intersects, disable road drawing
                combinedNode = [Canvas.roadNodes, Canvas.tempRoadNodes[:-1]]
                realMouseCoords = [ a + b for a, b in zip(endLine, MainCameraSurface.cameraCoords)] # Real mouse coordinates. (mouse coords current - camera coords)
                for i in range(2):
                    for j in range(len(combinedNode[i])):
                        for k in range(len(combinedNode[i][j].connectedNodes.keys())):
                            # Check for intersections between 2 lines. one line is from the last temporary node to mouse coord. second line is every possible road.
                            state, pos = GMmat.checkLineIntersection(Canvas.tempRoadNodes[-1].coords, realMouseCoords,  combinedNode[i][j].coords, list( combinedNode[i][j].connectedNodes.keys() )[k].coords, False)
                            # If current mouse coordinates connects to road then snap road.
                            if realMouseCoords == combinedNode[i][j].coords:
                                state = True
                                pos = combinedNode[i][j].coords
                            # If intersecting then
                            if state:
                                # Calculate length from intersection.
                                lengthFromIntersection = math.sqrt(sum( [ (a - b) ** 2 for a, b in zip(pos, realMouseCoords) ] ))
                                snap = lengthFromIntersection < Canvas.snapLength
                                canDrawRoad = True if snap else False
                                # The node data for the one intersecting
                                # If snap then
                                if snap:
                                    pos = [ pos[i] - (pos[i] % MainCameraSurface.cellSize[i]) for i in range(2) ]
                                    firstNode = combinedNode[i][j]
                                    secondNode = list( combinedNode[i][j].connectedNodes.keys() )[k]
                                    break # Break from for loop
                        if canDrawRoad == False or snap: break # Continue breaking
                    if canDrawRoad == False or snap: break # Still breaking

                # This is the script to check if road is going back 180 degrees, overlapping the previous road.
                # This works by comparing the normalized vector2 of the before road, and the current road by mouse.
                if len(Canvas.tempRoadNodes) > 1:
                    vec1: pygame.math.Vector2 = list(Canvas.tempRoadNodes[-2].connectedNodes.values())[0]
                    vec2 = pygame.math.Vector2( [ a - b for a, b in zip(Canvas.tempRoadNodes[-1].coords, realMouseCoords) ] )
                    try:
                        if vec1.normalize() == vec2.normalize():
                            canDrawRoad = False
                            snap = False
                    except:
                        pass

                color = (52, 139, 201) if snap else ((50, 150, 50) if canDrawRoad else (150, 50, 50))
                pygame.draw.line(MainCameraSurface.mainSurface, color, startLine, [ a - b for a, b in zip(pos, MainCameraSurface.cameraCoords ) ] if snap else endLine, 16) # If snaps to road, change the end line to the snapped position, else to mouse position
                GMfun.insertDrawTopMostQueue( GMvar.defFont12.render("Length: {}m".format(str(round(length, 3))), True, (0, 0, 0) ), (GMvar.latestMouse[0] + 20, GMvar.latestMouse[1]) ) # Draw road estimation description
                GMfun.insertDrawTopMostQueue( GMvar.defFont12.render("Total length: {}m".format(str(round(Canvas.temporaryLength, 3))), True, (0, 0, 0) ), (GMvar.latestMouse[0] + 20, GMvar.latestMouse[1] + 10) ) # Draw road estimation description

            # Draw temporary roads when left clicked
            if GMvar.mouseStateSingle[0] and GMvar.latestMouse[1] < bottomGui.guiHeightChange + bottomGui.sliderHeight and canDrawRoad:
                # Add length to total length
                Canvas.temporaryLength += length
                # If mouse is clicked on the canvas,
                if not snap:
                    newMouseCoords = [ MainCameraSurface.getRealMouseCoords()[i] - ( (MainCameraSurface.getRealMouseCoords()[i] % MainCameraSurface.cellSize[i]) ) for i in range(2) ] # New mouse coords adjusted with the camera
                    newNode = StreetNodes(newMouseCoords, [], [Canvas.tempRoadNodes[-1]] if len(Canvas.tempRoadNodes) > 0 else [], 0 ) # Create new object StreetNodes with current snapped mouse coordinates, empty front nodes, with back nodes from the last added.
                else:
                    ###################### Creates entirely new node, deletes already preexisting node.
                    # newNode = StreetNodes( pos, [secondNode], [Canvas.tempRoadNodes[-1]] if len(Canvas.tempRoadNodes) > 0 else [], 0 )
                    # for i in range(len(secondNode.backNodes)):
                    #     if secondNode.backNodes[i] == firstNode:
                    #         secondNode.backNodes[i] = newNode
                    # del firstNode.connectedNodes[secondNode]
                    # firstNode.connectedNodes[newNode] = pygame.math.Vector2( [ a - b for a, b in zip(firstNode.coords, pos) ] )
                    ###################### Creates new node, but overlaps with other node.
                    newNode = StreetNodes( pos, [secondNode], [Canvas.tempRoadNodes[-1]] if len(Canvas.tempRoadNodes) > 0 else [], 0 ) # Draw new node, with the connected node to the second node.
                if len(Canvas.tempRoadNodes) > 0:
                    Canvas.tempRoadNodes[-1].connectedNodes[newNode] = pygame.math.Vector2( [ newNode.coords[i] - Canvas.tempRoadNodes[-1].coords[i] for i in range(2) ] ) # Add newNode to front node of the previous StreetNode
                Canvas.tempRoadNodes.append( newNode ) # Add newNode to current roadNodes list

            # When Enter clicked, save current temp roads to road nodes
            if pygame.K_RETURN in GMvar.keyboardPressedStates:
                Canvas.roadNodes += Canvas.tempRoadNodes
                del Canvas.tempRoadNodes[:]

        else:
            Canvas.temporaryLength = 0
        Canvas.drawRoads(Canvas.tempRoadNodes, (50, 150, 50))
        Canvas.drawRoads(Canvas.roadNodes, (50, 50, 50))

class bottomGui:

    # image for the slider
    slider = pygame.image.load("images/sprites/GuiButtons/Slider.png").convert_alpha()
    sliderDirection = 0 # Slider's image direction
    sliderRect = slider.get_rect() # Slider rect

    guiHeight = 120 # The height of the rectangle part of the gui
    sliderHeight = sliderRect[3] + 50 # The height of the slider's image plus some breathing room

    guiOpen = False # State whether gui is open or nah
    guiHeightChange = GMvar.resolution[1] - sliderHeight # Current gui's position on the screen.
    sliderX = GMvar.resolution[0]/2 - sliderRect[2]/2 # Middle point of the slider
    sliderYOffset = 15 # Offset of slider button from the top of the surface

    openSpeed = 50 # Initial speed to open the GUI
    increment = 500 # Speed acceleration

    surfGui = pygame.Surface((GMvar.resolution[0], guiHeight + sliderHeight),pygame.SRCALPHA).convert_alpha() # an isolated Surface in which to draw the GUI

    # Buttons
    reCenter = Button.Button(surfGui, (GMvar.resolution[0]/2 - 55, sliderHeight - 35), "images/sprites/GuiButtons/Recenter.png", "images/sprites/GuiButtons/RecenterTog.png", (0, 0, 111, 111))
    buttonTopLeft = Button.Button(surfGui, (GMvar.resolution[0]/2 - 156, sliderHeight ), "images/sprites/GuiButtons/TopLeft.png", "images/sprites/GuiButtons/TopLeftTog.png", (0, 10, 91, 48))
    buttonTopRight = Button.Button(surfGui, (GMvar.resolution[0]/2 - 156, sliderHeight ), "images/sprites/GuiButtons/TopRight.png", "images/sprites/GuiButtons/TopRightTog.png", (221, 10, 91, 48))
    buttonBotLeft = Button.ToggleButton(surfGui, (GMvar.resolution[0]/2 - 156, sliderHeight ), "images/sprites/GuiButtons/BotLeft.png", "images/sprites/GuiButtons/BotLeftTog.png", (0, 64, 124, 48))
    buttonBotRight = Button.ToggleButton(surfGui, (GMvar.resolution[0]/2 - 156, sliderHeight ), "images/sprites/GuiButtons/BotRight.png", "images/sprites/GuiButtons/BotRightTog.png", (188, 64, 124, 48))

    Buttons = [reCenter, buttonTopLeft, buttonTopRight, buttonBotLeft, buttonBotRight]
    
    def update(): # pylint: disable=fixme, no-method-argument
        
        # CLICK BUTTON CHECK EVENTS HERE
        if bottomGui.reCenter.checkState():
            MainCameraSurface.returnCamera = True

        # If mouse is clicked on the button then open/close gui
        if GMfun.mouseClickedArea(0, bottomGui.sliderX, (bottomGui.sliderX + bottomGui.sliderRect[2]), (bottomGui.guiHeightChange + bottomGui.sliderYOffset), (bottomGui.guiHeightChange + bottomGui.sliderRect[3] + bottomGui.sliderYOffset)):
            bottomGui.guiOpen = not bottomGui.guiOpen

        # If open and not in position, set the coordinates
        if bottomGui.guiOpen:
            if bottomGui.guiHeightChange > (GMvar.resolution[1] - bottomGui.guiHeight - bottomGui.sliderHeight):
                bottomGui.openSpeed += bottomGui.increment * GMvar.deltaTime
                bottomGui.guiHeightChange -= bottomGui.openSpeed * GMvar.deltaTime
            else:
                bottomGui.guiHeightChange = GMvar.resolution[1] - bottomGui.guiHeight - bottomGui.sliderHeight
            if bottomGui.sliderDirection < 180:
                bottomGui.sliderDirection += 450 * GMvar.deltaTime
            else:
                bottomGui.sliderDirection = 180
        else:
            if bottomGui.guiHeightChange < (GMvar.resolution[1] - bottomGui.sliderHeight):
                bottomGui.openSpeed -= bottomGui.increment * GMvar.deltaTime
                bottomGui.guiHeightChange += bottomGui.openSpeed * GMvar.deltaTime
            else:
                # Reset everything so the numbers are not weird
                bottomGui.openSpeed = 50
                bottomGui.guiHeightChange = GMvar.resolution[1] - bottomGui.sliderHeight
            if bottomGui.sliderDirection > 0:
                bottomGui.sliderDirection -= 450 * GMvar.deltaTime
            else:
                bottomGui.sliderDirection = 0

        bottomGui.sliderDirection = round(bottomGui.sliderDirection)

        # Clear surface
        bottomGui.surfGui.fill((0, 0, 0, 0))

        slider, rect = GMfun.rotationAnchor(bottomGui.slider, bottomGui.sliderDirection, (0.5, 0.5)) # Get rotation


        # Draw and blit to main screen buffer
        bottomGui.surfGui.blit( slider, [ a + b for a, b in zip((rect.x, rect.y), (bottomGui.sliderX, bottomGui.sliderYOffset)) ] )     # Blit slider button to surface
        pygame.draw.rect(bottomGui.surfGui, (44, 66, 81), (0, bottomGui.sliderHeight, GMvar.resolution[0], bottomGui.guiHeight + 0)) # Plus 1 to fix the weird 1 pixel

        # Draw buttons to surface
        # Update buttons
        toggled = False
        for button in bottomGui.Buttons:
            button.update(0, bottomGui.guiHeightChange) # Draw buttons
            try:
                if toggled and button.clicked:
                    button.clicked = False
                if button.clicked == True:
                    toggled = True
            except:
                pass

        # TOGGLE BUTTON CHECK EVENTS HERE
        # New Road
        if bottomGui.buttonBotRight.checkState():
            Canvas.editRoad = True
            if mouse_design.currentMouse != mouse_design.mouseRoad:
                mouse_design.setMouse(mouse_design.mouseRoad)
        else:
            Canvas.editRoad = False
            if mouse_design.currentMouse != "Default":
                mouse_design.setDefaultMouse()

        GMvar.mainScreenBuffer.blit(bottomGui.surfGui, (0, bottomGui.guiHeightChange + 1)) # Finally, draw everything to main buffer
