import unittest, math

import openseespy.opensees as ops

from opsel.nodes import Nodes, Node
import opsel.nodes


class TestCartesianCoordSys(unittest.TestCase):

    def setUp(self):
        ops.wipe()
        ops.model('Basic', '-ndm', 3)
        counter = 1
        for i in range(1, 11):
            for j in range(1, 11):
                ops.node(counter, float(i), float(j), float(i*j))
                counter += 1

    def test_by_location_constant(self):
        s = opsel.nodes.by_location(x=1)
        self.assertEqual(len(s.ids()), 10)
        for x in s.x():
            self.assertEqual(x, 1)

    def test_by_location_greater_than(self):
        s = opsel.nodes.by_location(xmin=8)
        self.assertEqual(len(s.ids()), 10*3)
        for x in s.x():
            self.assertGreaterEqual(x, 8)

    def test_by_location_less_than(self):
        s = opsel.nodes.by_location(xmax=8)
        self.assertEqual(len(s.ids()), 10*8)
        for x in s.x():
            self.assertLessEqual(x, 8)

    def test_by_location_combination(self):
        s = opsel.nodes.by_location(xmax=8, ymin=9)
        self.assertEqual(len(s.ids()), 8*2)
        for x, y in zip(s.x(), s.y()):
            self.assertLessEqual(x, 8)        
            self.assertGreaterEqual(y, 9)

    def test_by_location_origin_modified(self):
        s = opsel.nodes.by_location(x=-1, y=-1, origin=(9, 9, 9))
        self.assertEqual(len(s.ids()), 1)
        self.assertEqual(s.x()[0], 8)
        self.assertEqual(s.y()[0], 8)

    def test_nodes_class_filter_by_location_origin_modified(self):
        nodes = Nodes()
        for n in ops.getNodeTags():
            nodes += Node(*ops.nodeCoord(n), id=n)
            
        s = nodes.filter_by_location(x=-1, y=-1, origin=(9, 9, 9))
        self.assertEqual(len(s.ids()), 1)
        self.assertEqual(s.x()[0], 8)
        self.assertEqual(s.y()[0], 8)

    def test_by_location_rotated_system(self):
        # TODO check, not working as expected
        axis = (0, 0, 1)
        angle = math.pi / 2
        s = opsel.nodes.by_location(x=-1, rotation_axis=axis, rotation_angle=angle)
        
        self.assertEqual(len(s.ids()), 10)
        self.assertEqual(s.ids()[0], 1)
        self.assertEqual(s.x()[0], 1)
        self.assertEqual(s.y()[0], 1)
        for x in s.y():
            self.assertEqual(x, 1)
        
    def test_by_location_combination_rotated_system(self):
        # TODO check, not working as expected
        axis = (0, 0, 1)
        angle = math.pi / 2
        s = opsel.nodes.by_location(y=-1, rotation_axis=axis, rotation_angle=angle)
        #print(s)
        # TODO
        """self.assertEqual(len(s.ids()), 10)
        self.assertEqual(s.ids()[0], 1)
        self.assertEqual(s.x()[0], 1)
        self.assertEqual(s.y()[0], 1)
        for x in s.y():
            self.assertEqual(x, 1)
        """