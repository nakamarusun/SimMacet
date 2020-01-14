from shapely.geometry import LineString, Point

line = LineString( [(0, -10), (0, 10)] )
newPoint = Point(1, 1)

print(list(zip(*line.interpolate(line.project(newPoint)).coords.xy))[0])