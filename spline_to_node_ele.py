import numpy as np
from spline_loader.loader import SplineLoader
from node_creator.node_file_creator import NodeEleFileCreator
import plotly.graph_objects as go

def push_to_debug(fig, arr):
    debug = np.array(arr)
    fig.add_trace(go.Scatter3d(
        x=debug[:, 0], 
        y=debug[:, 1], 
        z=debug[:, 2], 
        mode='markers'
    ))

def extract_cuboid_index(i, l, r):
    #    E ----- F  ← top
    #  / |     / |
    # A ----- B  |  ← top
    # |  G ---|- H  ← bottom
    # | /     | /
    # C ----- D     ← bottom
    # ↑       ↑
    # left    right
    bottom = i * 64         # TODO: 64 é a (length das directions x 2)
    top = (i + 1) * 64
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

def create_cuboid(i, l, r):
    nodes = []
    A, B, C, D, E, F, G, H = extract_cuboid_index(i, l, r)
    nodes.append([ A, C, D, G ])
    nodes.append([ A, D, F, G ])
    nodes.append([ D, F, G, H ])
    nodes.append([ A, E, F, G ])
    nodes.append([ A, B, D, F ])
    return nodes

def main() -> None:
    spline = SplineLoader().load('spline_loader/spline.txt')

    cps = spline.get_control_points()
    dps = []
    nodes = []

    fig = go.Figure()
    push_to_debug(fig, cps)

    for i in range(len(cps)):
        cp = cps[i]
        directions = spline.get_direction_points_from_cp(i)
        push_to_debug(fig, directions + cp)

        for direction in directions:
            dps.append(direction + cp)
            dps.append((direction * 1.25) + cp)

    fig.write_html("debug.html")

    directions_len = len(spline.get_direction_points_from_cp(0))
    for i in range(len(cps) - 1):
        for j in range(directions_len - 1):
            nodes.extend(create_cuboid(i, j, j))
        nodes.extend(create_cuboid(i, 0, directions_len - 2))

    creator = NodeEleFileCreator()
    creator.create_node(np.array(dps), "colon")
    creator.create_ele(np.array(nodes), "colon")

if __name__ == "__main__":
    main()