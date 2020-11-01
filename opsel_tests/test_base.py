import unittest, math

from opsel.base import rotate, cartesian_to


DECIMALS = 15

class TestRotate(unittest.TestCase):

    def test_rotate_angle_zero(self):
        p = (0, 1, 0)
        axis = (1, 0, 0)
        angle = 0
        q = rotate(p, axis, angle)
        self.assertNotEqual(p, q)
        self.assertAlmostEqual(q[0], 0, places=DECIMALS)
        self.assertAlmostEqual(q[1], 1, places=DECIMALS)
        self.assertAlmostEqual(q[2], 0, places=DECIMALS)

    def test_rotate_angle_2pi(self):
        p = (0, 1, 0)
        axis = (1, 0, 0)
        angle = 2 * math.pi
        q = rotate(p, axis, angle)
        self.assertNotEqual(p, q)
        self.assertAlmostEqual(q[0], 0, places=DECIMALS)
        self.assertAlmostEqual(q[1], 1, places=DECIMALS)
        self.assertAlmostEqual(q[2], 0, places=DECIMALS)

    def test_rotate_axis_null(self):
        p = (0, 1, 0)
        axis = (0, 0, 0)
        angle = math.pi
        q = rotate(p, axis, angle)
        self.assertNotEqual(p, q)
        self.assertAlmostEqual(q[0], 0, places=DECIMALS)
        self.assertAlmostEqual(q[1], 1, places=DECIMALS)
        self.assertAlmostEqual(q[2], 0, places=DECIMALS)

    def test_rotate_about_x_axis(self):
        p = (0, 1, 0)
        axis = (1, 0, 0)
        angle = math.pi / 2
        q = rotate(p, axis, angle)
        self.assertAlmostEqual(q[0], 0, places=DECIMALS)
        self.assertAlmostEqual(q[1], 0, places=DECIMALS)
        self.assertAlmostEqual(q[2], 1, places=DECIMALS)

    def test_rotate_about_y_axis(self):
        p = (1, 0, 0)
        axis = (0, 1, 0)
        angle = math.pi / 2
        q = rotate(p, axis, angle)
        self.assertAlmostEqual(q[0], 0, places=DECIMALS)
        self.assertAlmostEqual(q[1], 0, places=DECIMALS)
        self.assertAlmostEqual(q[2], -1, places=DECIMALS)

    def test_rotate_about_z_axis(self):
        p = (1, 0, 0)
        axis = (0, 0, 1)
        angle = math.pi / 2
        q = rotate(p, axis, angle)
        self.assertAlmostEqual(q[0], 0, places=DECIMALS)
        self.assertAlmostEqual(q[1], +1, places=DECIMALS)
        self.assertAlmostEqual(q[2], 0, places=DECIMALS)

    def test_rotate_about_random_axis(self):
        p = (1, 0, 0)
        axis = (0, 1, 1)
        angle = math.pi / 2
        q = rotate(p, axis, angle)
        self.assertAlmostEqual(q[0], 0, places=DECIMALS)
        self.assertAlmostEqual(q[1], +1*math.sqrt(2)/2, places=DECIMALS)
        self.assertAlmostEqual(q[2], -1*math.sqrt(2)/2, places=DECIMALS)    


class TestCartesianTo(unittest.TestCase):

    def test_origin_displacement(self):
        p = (8, 8, 8)
        new_origin = (7, 7, 7)
        q = cartesian_to(point=p, origin=new_origin)
        self.assertEqual(q, (1, 1, 1))

    def test_rotation(self):
        p = (1, 0, 0)
        axis = (0, 0, 1)
        angle = math.pi / 2
        q = cartesian_to(point=p, rotation_axis=axis, rotation_angle=angle)
        self.assertAlmostEqual(q[0], 0, places=DECIMALS)
        self.assertAlmostEqual(q[1], 1, places=DECIMALS)
        self.assertAlmostEqual(q[2], 0, places=DECIMALS)

    def test_rotation2(self):
        p = (1, 1, 0)
        axis = (0, 0, 1)
        angle = math.pi / 2
        q = cartesian_to(point=p, rotation_axis=axis, rotation_angle=angle)
        #print(q)
        self.assertAlmostEqual(q[0], -1, places=DECIMALS)
        self.assertAlmostEqual(q[1], +1, places=DECIMALS)
        self.assertAlmostEqual(q[2], 0, places=DECIMALS)