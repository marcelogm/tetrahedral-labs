import unittest
import numpy as np
from load_spline.loader import SplineLoader

class SplineLoaderTest(unittest.TestCase):

    def test_must_load_spline_file(self):
        # when
        spline = SplineLoader().load("load_spline/spline.txt")

        # then
        self.assertTrue(len(spline.get_control_points()) > 0)

    def test_must_raise_exception_on_invalid_file_format(self):
        with self.assertRaisesRegex(Exception, 'Não foi possível extrair pontos do arquivo load_spline/not_spline.txt'):
            SplineLoader().load("load_spline/not_spline.txt")
            
    def test_must_extract_all_control_points(self):
        # when
        spline = SplineLoader().load("load_spline/spline.txt")

        # then
        control_points = spline.get_control_points()
        self.assertTrue(len(control_points) == 112)
        
        # and: first control point
        self.assertTrue(np.allclose(control_points[0], [ -0.02821, 0.04348, -0.19054]))

        # and: extract the next one
        self.assertTrue(np.allclose(control_points[1], [ -0.02821, 0.04348, -0.18054 ]))

    def test_must_extract_all_direction_points(self):
        # when
        spline = SplineLoader().load("load_spline/spline.txt")

        # then
        directions = spline.get_direction_points_from_cp(0)
        self.assertTrue(len(directions) == 32)

        # and
        self.assertTrue(np.allclose(directions[0], [ 0.0008440465, -0.004397966, 0 ]))
        self.assertTrue(np.allclose(directions[-1], [ -2.93646E-05, -0.0043584, 0 ]))