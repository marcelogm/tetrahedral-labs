import unittest
import numpy as np
from spline_loader.loader import SplineLoader

class SplineLoaderTest(unittest.TestCase):

    def test_must_load_spline_file(self):
        # given
        spline = SplineLoader().load("spline_loader/spline.txt")

        # expect
        self.assertTrue(len(spline.get_control_points()) > 0)

    def test_must_raise_exception_on_invalid_file_format(self):
        # expect
        with self.assertRaisesRegex(Exception, 'Não foi possível extrair pontos do arquivo spline_loader/not_spline.txt'):
            SplineLoader().load("spline_loader/not_spline.txt")
            
    def test_must_extract_all_control_points(self):
        # given
        spline = SplineLoader().load("spline_loader/spline.txt")

        # when
        control_points = spline.get_control_points()

        # then
        self.assertTrue(len(control_points) == 112)
        self.assertTrue(np.allclose(control_points[0], [ -0.02821, 0.04348, -0.19054]))
        self.assertTrue(np.allclose(control_points[1], [ -0.02821, 0.04348, -0.18054 ]))

    def test_must_extract_all_direction_points(self):
        # given
        spline = SplineLoader().load("spline_loader/spline.txt")

        # when
        directions = spline.get_direction_points_from_cp(0)

        # then
        self.assertTrue(len(directions) == 32)
        self.assertTrue(np.allclose(directions[0], [ 0.0008440465, -0.004397966, 0 ]))
        self.assertTrue(np.allclose(directions[-1], [ -2.93646E-05, -0.0043584, 0 ]))

    def test_must_provide_spline_length_aka_control_points_length(self):
        # given
        spline = SplineLoader().load("spline_loader/spline.txt")

        # when
        size = spline.get_length()

        # then
        self.assertTrue(size == 112)

    def test_must_provide_directions_count(self):
        # given
        spline = SplineLoader().load("spline_loader/spline.txt")

        # when
        size = spline.get_directions_count()

        # then
        self.assertTrue(size == 32)