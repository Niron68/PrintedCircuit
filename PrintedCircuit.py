from math import *

class PrintedCircuit:


    def __init__(self, coord_table = []):
        self.coord_table = coord_table


    def getRelativeCoord(self):
        res = []
        min_x = abs(min(self.coord_table)[0])
        min_y = abs(min(self.coord_table, key = lambda t: t[1])[1])
        for coord in self.coord_table:
            res.append((coord[0] + min_x, coord[1] + min_y))
        return res


    def getCoordInCanvas(self, width = 400, height = 250, coord_list = [], revert = False):
        percent_coord = self.invertPercentCoord(self.getPercentCoord(coord_list=coord_list), x = revert)
        return [(int(coord[0]*(width-20)+10), int(coord[1]*(height-20)+10)) for coord in percent_coord]


    def getPercentCoord(self, coord_list = []):
        coord_table = self.getRelativeCoord() if coord_list == [] else coord_list
        global_coord_table = self.getRelativeCoord()
        percent_coord = []
        max_x = max(global_coord_table)[0]
        max_y = max(global_coord_table, key = lambda t: t[1])[1]
        min_x = min(global_coord_table)[0]
        min_y = min(global_coord_table, key = lambda t: t[1])[1]
        max_percent_x = max_x - min_x
        max_percent_y = max_y - min_y
        for coord in coord_table:
            x_percent = (coord[0] - min_x)/max_percent_x
            y_percent = (coord[1] - min_y)/max_percent_y
            percent_coord.append((x_percent, y_percent))
        return percent_coord


    def invertPercentCoord(self, coord_table, x = False, y = True):
        return [(1 - coord[0] if x else coord[0], 1 - coord[1] if y else coord[1]) for coord in coord_table]


    def getDistance(self, first, second):
        delta_x = abs(first[0] - second[0])
        delta_y = abs(first[1] - second[1])
        return sqrt((delta_x*delta_x)+(delta_y*delta_y))


    def getCorner(self):
        coord_table = self.getRelativeCoord()
        min_corner = (min(coord_table)[0], min(coord_table, key= lambda t: t[1])[1])
        max_corner = (max(coord_table)[0], max(coord_table, key= lambda t: t[1])[1])
        min_distance_list = [self.getDistance(coord, min_corner) for coord in coord_table]
        max_distance_list = [self.getDistance(coord, max_corner) for coord in coord_table]
        return [coord_table[min_distance_list.index(min(min_distance_list))], coord_table[max_distance_list.index(min(max_distance_list))]]


    def rotate_point(self, origin, angle, point):
        radiant_angle = angle * (pi/180)
        delta_x = point[0] - origin[0]
        delta_y = point[1] - origin[1]
        x = delta_x * cos(radiant_angle) + delta_y * sin(radiant_angle) + origin[0]
        y = - delta_x * sin(radiant_angle) + delta_y * cos(radiant_angle) + origin[1]
        return (x, y)


    def get_transformed_coord(self, angle):
        coord_table = self.getRelativeCoord()
        return [self.rotate_point(self.getCorner()[0], angle, coord) for coord in coord_table]