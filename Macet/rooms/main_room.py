import pygame.surface
import pygame.image
import pygame.draw
import pygame.transform
import pygame.math
from shapely.geometry import LineString, Point, box

import math
import random
import sys
import numpy as np
sys.path.append('..')

import global_variables as GMvar
from objects_manager import Object
from objects.street_nodes import StreetNodes
import game_functions as GMfun
import objects.button as Button
import event_queue as EVque
import mouse_design
import game_math.custom_math_funcs as GMmat
from game_math.road_functions import selectRoad
from objects.car_object import Car
from game_math.displacement_functions import kmhToPixels

class MainCameraSurface:
    # This is the surface in which every object that needs to be movable

    objectsQueue = []   # Objects to be loaded in the camera

    mainSurface = pygame.Surface(GMvar.resolution)    # Main surface of the camera, need to have transparency enabled
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
        GMvar.mainScreenBuffer.blit(objectToDraw, newSurfCoords) # Blit objects to camera surface

    def homeCamera(second: int):
        MainCameraSurface.returnCameraMultiplier -= GMvar.deltaTime * 1/second
        MainCameraSurface.cameraCoords = [ GMfun.cosInterpolation( i, MainCameraSurface.returnCameraMultiplier ) for i in MainCameraSurface.oldHomeCamCoords ]
        if MainCameraSurface.returnCameraMultiplier < 0:
            MainCameraSurface.returnCamera = False

    def update():
        # Clear surface
        GMvar.mainScreenBuffer.fill((255, 255, 255))

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

        # For every object in the camera queue, do their respective update event, and put them in their new coordinates
        for objects in MainCameraSurface.objectsQueue:
            objects.update()
            newSurfCoords = [ a - b for a, b in zip(objects.coords, MainCameraSurface.cameraCoords) ] # Calculate new object coordinates based on camera coords
            GMvar.mainScreenBuffer.blit(objects.image, newSurfCoords) # Blit objects to camera surface

class CarEx(Object):

    def __init__(self, coords=[0,0], image=None, drawn=True, surface=GMvar.mainScreenBuffer):
        super().__init__(coords=coords, image=image, drawn=drawn, surface=surface)
        MainCameraSurface.objectsQueue.append(self)

    def update(self):
        self.speed = [10, 0]
        super().update()

