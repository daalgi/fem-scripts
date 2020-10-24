import unittest, math

from opsel.nodes import Node, Nodes, sort


class TestNodesClass(unittest.TestCase):

    def test_add_node(self):
        r = Nodes([
            Node(0, 0)
        ])
        self.assertEqual(r.n, 1)

        s = r + Node(1, 1)
        self.assertEqual(s.n, 2)
    
    def test_add_nodes(self):
        r = Nodes([
            Node(0, 0),
            Node(2, 2)
        ])
        self.assertEqual(r.n, 2)

        s = Nodes([
            Node(1, 1)
        ])
        self.assertEqual(s.n, 1)

        t = r + s
        self.assertEqual(t.n, 3)

    def test_center(self):
        nodes = Nodes([
            Node(+1, -1),
            Node(-1, -1),    
            Node(+1, +1),
            Node(-1, +1)            
        ])
        c = nodes.center()
        self.assertIsInstance(c, Node)
        self.assertEqual(c.coord(), [0, 0, 0])
    
    def test_iter(self):
        nodes = Nodes([
            Node(0, 0),
            Node(2, 2)
        ])
        for node in nodes:
            self.assertIsInstance(node, Node)