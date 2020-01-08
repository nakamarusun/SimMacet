import pygame.math
from shapely.geometry import LineString

def vec2Projection(source: pygame.math.Vector2, dest: pygame.math.Vector2) -> pygame.math.Vector2:
    # Definition: Source vector is PROJECTED ONTO Dest vector
    divided = source.dot(dest) / dest.magnitude_squared()
    return pygame.math.Vector2([ divided * num for num in dest ])

def determinant2x2(y1: list, y2: list):
    return y1[0] * y2[1] - y1[1] * y2[0]

def checkLineIntersection(Ax1y1: list, Ax2y2: list, Bx1y1: list, Bx2y2: list) -> list:
    line1 = LineString( [Ax1y1, Ax2y2] )
    line2 = LineString( [Bx1y1, Bx2y2] )
    intersect = line1.intersection(line2)
    if intersect.is_empty:
        return False, [0, 0]

    return True, [intersect.x, intersect.y]