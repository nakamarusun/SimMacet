from shapely.geometry import LineString, box

def selectRoad(coords: list, roadList: list, radius: int) -> list:
    # If there are any roads in the vicinity of the radius of the coords, return the road, the connected, and the closest coords in the road from coords.
    bounds = box( *[ coords[ i % 2 ] - (radius if i < 2 else -radius) for i in range(4) ] )
    for roads in roadList:
        for connectedRoads in roads.connectedNodes:
            line = LineString( [roads.coords, connectedRoads.coords] )
            boundary = line.intersection(bounds)
            if not boundary.is_empty:
                print(boundary)
                boundary = boundary.boundary
                print(boundary)
                return [ roads, connectedRoads, [ (boundary[0].coords.xy[i][0] + boundary[1].coords.xy[i][0]) / 2 for i in range(2) ] ]