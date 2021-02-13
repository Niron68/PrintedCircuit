from math import *

class Graphe:
    def __init__(self, list):
        self.edges = [e for e in list]
        self.mat = {}
        for edge in self.edges:
            line = {}
            for e in self.edges:
                line[e] = Graphe.get_distance(e, edge)
            self.mat[edge] = line
        print(self.mat)


    def get_distance(first, second):
        delta_x = abs(first[0] - second[0])
        delta_y = abs(first[1] - second[1])
        return sqrt((delta_x*delta_x)+(delta_y*delta_y))


    def get_distance_chemin(list):
        total = 0
        previous = ""
        for point in list:
            if previous != "":
                total += Graphe.get_distance(previous, point)
                previous = point
            else:
                previous = point


    def get_chemin(self):
        pass
