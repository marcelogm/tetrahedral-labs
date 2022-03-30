import numpy as np
from spline_loader.loader import SplineLoader
from node_creator.node_file_creator import NodeEleFileCreator

#    E ----- F  ← (i + 1)
#  / |     / |
# A ----- B  |  ← (i + 1)
# |  G ---|- H  ← i
# | /     | /
# C ----- D     ← i
# 
# ↑       ↑
# l       r
def extract_cuboid_index(i, l, r):
    A =  (i * 64)       + (l * 2) + 0
    B =  (i * 64)       + (r * 2) + 2
    C = ((i + 1) * 64)  + (l * 2) + 0
    D = ((i + 1) * 64)  + (r * 2) + 2
    E =  (i * 64)       + (l * 2) + 1
    F =  (i * 64)       + (r * 2) + 3
    G = ((i + 1) * 64)  + (l * 2) + 1
    H = ((i + 1) * 64)  + (r * 2) + 3
    return A, B, C, D, E, F, G, H


def main() -> None:
    spline = SplineLoader().load('spline_loader/spline.txt')

    cps = spline.get_control_points()
    dps = []
    for i in range(len(cps)):
        cp = cps[i]
        for dp in spline.get_direction_points_from_cp(i):
            dps.append(dp + cp)
            dps.append((dp * 1.25) + cp)

    nodes = []
    direction_len = len(spline.get_direction_points_from_cp(0))
    for i in range(len(cps) - 1):
        for j in range(direction_len - 1):
            A, B, C, D, E, F, G, H = extract_cuboid_index(i, j, j)
            nodes.append([ A, C, D, G ])
            nodes.append([ A, D, F, G ])
            nodes.append([ D, F, G, H ])
            nodes.append([ A, E, F, G ])
            nodes.append([ A, B, D, F ])

        A, B, C, D, E, F, G, H = extract_cuboid_index(i, 0, direction_len - 2)
        nodes.append([ A, C, D, G ])
        nodes.append([ A, D, F, G ])
        nodes.append([ D, F, G, H ])
        nodes.append([ A, E, F, G ])
        nodes.append([ A, B, D, F ])

    creator = NodeEleFileCreator()
    creator.create_node(np.array(dps), "colon")
    creator.create_ele(np.array(nodes), "colon")

if __name__ == "__main__":
    main()