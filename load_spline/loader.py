from io import FileIO
from tkinter import E
import plotly.graph_objects as go
import numpy as np

class Spline:
    
    def __init__(self, control_points: np.ndarray, direction_points: np.ndarray) -> None:
        self.__control_points = control_points
        self.__direction_points = direction_points

    def get_control_points(self) -> np.ndarray:
        return self.__control_points
        
    def get_direction_points_from_cp(self, control_point_index) -> np.ndarray:
        return self.__direction_points[control_point_index]

class SplineLoader:

    def load(self, path: str) -> Spline:
        try:
            file = open(path, mode='r')
            return self.__build(file)
        except Exception as ex:
            raise Exception('Não foi possível extrair pontos do arquivo %s' % path, ex) 

    def __build(self, file: FileIO):
        control_points = []
        direction_points = []
        control_point_count, direction_count = self.__get_params(file)

        for i in range(control_point_count):
            cp =  self.__get_point_from_file(file)
            control_points.append(cp)
            direction_from_cp = []
            for j in range(direction_count):
                dp =  self.__get_point_from_file(file)
                direction_from_cp.append(dp)
            direction_points.append(direction_from_cp)

        return Spline(np.array(control_points), np.array(direction_points))

    def __get_params(self, file: FileIO):
        return [ int(param) for param in file.readline().split() if param.isdigit() ]

    def __get_point_from_file(self, file: FileIO):
        coord = [ float(num) for num in file.readline().split() ]
        return np.array([ coord[0], coord[1], coord[2] ])


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

def print_triangles(fig, tet):
    t1 = np.array([ tet[0], tet[1], tet[2], tet[0] ])
    fig.add_trace(go.Scatter3d(
        x=t1[:, 0],
        y=t1[:, 1],
        z=t1[:, 2]
    ))
    
    t2 = np.array([ tet[0], tet[1], tet[3], tet[0] ])
    fig.add_trace(go.Scatter3d(
        x=t2[:, 0],
        y=t2[:, 1],
        z=t2[:, 2]
    ))

    t3 = np.array([ tet[1], tet[2], tet[3], tet[1] ])
    fig.add_trace(go.Scatter3d(
        x=t3[:, 0],
        y=t3[:, 1],
        z=t3[:, 2]
    ))

    t4 = np.array([ tet[2], tet[3], tet[0], tet[2] ])
    fig.add_trace(go.Scatter3d(
        x=t4[:, 0],
        y=t4[:, 1],
        z=t4[:, 2]
    ))


def main() -> None:
    spline = SplineLoader().load('load_spline/spline.txt')
    fig = go.Figure()

    cps = spline.get_control_points()
    fig.add_trace(go.Scatter3d(x=cps[:, 0], y=cps[:, 1], z=cps[:, 2]))

    dps = []
    for i in range(len(cps)):
        cp = cps[i]
        for dp in spline.get_direction_points_from_cp(i):
            dps.append(dp + cp)
            dps.append((dp * 1.25) + cp)

    cubes = []
    for i in range(112):
        cube = []
        cp = cps[i]
        for j in range(32 - 1):
            #    E ----- F  ← (i + 1)
            #  / |     / |
            # A ----- B  |  ← (i + 1)
            # |  G ---|- H  ← i
            # | /     | /
            # C ----- D     ← i
            # 
            # ↑       ↑
            # l       r
            A, B, C, D, E, F, G, H = extract_cuboid_index(i, j, j)

            tet1 = np.array([ dps[A], dps[C], dps[D], dps[G] ])
            tet2 = np.array([ dps[A], dps[D], dps[F], dps[G] ])
            tet3 = np.array([ dps[D], dps[F], dps[G], dps[H] ])
            tet4 = np.array([ dps[A], dps[E], dps[F], dps[G] ])
            tet5 = np.array([ dps[A], dps[B], dps[D], dps[F] ])
            
            print_triangles(fig, tet1)
            print_triangles(fig, tet2)
            print_triangles(fig, tet3)
            print_triangles(fig, tet4)
            print_triangles(fig, tet5)

            #cube = np.array([ 
            #    dps[A], dps[B], dps[C], dps[D],
            #    dps[E], dps[F], dps[G], dps[H]
            #])
            #cubes.append(cube)
            #fig.add_trace(go.Scatter3d(
            #    x=cube[:, 0],
            #    y=cube[:, 1],
            #    z=cube[:, 2]
            #))

        A, B, C, D, E, F, G, H = extract_cuboid_index(i, 0, 30)

        tet1 = np.array([ dps[A], dps[C], dps[D], dps[G] ])
        tet2 = np.array([ dps[A], dps[D], dps[F], dps[G] ])
        tet3 = np.array([ dps[D], dps[F], dps[G], dps[H] ])
        tet4 = np.array([ dps[A], dps[E], dps[F], dps[G] ])
        tet5 = np.array([ dps[A], dps[B], dps[D], dps[F] ])
        
        print_triangles(fig, tet1)
        print_triangles(fig, tet2)
        print_triangles(fig, tet3)
        print_triangles(fig, tet4)
        print_triangles(fig, tet5)
        # A, B, C, D, E, F, G, H = extract_cuboid_index(i, 0, 30)
        # cube = np.array([ 
        #     dps[A], dps[B], dps[C], dps[D],
        #     dps[E], dps[F], dps[G], dps[H]
        # ])
        # fig.add_trace(go.Scatter3d(
        #     x=cube[:, 0],
        #     y=cube[:, 1],
        #     z=cube[:, 2]
        # ))
        # cubes.append(cube)


    fig.write_html('output.html')

if __name__ == "__main__":
    main()