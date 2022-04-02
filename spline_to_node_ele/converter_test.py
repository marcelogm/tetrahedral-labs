import unittest
import numpy as np
from unittest.mock import patch
from spline_loader.loader import Spline
from node_creator.node_file_creator import NodeEleFileCreator
from spline_to_node_ele.converter import Converter


class ConverterTest(unittest.TestCase):

    @patch('node_creator.node_file_creator.NodeEleFileCreator')
    def test_converter_spline_to_tet_mesh(self, fileCreator: NodeEleFileCreator):
        # given
        spline = Spline(np.array([
            [0, 0, 1],
            [0, 0, 2]
        ]), np.array([
            [1, 0, 0],
            [0, 1, 0],
            [-1, 0, 0],
            [0, -1, 0],
            [1, 0, 0],
            [0, 1, 0],
            [-1, 0, 0],
            [0, -1, 0]
        ]))
        converter = Converter(fileCreator)

        # when
        converter.apply(spline, 1.2)

        # then

        self.assertTrue(np.allclose(
            self.__get_expected_vertices(),
            fileCreator.create_node.call_args[0][0]
        ))
        self.assertTrue(np.allclose(
            self.__get_expected_tet_structures(),
            fileCreator.create_ele.call_args[0][0]
        ))
        self.assertEqual('colon', fileCreator.create_node.call_args[0][1])
        self.assertEqual('colon', fileCreator.create_ele.call_args[0][1])

    def __get_expected_vertices(self):
        return [
            [1, 1, 2],
            [1.2, 1.2, 2.2],
            [0, 0, 1],
            [0., 0., 1.],
            [0, 0, 1],
            [0., 0., 1.],
            [0, 0, 2],
            [0., 0., 2.],
            [1, 1, 3],
            [1.2, 1.2, 3.2],
            [0, 0, 2],
            [0., 0., 2.]
        ]

    def __get_expected_tet_structures(self):
        return [
            [0, 64, 66, 65],
            [0, 66,  3, 65],
            [66,  3, 65, 67],
            [0,  1,  3, 65],
            [0,  2, 66,  3],
            [2,  4, 66,  3],
            [66,  3, 67, 69],
            [4, 66, 68, 69],
            [4, 66,  3, 69],
            [4,  3,  5, 69],
            [0, 64, 68, 65],
            [0, 68,  5, 65],
            [68,  5, 65, 69],
            [0,  1,  5, 65],
            [0,  4, 68,  5]
        ]
