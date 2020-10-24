import unittest, math

from opsel.nodes import Node, Nodes, sort


class TestSort(unittest.TestCase):

    def test_sort_triangle_counter_clockwise(self):
        nodes = Nodes([
            Node(0, 0),
            Node(10, 0),
            Node(5, 10)
        ])
        s = sort(nodes, clockwise=False)
        self.assertEqual(s.get(0).coord(), [0, 0, 0])
        self.assertEqual(s.get(1).coord(), [10, 0, 0])
        self.assertEqual(s.get(2).coord(), [5, 10, 0])

    def test_sort_triangle_clockwise(self):
        nodes = Nodes([
            Node(0, 0),
            Node(10, 0),
            Node(5, 10)
        ])
        s = sort(nodes, clockwise=True)
        """
        # If first node not altered
        self.assertEqual(s.get(0).coord(), [0, 0, 0])
        self.assertEqual(s.get(1).coord(), [5, 10, 0])
        self.assertEqual(s.get(2).coord(), [10, 0, 0])
        """
        self.assertEqual(s.get(0).coord(), [5, 10, 0])
        self.assertEqual(s.get(1).coord(), [10, 0, 0])
        self.assertEqual(s.get(2).coord(), [0, 0, 0])

    def test_square_counter_clockwise(self):
        nodes = Nodes([
            Node(+1, -1),
            Node(-1, -1),    
            Node(+1, +1),
            Node(-1, +1)            
        ])
        s = sort(nodes, clockwise=False)
        self.assertEqual(s.get(0).coord(), [+1, -1, 0])
        self.assertEqual(s.get(1).coord(), [+1, +1, 0])
        self.assertEqual(s.get(2).coord(), [-1, +1, 0])
        self.assertEqual(s.get(3).coord(), [-1, -1, 0])

    def test_square_clockwise(self):
        nodes = Nodes([
            Node(+1, -1),
            Node(-1, -1),    
            Node(-1, +1),
            Node(+1, +1)
        ])
        s = sort(nodes, clockwise=True)
        """
        # If first node not altered
        self.assertEqual(s.get(0).coord(), [+1, -1, 0])
        self.assertEqual(s.get(1).coord(), [-1, -1, 0])
        self.assertEqual(s.get(2).coord(), [-1, +1, 0])
        self.assertEqual(s.get(3).coord(), [+1, +1, 0])
        """
        self.assertEqual(s.get(0).coord(), [-1, -1, 0])
        self.assertEqual(s.get(1).coord(), [-1, +1, 0])
        self.assertEqual(s.get(2).coord(), [+1, +1, 0])
        self.assertEqual(s.get(3).coord(), [+1, -1, 0])

    def test_8points_square_counter_clockwise(self):
        nodes = Nodes([
            Node(+1, -1),
            Node(-1, -1),    
            Node(-1, +1),
            Node(+1, +1),
            Node(+1, +0),
            Node(-1, +0),
            Node(+0, -1),
            Node(+0, +1)
        ])
        s = sort(nodes, clockwise=False)
        self.assertEqual(s.get(0).coord(), [+1, -1, 0])
        self.assertEqual(s.get(1).coord(), [+1,  0, 0])
        self.assertEqual(s.get(2).coord(), [+1, +1, 0])
        self.assertEqual(s.get(3).coord(), [ 0, +1, 0])
        self.assertEqual(s.get(4).coord(), [-1, +1, 0])
        self.assertEqual(s.get(5).coord(), [-1,  0, 0])
        self.assertEqual(s.get(6).coord(), [-1, -1, 0])
        self.assertEqual(s.get(7).coord(), [ 0, -1, 0])
    