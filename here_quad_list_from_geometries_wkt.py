import here.geotiles.heretile
import here.geotiles.heretile as heretile
import shapely

with open('thailand_tile_list.txt', 'w') as tile_list_output:
    tile_list_output.write('quadkey\twkt\n')
    with open('thailand.geojson', 'r') as input_geojson:
        lines = input_geojson.readlines()
        for line in lines:
            west, south, east, north = shapely.from_geojson(line).bounds
            level = 12
            tile_list = heretile.in_bounding_box(west=west, south=south, east=east, north=north, level=level)
            for tile in tile_list:
                (tile_west, tile_south, tile_east, tile_north) = heretile.get_bounds(tile)
                tile_polygon = shapely.Polygon.from_bounds(tile_west, tile_south, tile_east, tile_north)
                if shapely.from_geojson(line).intersects(tile_polygon):
                    print(tile.real, tile_polygon.wkt)
                    tile_list_output.write('{}\t{}\n'.format(tile.real, tile_polygon.wkt))
