from math import *

class PrintedCircuit:


    def __init__(self, coord_table = []):
        self.coord_table = coord_table
        self.angle = 0
        self.growth = 1


    def getRelativeCoord(self):
        res = []
        min_x = abs(min(self.coord_table)[0])
        min_y = abs(min(self.coord_table, key = lambda t: t[1])[1])
        for coord in self.coord_table:
            res.append((coord[0] + min_x, coord[1] + min_y))
        if min(res)[0] != 0 or min(res, key= lambda t: t[1])[1] != 0:
            min_x = min(res)[0]
            min_y = min(res, key= lambda t: t[1])[1]
            old_res = res
            res = [(coord[0] - min_x, coord[1] - min_y) for coord in old_res]
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
        min_percent_x = abs(min(percent_coord)[0])
        min_percent_y = abs(min(percent_coord, key= lambda t: t[1])[1])
        max_percent_x = max(percent_coord)[0]
        max_percent_y = max(percent_coord, key= lambda t: t[1])[1]
        if max_percent_x > 1 or max_percent_y > 1:
            res = []
            for coord in percent_coord:
                x_percent = (coord[0] + min_percent_x) / (max_percent_x + min_percent_x)
                y_percent = (coord[1] + min_percent_y) / (max_percent_y + min_percent_y)
                res.append((x_percent, y_percent))
            return res
        else:
            return percent_coord


    def invertPercentCoord(self, coord_table, x = False, y = True):
        return [(1 - coord[0] if x else coord[0], 1 - coord[1] if y else coord[1]) for coord in coord_table]


    def getDistance(first, second):
        delta_x = abs(first[0] - second[0])
        delta_y = abs(first[1] - second[1])
        return sqrt((delta_x*delta_x)+(delta_y*delta_y))


    def getCorner(self):
        coord_table = self.getRelativeCoord()
        min_corner = (min(coord_table)[0], min(coord_table, key= lambda t: t[1])[1])
        max_corner = (max(coord_table)[0], max(coord_table, key= lambda t: t[1])[1])
        min_distance_list = [PrintedCircuit.getDistance(coord, min_corner) for coord in coord_table]
        max_distance_list = [PrintedCircuit.getDistance(coord, max_corner) for coord in coord_table]
        return [coord_table[min_distance_list.index(min(min_distance_list))], coord_table[max_distance_list.index(min(max_distance_list))]]


    def getCorner2(self):
        coord_table = self.getRelativeCoord()
        min_corner = (min(coord_table)[0], min(coord_table, key= lambda t: t[1])[1])
        max_corner = (max(coord_table)[0], max(coord_table, key= lambda t: t[1])[1])
        min_distance_list = [PrintedCircuit.getDistance(coord, min_corner) for coord in coord_table]
        max_distance_list = [PrintedCircuit.getDistance(coord, max_corner) for coord in coord_table]
        return [coord_table[min_distance_list.index(min(min_distance_list))], coord_table[max_distance_list.index(min(max_distance_list))]]


    def rotate_point(origin, angle, point):
        radiant_angle = angle * (pi/180)
        delta_x = point[0] - origin[0]
        delta_y = point[1] - origin[1]
        x = delta_x * cos(radiant_angle) + delta_y * sin(radiant_angle) + origin[0]
        y = - delta_x * sin(radiant_angle) + delta_y * cos(radiant_angle) + origin[1]
        return (x, y)


    def get_angle2(a, b, c):
        ab_vector = (b[0] - a[0], b[1] - c[1])
        ac_vector = (c[0] - a[0], c[1] - a[1])
        ab = sqrt((ab_vector[0] * ab_vector[0]) + (ab_vector[1] * ab_vector[1]))
        ac = sqrt((ac_vector[0] * ac_vector[0]) + (ac_vector[1] * ac_vector[1]))
        cosbac = ((ab_vector[0] * ac_vector[0]) + (ab_vector[1] * ac_vector[1]))/(ab * ac)
        return acos(cosbac)


    def get_angle(a, b, c):
        angle1 = tan((b[1] - a[1])/(b[0] - a[0]))
        angle2 = tan((c[1] - a[1])/(c[0] - a[0]))
        return degrees(angle2 - angle1)


    def get_growth_factor(a, b, c):
        ab = PrintedCircuit.getDistance(a, b)
        ac = PrintedCircuit.getDistance(a, c)
        return ab / ac


    def get_transformed_coord(self, angle, coord_list = []):
        coord_table = self.getRelativeCoord() if coord_list == [] else coord_list
        return [PrintedCircuit.rotate_point(self.getCorner()[1], angle, coord) for coord in coord_table]


    def get_path_lenght(list):
        total = 0
        prev = ""
        for point in list:
            if prev != "":
                total += PrintedCircuit.getDistance(prev, point)
            prev = point
        return total

    def get_best_sort(list):
        list_x = sorted(list)
        list_y = sorted(list, key=lambda t: t[1])
        all_list = { PrintedCircuit.get_path_lenght(list): list, PrintedCircuit.get_path_lenght(list_x): list_x, PrintedCircuit.get_path_lenght(list_y): list_y }
        return all_list[min(all_list, key=all_list.get)]


    def update_attr(self, angle=False, growth=False):
        if angle:
            self.angle = angle
        if growth:
            self.growth = growth


    def get_correct_coord(self):
        coord_table = self.getRelativeCoord()
        corners = self.getCorner()
        coord_list = [(coord[0] - corners[0][0], coord[1] - corners[0][1]) for coord in coord_table]
        #coord_list = self.get_transformed_coord(self.angle, coord_list=coord_list)
        return PrintedCircuit.get_best_sort([(coord[0] * self.growth, coord[1] * self.growth) for coord in coord_list])