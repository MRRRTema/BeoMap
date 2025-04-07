import geopandas as gpd
from shapely.geometry import box
from geopandas.array import from_shapely
import math

center_lat = 44.817
center_lon = 20.457

# Размер одного квадрата (1 км) в градусах
lat_deg_per_km = 1 / 111  # 1° широты ≈ 111 км
lon_deg_per_km = 1 / (111.320 * math.cos(math.radians(center_lat)))  # по долготе — с поправкой

# Размер сетки: 10x10 км
cols = 30
rows = 30

minx = center_lon - (cols / 2) * lon_deg_per_km
maxy = center_lat + (rows / 2) * lat_deg_per_km

grid = []
for i in range(cols):
    for j in range(rows):
        x1 = minx + i * lon_deg_per_km
        y1 = maxy - j * lat_deg_per_km
        x2 = x1 + lon_deg_per_km
        y2 = y1 - lat_deg_per_km
        grid.append(box(x1, y2, x2, y1))

geometry_array = from_shapely(grid, crs="EPSG:4326")
gdf = gpd.GeoDataFrame(geometry=geometry_array)
gdf.to_file("belgrade_grid_1km.geojson", driver="GeoJSON")
