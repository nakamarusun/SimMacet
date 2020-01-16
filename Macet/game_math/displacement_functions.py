# 16 pixel = 30 meters. 

def kmhToPixels(kmh: float) -> float:
    return (kmh / 3.6) * 5.333333

def pixelsToKmh(pixels: float) -> float:
    return pixels * 3.6/5.333333