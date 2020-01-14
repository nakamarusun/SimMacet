import pygame.math
from shapely.geometry import LineString

def vec2Projection(source: pygame.math.Vector2, dest: pygame.math.Vector2) -> pygame.math.Vector2:
    # Definition: Source vector is PROJECTED ONTO Dest vector
    divided = source.dot(dest) / dest.magnitude_squared()
    return pygame.math.Vector2([ divided * num for num in dest ])

def determinant2x2(y1: list, y2: list):
    return y1[0] * y2[1] - y1[1] * y2[0]

def checkLineIntersection(Ax1y1: list, Ax2y2: list, Bx1y1: list, Bx2y2: list, canTouch: bool) -> list:
    line1 = LineString( [Ax1y1, Ax2y2] )
    line2 = LineString( [Bx1y1, Bx2y2] )
    intersect = line1.intersection(line2)
    if intersect.is_empty or not line1.crosses(line2):
        if not canTouch:
            return False, [0, 0]

    try:
        return True, [intersect.x, intersect.y]
    except:
        return False, [0, 0]

def triangleArea(point1: list, point2: list, point3: list) -> float:
    return ( point1[0] * (point2[1] - point3[1]) + point2[0] * (point3[1] - point1[1]) + point3[0] * (point1[1] - point2[1]) ) / 2

def isPointInTriangle(point: list, trianglePoint1: list, trianglePoint2: list, trianglePoint3: list, area=0) -> bool:
    area = area
    if area == 0:
        area = triangleArea(trianglePoint1, trianglePoint2, trianglePoint3)

    triangle1 = triangleArea(point, trianglePoint1, trianglePoint2)
    triangle2 = triangleArea(point, trianglePoint2, trianglePoint3)
    triangle3 = triangleArea(point, trianglePoint3, trianglePoint1)

    return (triangle1 + triangle2 + triangle3 == area)