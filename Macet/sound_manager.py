import shapely.geometry

point = shapely.geometry.Point(1, 1)
line = shapely.geometry.LineString( [(0, 0), (10, 10)] )

print(point.intersection(line))