class Canvas:
    
    addRoad = GMvar.defFont12.render("Press ESCAPE to discard and exit new road mode, LEFT CLICK to add road, and ENTER to confirm addition", True, (0, 0, 0))
    editRoadText = GMvar.defFont12.render("LEFT CLICK and drag, then release to select roads. DELETE / BACKSPACE to delete them.", True, (0, 0, 0))

    # Button states clicked
    newRoad = False
    editRoad = False
    addCar = False
    addCarSpawner = False

    # Selection rectangle coordinate
    selectionRect = []

    # Roads list
    roadNodes: StreetNodes = []
    tempRoadNodes: StreetNodes = []

    # Cars spawners list
    carSpawners = []
    cars: Car = []

    # Temporary length when adding road
    temporaryLength: float = 0

    # Constant. Maximum snapping length before cannot draw
    snapLength = 128

    # Direction to compare with the next road
    addRoadDirection = 0
    directionRange = 210 

    # Mouse coordinates when snapped to grid.
    mouseCoords = [0, 0]

    def highlightGrid(cellWidth, cellHeight):
        # Highlight grid based on the data gathered from MainCameraSurface
        size = [ a * b for a, b in zip([cellWidth, cellHeight], MainCameraSurface.cellSize) ] # Size of the grid times the cellWidth and cellHeight
        pygame.draw.rect(GMvar.mainScreenBuffer, (0, 150, 0, 120), (*Canvas.mouseCoords, *size) ) # Draw highlight

    def drawRoads(fromList: list, color: tuple):
        # for node in fromList:
        #     for connectedNodes in node.connectedNodes.keys():
        #         pygame.draw.line(GMvar.mainScreenBuffer, color, [ a - b for a, b in zip(node.coords, MainCameraSurface.cameraCoords) ], [ a - b for a, b in zip(connectedNodes.coords, MainCameraSurface.cameraCoords) ], 16)
        for node in fromList:
            node.drawSelf(GMvar.mainScreenBuffer, [ -i for i in MainCameraSurface.cameraCoords ], color=color)

    def update():

        # Update mouse coords when snapped to grid
        Canvas.mouseCoords = [ (GMvar.latestMouse[i] - ( ( GMvar.latestMouse[i] + MainCameraSurface.gridOffset[i] ) % MainCameraSurface.cellSize[i] ) )  for i in range(2) ]

        if Canvas.newRoad:
            Canvas.highlightGrid(1, 1) # Grid highlight size
            GMfun.insertDrawTopMostQueue(Canvas.addRoad, (5, 25) ) # Instructions

            if pygame.K_ESCAPE in GMvar.keyboardPressedStates:
                bottomGui.addRoad.clicked = False
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
                combinedNode = [Canvas.roadNodes, Canvas.tempRoadNodes[:-2]]
                realMouseCoords = [ a + b for a, b in zip(endLine, MainCameraSurface.cameraCoords)] # Real mouse coordinates. (mouse coords current - camera coords)
                # To avoid any unwanted intersections, offset node coords a bit.
                try:
                    newRoadVec = pygame.math.Vector2( [ a - b for a, b in zip(realMouseCoords, Canvas.tempRoadNodes[-1].coords) ] ).normalize()
                except:
                    newRoadVec = [0, 0]

                intersectionCount = 0
                # Code for drawing temporary road to mouse.
                for i in range(2):
                    for j in range(len(combinedNode[i])):
                        for k in range(len(combinedNode[i][j].connectedNodes.keys())):
                            # Check for intersections between 2 lines. one line is from the last temporary node to mouse coord. second line is every possible road.
                            state, pos = GMmat.checkLineIntersection( [ a + b for a, b in zip(newRoadVec, Canvas.tempRoadNodes[-1].coords) ] , realMouseCoords,  combinedNode[i][j].coords, list( combinedNode[i][j].connectedNodes.keys() )[k].coords, True)
                            # If current mouse coordinates connects to road then snap road.
                            # if realMouseCoords == combinedNode[i][j].coords:
                            #     state = True
                            #     pos = combinedNode[i][j].coords
                            # If intersecting then
                            if state:
                                intersectionCount += 1
                                # Calculate length from intersection.
                                lengthFromIntersection = math.sqrt(sum( [ (a - b) ** 2 for a, b in zip(pos, realMouseCoords) ] ))
                                snap = lengthFromIntersection < Canvas.snapLength
                                canDrawRoad = True if snap else False
                                # The node data for the one intersecting
                                # If snap then
                                if snap:
                                    # pos = [ pos[i] - (pos[i] % MainCameraSurface.cellSize[i]) for i in range(2) ] # If want to snap to grid, do this.
                                    firstNode: StreetNodes = combinedNode[i][j]
                                    secondNode: StreetNodes = list( combinedNode[i][j].connectedNodes.keys() )[k]
                                    break # Break from for loop
                        if canDrawRoad == False or snap: break # Continue breaking
                    if canDrawRoad == False or snap: break # Still breaking

                if intersectionCount > 1:
                    canDrawRoad = False

                # This is the script to check if road is going back 180 degrees, overlapping the previous road.
                # This works by comparing the normalized vector2 of the before road, and the current road by mouse.
                # Fixed problem where you can't place roads if there is two or more connectedNodes
                if len(Canvas.tempRoadNodes) > 1:
                    vec1: pygame.math.Vector2 = list(Canvas.tempRoadNodes[-2].connectedNodes.values())[-1][0]
                    vec2 = pygame.math.Vector2( [ b - a for a, b in zip(realMouseCoords, Canvas.tempRoadNodes[-1].coords) ] )
                    try:
                        if vec1.normalize() == vec2.normalize():
                            canDrawRoad = False
                            snap = False
                    except:
                        pass

                    roadMouseDirection = ( np.arctan2(*newRoadVec[::-1]) * 180/math.pi )
                    roadMouseDirection = 360 + roadMouseDirection if roadMouseDirection < 0 else roadMouseDirection
                    if not ((roadMouseDirection < Canvas.addRoadDirection + Canvas.directionRange/2 or (roadMouseDirection < Canvas.addRoadDirection + Canvas.directionRange/2 + 360 and roadMouseDirection > Canvas.addRoadDirection - Canvas.directionRange/2 + 360 )) and roadMouseDirection > Canvas.addRoadDirection - Canvas.directionRange/2):
                        canDrawRoad = False

                color = (52, 139, 201) if snap else ((50, 150, 50) if canDrawRoad else (150, 50, 50))
                GMfun.drawBetterLine(GMvar.mainScreenBuffer, color, *[ b + 16 if (b > a - c) else b for a, b, c in zip(pos, startLine, MainCameraSurface.cameraCoords) ] if snap else startLine, *[ a - b for a, b in zip(pos, MainCameraSurface.cameraCoords ) ] if snap else endLine, 16) # If snaps to road, change the end line to the snapped position, else to mouse position
                GMfun.insertDrawTopMostQueue( GMvar.defFont12.render("Length: {}m".format(str(round(length, 3))), True, (0, 0, 0) ), (GMvar.latestMouse[0] + 20, GMvar.latestMouse[1]) ) # Draw road estimation description
                GMfun.insertDrawTopMostQueue( GMvar.defFont12.render("Total length: {}m".format(str(round(Canvas.temporaryLength, 3))), True, (0, 0, 0) ), (GMvar.latestMouse[0] + 20, GMvar.latestMouse[1] + 10) ) # Draw road estimation description

            beginConnectRoad = False
            # If clicked on a road when temporary road is still empty.
            # This creates a new intersection point on the position where the mouse hovers, allowing the user to make a new road node from existing roads.
            if len(Canvas.tempRoadNodes) == 0:
                for i in range(len(Canvas.roadNodes)):
                    for connectedNodes in Canvas.roadNodes[i].connectedNodes.keys():
                        point = Point(Canvas.mouseCoords)
                        line = LineString( [ Canvas.roadNodes[i].coords, connectedNodes.coords ] )
                        if point.intersection(line):
                            pos = point
                            firstNode: StreetNodes = Canvas.roadNodes[i]
                            canDrawRoad = True
                            beginConnectRoad = True
                            break
                    if beginConnectRoad: break

            # Draw temporary roads when left clicked
            if GMvar.mouseStateSingle[0] and GMvar.latestMouse[1] < bottomGui.guiHeightChange + bottomGui.sliderHeight and canDrawRoad:
                # Add length to total length
                Canvas.temporaryLength += length
                # If mouse is clicked on the canvas,
                if not snap:
                    newMouseCoords = [ MainCameraSurface.getRealMouseCoords()[i] - ( (MainCameraSurface.getRealMouseCoords()[i] % MainCameraSurface.cellSize[i]) ) for i in range(2) ] # New mouse coords adjusted with the camera
                    newNode = StreetNodes(newMouseCoords, [], [firstNode] if beginConnectRoad else ( [Canvas.tempRoadNodes[-1]] if len(Canvas.tempRoadNodes) > 0 else [] ), 0 ) # Create new object StreetNodes with current snapped mouse coordinates, empty front nodes, with back nodes from the last added.
                    if beginConnectRoad:
                        firstNode.connectTo( newNode )
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
                    firstNode.connectTo(newNode)
                if len(Canvas.tempRoadNodes) > 0:
                    Canvas.addRoadDirection = ( np.arctan2( *[ b - a for a, b in zip(Canvas.tempRoadNodes[-1].coords[::-1], newNode.coords[::-1]) ] ) * 180/math.pi )
                    Canvas.addRoadDirection = 360 + Canvas.addRoadDirection if Canvas.addRoadDirection < 0 else Canvas.addRoadDirection
                    Canvas.tempRoadNodes[-1].connectTo(newNode) # Add newNode to front node of the previous StreetNode
                Canvas.tempRoadNodes.append( newNode ) # Add newNode to current roadNodes list

            # When Enter clicked, save current temp roads to road nodes
            if pygame.K_RETURN in GMvar.keyboardPressedStates:
                Canvas.roadNodes += Canvas.tempRoadNodes
                del Canvas.tempRoadNodes[:]
        else:
            Canvas.temporaryLength = 0
            Canvas.addRoadDirection = 0

        if Canvas.editRoad:
            Canvas.highlightGrid(1, 1) # Grid highlight size
            GMfun.insertDrawTopMostQueue(Canvas.editRoadText, (5, 25) ) # Instructions

            if GMvar.mouseState[0]:
                del Canvas.tempRoadNodes[:]
                rectSize = [ a - b for a, b in zip(GMvar.latestMouse, GMvar.latestMouseLeft) ]
                rectSurface = pygame.Surface( [ abs(num) for num in rectSize ] )
                rectSurface.set_alpha(100)
                rectSurface.fill( (84, 184, 214) )
                rectCoords = GMvar.latestMouseLeft
                rectCoords = [ a + b if b < 0 else a for a, b in zip(rectCoords, rectSize) ]
                GMvar.mainScreenBuffer.blit( rectSurface, rectCoords )

                rectCoords = [ a + b for a, b in zip(rectCoords, MainCameraSurface.cameraCoords)]

                Canvas.selectionRect = [ *rectCoords, *[ a + b for a, b in zip([ abs(num) for num in rectSize ], rectCoords) ] ]
            
            if not GMvar.mouseState[0] and len(Canvas.selectionRect) > 0:
                # Make a rectangle shapely object from the selection made
                rectangleGeometry = box( *Canvas.selectionRect )
                # Check if nodes / line intersection is in selection
                for nodes in Canvas.roadNodes:
                    for connectedNodes in  nodes.connectedNodes.keys():
                        line = LineString( [ nodes.coords, connectedNodes.coords ] )
                        # If line is intersecting with selection rect, then append to list
                        if line.intersects(rectangleGeometry):
                            Canvas.tempRoadNodes.append(nodes)
                            break
                    # If node is in selection rect, then append to list
                    if nodes.coords[0] > Canvas.selectionRect[0] and nodes.coords[0] < Canvas.selectionRect[2]:
                        if nodes.coords[1] > Canvas.selectionRect[1] and nodes.coords[1] < Canvas.selectionRect[3]:
                            Canvas.tempRoadNodes.append(nodes)
            
            # Delete selection rect if mouse is not clicked
            if not GMvar.mouseState[0]:
                del Canvas.selectionRect[:]

            # Recreate new canvas.roadnodes without anything in canvas temproadnodes. so, basically Canvas.roadNodes = Canvas.roadNodes - Canvas.tempRoadNodes
            if pygame.K_DELETE  in GMvar.keyboardPressedStates or pygame.K_BACKSPACE in GMvar.keyboardPressedStates and len(Canvas.tempRoadNodes) > 0:
                # If an element of roadnodes is in temproadnodes, delete the connectedRoads element of the roadnodes' backnode.
                # for i in range(len(Canvas.roadNodes)):
                #     if Canvas.roadNodes[i] in Canvas.tempRoadNodes:
                #         for j in range(len(Canvas.roadNodes[i].backNodes)):
                #             del Canvas.roadNodes[i].backNodes[j].connectedNodes[Canvas.roadNodes[i]] # NEED SOME FIXING HOMIE
                # Delete from roadnodes
                Canvas.roadNodes = [ nodes for nodes in Canvas.roadNodes if nodes not in Canvas.tempRoadNodes ]
                # Delete any reference to deleted roads, to avoid car crossing the road even after deleted.
                # Dont forget to delete cars too.
                for deletedNodes in Canvas.tempRoadNodes:
                    deletedNodes.connectedNodes = {}
                    deletedCars = 0
                    for i in range(len(Canvas.cars)):
                        i -= deletedCars
                        if Canvas.cars[i].nodeAnchor == deletedNodes:
                            Canvas.cars.pop(i)
                            deletedCars += 1

                del Canvas.tempRoadNodes[:]
        else:
            del Canvas.selectionRect[:]

        if Canvas.addCarSpawner:
            if GMvar.mouseStateSingle[2]:
                selected = selectRoad( MainCameraSurface.getRealMouseCoords(), Canvas.roadNodes, 16 )
                if selected != None:
                    node, connectedNode, selectedCoord = selected
        
        if Canvas.addCar:
            if GMvar.mouseStateSingle[0]:
                try:
                    selected = selectRoad( MainCameraSurface.getRealMouseCoords(), Canvas.roadNodes, 16 )
                except:
                    selected = None

                if selected != None:
                    node, connectedNode, selectedCoord = selected

                    # Search for the absolute end of the road (curEndNode)
                    longestLength = 0
                    curEndNode: StreetNodes = None
                    for connected in node.connectedNodes:
                        curLength = node.connectedNodes[connected][0].length_squared()
                        if curLength > longestLength:
                            curEndNode = connected
                            longestLength = curLength

                    # Define start point and end point
                    lineToCheck = LineString( [ [*selectedCoord], [*curEndNode.coords] ] )

                    roadSplitChoices = []
                    
                    for connected in node.connectedNodes:
                        if Point(connected.coords).intersects(lineToCheck):
                            roadSplitChoices.append(connected)

                    Canvas.cars.append( Car(node, roadSplitChoices[ random.randint(0, len(roadSplitChoices) - 1) ], kmhToPixels(200), selectedCoord, GMvar.mainScreenBuffer) )
                    del roadSplitChoices # Delete references

        Canvas.drawRoads(Canvas.roadNodes, (30, 30, 30))
        Canvas.drawRoads(Canvas.tempRoadNodes, (50, 150, 50) if Canvas.newRoad else (52, 192, 217))

        deletedCars = 0
        for i in range(len(Canvas.cars)):
            # If car has reached its end-destination then
            i -= deletedCars
            if Canvas.cars[i].update(MainCameraSurface.cameraCoords):
                # Delete car from list. Then, index is subtracted by 1, so not outOfRangeError
                Canvas.cars.pop(i)
                deletedCars += 1

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

    surfTransparent = pygame.Surface((111, 200), pygame.SRCALPHA)
    surfGui = pygame.Surface((GMvar.resolution[0], guiHeight)) # an isolated Surface in which to draw the GUI

    # Buttons
    reCenter = Button.Button(surfTransparent, (0, 52), "images/sprites/GuiButtons/Recenter.png", "images/sprites/GuiButtons/RecenterTog.png", (0, 0, 111, 111))
    buttonTopLeft = Button.Button(surfGui, (GMvar.resolution[0]/2 - 156, 0 ), "images/sprites/GuiButtons/TopLeft.png", "images/sprites/GuiButtons/TopLeftTog.png", (0, 10, 91, 48))
    buttonTopRight = Button.Button(surfGui, (GMvar.resolution[0]/2 - 156, 0 ), "images/sprites/GuiButtons/TopRight.png", "images/sprites/GuiButtons/TopRightTog.png", (221, 10, 91, 48))
    buttonBotLeft = Button.ToggleButton(surfGui, (GMvar.resolution[0]/2 - 156, 0 ), "images/sprites/GuiButtons/BotLeft.png", "images/sprites/GuiButtons/BotLeftTog.png", (0, 64, 124, 48))
    buttonBotRight = Button.ToggleButton(surfGui, (GMvar.resolution[0]/2 - 156,0 ), "images/sprites/GuiButtons/BotRight.png", "images/sprites/GuiButtons/BotRightTog.png", (188, 64, 124, 48))

    addRoad = Button.ToggleButton(surfGui, (GMvar.resolution[0]/2 + 171, 10 ), "images/sprites/GuiButtons/AddRoad.png", "images/sprites/GuiButtons/AddRoadTog.png", (0, 0, 46, 47))
    inspectRoad = Button.ToggleButton(surfGui, (GMvar.resolution[0]/2 + 171, 10 ), "images/sprites/GuiButtons/InspectRoad.png", "images/sprites/GuiButtons/InspectRoadTog.png", (0, 54, 46, 47))

    addCar = Button.ToggleButton(surfGui, (GMvar.resolution[0]/2 - 217, 10 ), "images/sprites/GuiButtons/AddCar.png", "images/sprites/GuiButtons/AddCarTog.png", (0, 0, 46, 47))
    addCarSpawner = Button.ToggleButton(surfGui, (GMvar.resolution[0]/2 - 217, 10 ), "images/sprites/GuiButtons/AddCarSpawner.png", "images/sprites/GuiButtons/AddCarSpawnerTog.png", (0, 54, 46, 47))
    
    # Conflicts
    buttonBotLeft.addConflictButtons([buttonBotRight])
    buttonBotRight.addConflictButtons([buttonBotLeft])

    addRoad.addConflictButtons([inspectRoad])
    inspectRoad.addConflictButtons([addRoad])

    addCar.addConflictButtons([addCarSpawner])
    addCarSpawner.addConflictButtons([addCar])
    
    # List
    roadButtons = [addRoad, inspectRoad]
    carButtons = [addCar, addCarSpawner]

    Buttons = [reCenter, buttonTopLeft, buttonTopRight, buttonBotLeft, buttonBotRight]
    
    def update(): # pylint: disable=fixme, no-method-argument
        # list of buttons that will be drawn
        buttonAdditions = []

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
        bottomGui.surfTransparent.fill((0))
        bottomGui.surfGui.fill((0))

        slider, rect = GMfun.rotationAnchor(bottomGui.slider, bottomGui.sliderDirection, (0.5, 0.5)) # Get rotation


        # Draw and blit to main screen buffer [ a + b for a, b in zip((rect.x, rect.y), (bottomGui.sliderX, bottomGui.sliderYOffset)) ]
        bottomGui.surfTransparent.blit( slider, (rect[0] + 8, rect[1] + 10) )     # Blit slider button to surface
        pygame.draw.rect(bottomGui.surfGui, (44, 66, 81), (0, 0, GMvar.resolution[0], bottomGui.guiHeight + 0)) # Plus 1 to fix the weird 1 pixel

        # TOGGLE BUTTON CHECK EVENTS HERE
        # Road button
        if bottomGui.buttonBotRight.checkState():
            buttonAdditions += bottomGui.roadButtons
            if mouse_design.currentMouse != mouse_design.mouseRoad and GMvar.customMouse:
                mouse_design.setMouse(mouse_design.mouseRoad)           # So apparently, changing the mouse design is VERY LAGGY OK F OFF
        else:
            if mouse_design.currentMouse != "Default" and GMvar.customMouse:
                mouse_design.setDefaultMouse()
            bottomGui.addRoad.clicked = False
            bottomGui.inspectRoad.clicked = False

        Canvas.newRoad = bottomGui.addRoad.checkState()
        Canvas.editRoad = bottomGui.inspectRoad.checkState()

        if bottomGui.buttonBotLeft.checkState():
            buttonAdditions += bottomGui.carButtons
        else:
            bottomGui.addCar.clicked = False
            bottomGui.addCarSpawner.clicked = False

        Canvas.addCar = bottomGui.addCar.checkState()

        # Draw buttons to surface
        # Update buttons
        toggled = False
        bottomGui.Buttons[0].update(GMvar.resolution[0]/2 - 55, bottomGui.guiHeightChange )
        for button in bottomGui.Buttons[1:] + buttonAdditions:
            button.update(0, bottomGui.guiHeightChange + bottomGui.sliderHeight) # Draw buttons

        GMvar.mainScreenBuffer.blit(bottomGui.surfGui, (0, bottomGui.guiHeightChange + bottomGui.sliderHeight)) # Finally, draw everything to main buffer
        GMvar.mainScreenBuffer.blit(bottomGui.surfTransparent, (GMvar.resolution[0]/2 - 55, bottomGui.guiHeightChange)) # Draw transparent surface to main buffer
