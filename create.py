from spline_loader.loader import SplineLoader
from spline_to_node_ele.converter import Converter
from node_creator.node_file_creator import NodeEleFileCreator

def main():
    spline = SplineLoader().load("spline_loader/spline.txt")
    converter = Converter(NodeEleFileCreator())
    converter.apply(spline, 1.2)

if __name__ == "__main__":
    main()