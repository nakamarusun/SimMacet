import pygame.math

def vec2Projection(source: pygame.math.Vector2, dest: pygame.math.Vector2) -> pygame.math.Vector2:
    # Definition: Source vector is PROJECTED ONTO Dest vector
    divided = source.dot(dest) / dest.magnitude_squared()
    return pygame.math.Vector2([ divided * num for num in dest ])