import unittest
import numpy as np
from node_creator.node_file_creator import NodeEleFileCreator

class NodeEleFileCreatorTest(unittest.TestCase):

    def test_must_create_a_node_file_from_vertices_array(self):
        # given
        filename = "node_creator/output"
        arr = np.array([
            [ 1.0, 2.0, 3.0 ],
            [ 4.0, 5.0, 6.0 ],
            [ 7.0, 8.0, 9.0 ]
        ])

        # when
        NodeEleFileCreator().create_node(arr, filename)

        # then
        file = open(filename + ".node", mode='r')
        self.assertEqual("# Node count, 3 dim, no attribute, no boundary marker\n", file.readline())
        self.assertEqual("3 3 0 0\n", file.readline())
        self.assertEqual("# Node index, node coordinates\n", file.readline())
        self.assertEqual("0 1.000000 2.000000 3.000000\n", file.readline())
        self.assertEqual("1 4.000000 5.000000 6.000000\n", file.readline())
        self.assertEqual("2 7.000000 8.000000 9.000000\n", file.readline())
        file.close()

    def test_must_create_a_ele_file_from_node_array(self):
        # given
        filename = "node_creator/output"
        arr = np.array([
            [ 1, 2, 3, 4, 1 ],
            [ 5, 6, 7, 8, 0 ]
        ])

        # when
        NodeEleFileCreator().create_ele(arr, filename)

        # then
        file = open(filename + ".ele", mode='r')
        self.assertEqual("# Node count, 4 corners, no attribute\n", file.readline())
        self.assertEqual("2 4 1\n", file.readline())
        self.assertEqual("# Node index, corner indexes\n", file.readline())
        self.assertEqual("0 1 2 3 4 1\n", file.readline())
        self.assertEqual("1 5 6 7 8 0\n", file.readline())
        file.close()

    def test_must_create_a_face_file_from_node_array(self):
        # given
        filename = "node_creator/output"
        arr = np.array([
            [ 1, 2, 3 ],
            [ 4, 5, 6 ]
        ])

        # when
        NodeEleFileCreator().create_collision_face_normal(arr, filename)

        # then
        file = open(filename + ".face", mode='r')
        self.assertEqual("# Face count, list of nodes, no attribute \n", file.readline())
        self.assertEqual("2 3 0\n", file.readline())
        self.assertEqual("# Index, node index \n", file.readline())
        self.assertEqual("0 1 2 3\n", file.readline())
        self.assertEqual("1 4 5 6\n", file.readline())
        file.close()
