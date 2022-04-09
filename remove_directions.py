
from spline_loader.loader import Spline, SplineLoader
from spline_to_node_ele.converter import Converter
from node_creator.node_file_creator import NodeEleFileCreator
import numpy as np

def main():
    spline = SplineLoader().load("spline_loader/spline.txt")

    new_directions = []
    for i in range(spline.get_length()):
        new_direction_arr = []
        direction_arr = spline.get_direction_points_from_cp(i)
        for j in range(len(direction_arr)):
            # half spline vectors
            if (j % 2 == 0):
                direction = direction_arr[j]
                new_direction_arr.append(direction)
        new_directions.append(new_direction_arr)
    
    new_spline = Spline(spline.get_control_points(), np.array(new_directions))
    converter = Converter(NodeEleFileCreator())
    converter.apply(new_spline, 1.2)

          
if __name__ == "__main__":
    main()