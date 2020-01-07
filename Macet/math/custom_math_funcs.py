import pygame.math

def vec2Projection(source: pygame.math.Vector2, dest: pygame.math.Vector2) -> pygame.math.Vector2:
    # Definition: Source vector is PROJECTED ONTO Dest vector
    divided = source.dot(dest) / dest.magnitude_squared()
    return pygame.math.Vector2([ divided * num for num in dest ])

def determinant2x2(y1: list, y2: list):
    return y1[0] * y2[1] - y1[1] * y2[0]

def checkLineIntersection(Ax1y1: list, Ax2y2: list, Bx1y1: list, Bx2y2: list):
    deltaX = (Ax1y1[0] - Ax2y2[0], Bx1y1[0] - Bx2y2[0])
    deltaY = (Ax1y1[1] - Ax2y2[1], Bx1y1[1] - Bx2y2[1])

    div = determinant2x2(deltaX, deltaY)
    if div == 0:
        return False, [0, 0]
    
    d = ( determinant2x2(Ax1y1, Ax2y2), determinant2x2(Bx1y1, Bx2y2) )
    x = determinant2x2(d, deltaX) / div
    y = determinant2x2(d, deltaY) / div

    return True, [x, y]