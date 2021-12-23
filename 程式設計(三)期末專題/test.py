import fiona
from shapely.geometry import shape, Point

collection = fiona.open('./TOWN_MOI_1060525.shp')