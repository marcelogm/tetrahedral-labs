import numpy as np
from spline_loader.loader import Spline, SplineLoader
from node_creator.node_file_creator import NodeEleFileCreator
import plotly.graph_objects as go

class Converter:

    def __init__(self, fileCreator: NodeEleFileCreator):
        self.fileCreator = fileCreator

    def apply(self, spline: Spline, volume_modifier = 1.1):
        vertices = self.__extract_vertices(spline, volume_modifier)
        nodes = self.__create_cuboid_structure(spline)

        self.fileCreator.create_node(np.array(vertices), "colon")
        self.fileCreator.create_ele(np.array(nodes), "colon")

    def __extract_vertices(self, spline: Spline, volume_modifier: float):
        vertices = []
        control_points = spline.get_control_points()
        for i in range(spline.get_length()):
            control_point = control_points[i]
            directions = spline.get_direction_points_from_cp(i)
            for direction in directions:
                vertices.append(direction + control_point)
                vertices.append((direction * volume_modifier) + control_point)
        return vertices

    def __create_cuboid_structure(self, spline: Spline):
        nodes = []
        direction_count = spline.get_directions_count()
        count_length = (direction_count * 2)
        for i in range(spline.get_length() - 1):
            for j in range(direction_count - 1):
                nodes.extend(self.__create_cuboid(i, j, j, count_length))
            nodes.extend(self.__create_cuboid(i, 0, direction_count - 2, count_length))
        return nodes

    #    E ----- F  ← top
    #  / |     / |
    # A ----- B  |  ← top
    # |  G ---|- H  ← bottom
    # | /     | /
    # C ----- D     ← bottom
    # ↑       ↑
    # left    right
    def __create_cuboid(self, i, l, r, length):
        nodes = []
        A, B, C, D, E, F, G, H = self.__extract_cuboid_index(i, l, r, length)
        #
        #  Using l   Using i   Using both
        #   __ __     __ __     __ __   
        #  | /|\ |   | /| /|   | /|\ |
        #  |/_|_\|   |/_|/_|   |/_|_\|
        #  | /|\ |   |\ |\ |   |\ | /|
        #  |/_|_\|   |_\|_\|   |_\|/_|
        #
        if (l % 2 == 0):
            # DRY IT
            if (i % 2 == 0):
                nodes.append([ A, D, C, G ])
                nodes.append([ A, B, D, F ])
                nodes.append([ A, F, D, G ])
                nodes.append([ F, E, G, A ])
                nodes.append([ F, G, H, D ])
            else:
                nodes.append([ A, B, C, E ])
                nodes.append([ B, D, C, H ])
                nodes.append([ B, C, E, H ])
                nodes.append([ F, E, H, B ])
                nodes.append([ E, G, H, C ])
        else:
            if (i % 2 == 1):
                nodes.append([ A, D, C, G ])
                nodes.append([ A, B, D, F ])
                nodes.append([ A, F, D, G ])
                nodes.append([ F, E, G, A ])
                nodes.append([ F, G, H, D ])
            else:
                nodes.append([ A, B, C, E ])
                nodes.append([ B, D, C, H ])
                nodes.append([ B, C, E, H ])
                nodes.append([ F, E, H, B ])
                nodes.append([ E, G, H, C ])
        return nodes

    def __extract_cuboid_index(self, i, l, r, length):
        bottom = i * length
        top = (i + 1) * length
        left = (l * 2)
        right = (r * 2)

        A = bottom + left  + 0
        B = bottom + right + 2
        C = top    + left  + 0
        D = top    + right + 2
        E = bottom + left  + 1
        F = bottom + right + 3
        G = top    + left  + 1
        H = top    + right + 3
        return A, B, C, D, E, F, G, H
