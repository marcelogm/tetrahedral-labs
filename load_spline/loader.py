from io import FileIO
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


def main() -> None:
    spline = SplineLoader().load('load_spline/spline.txt')
    fig = go.Figure()

    cps = spline.get_control_points()
    fig.add_trace(go.Scatter3d(x=cps[:, 0], y=cps[:, 1], z=cps[:, 2]))

    for i in range(len(cps)):
        cp = cps[i]
        dps = spline.get_direction_points_from_cp(i)

        fig.add_trace(go.Scatter3d(
            x=(dps[:, 0] + cp[0]), 
            y=(dps[:, 1] + cp[1]), 
            z=(dps[:, 2] + cp[2])
        ))

    fig.write_html('output.html')

if __name__ == "__main__":
    main()