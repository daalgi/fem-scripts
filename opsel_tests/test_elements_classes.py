import unittest

import openseespy.opensees as ops

from opsel.nodes import Node, Nodes
from opsel.elements import Element, Elements

from .base import init_2d_beam_model


class TestElement(unittest.TestCase):
    def setUp(self):
        init_2d_beam_model()
        self.e = Element(1)
        # element node ids = [1, 5, 107, 106]

    def test_init(self):        
        self.assertEqual(self.e.id, 1)
        self.assertIsInstance(self.e.nodes, Nodes)
        self.assertIsInstance(self.e.nodes.get(0), Node)
        self.assertEqual(self.e.nodes.n, 4)

    def test_nodes_in_list(self):
        nodes = self.e.nodes.ids() + list(range(8, 88))
        self.assertTrue(self.e.nodes_in_list(nodes))

        nodes = [1, 5, 105, 106]
        self.assertFalse(self.e.nodes_in_list(nodes))

        nodes = [1, 5]
        self.assertFalse(self.e.nodes_in_list(nodes))

        nodes = [10, 11]
        self.assertFalse(self.e.nodes_in_list(nodes))

    def test_any_nodes_in_list(self):
        nodes = self.e.nodes.ids() + list(range(8, 88))
        self.assertTrue(self.e.any_node_in_list(nodes))

        nodes = [1, 5, 105, 106]
        self.assertTrue(self.e.any_node_in_list(nodes))

        nodes = [1, 5]
        self.assertTrue(self.e.any_node_in_list(nodes))

        nodes = [10, 11]
        self.assertFalse(self.e.any_node_in_list(nodes))

        
class TestElements(unittest.TestCase):
    def setUp(self):
        init_2d_beam_model()
        self.e = Elements([Element(1), Element(2)])
        # element1 node ids = [1, 5, 107, 106]
        # element2 node ids = [106, 107, 108, 105]
    
    def test_init(self):        
        self.assertEqual(self.e.ids(), [1, 2])

    def test_add(self):
        f = self.e + 3
        self.assertEqual(f.ids(), [1, 2, 3])

        f = self.e + [3]
        self.assertEqual(f.ids(), [1, 2, 3])

        f = self.e + Element(3)
        self.assertEqual(f.ids(), [1, 2, 3])

        f = self.e + Elements([Element(3), Element(8)])
        self.assertEqual(f.ids(), [1, 2, 3, 8])

    def test_subtract(self):
        f = self.e - 1
        self.assertEqual(f.ids(), [2])

        f = self.e - [1]
        self.assertEqual(f.ids(), [2])

        f = self.e - Element(1)
        self.assertEqual(f.ids(), [2])

        f = self.e - Element(2)
        self.assertEqual(f.ids(), [1])

        f = self.e - Element(8)
        self.assertEqual(f.ids(), [1, 2])

    def test_iter(self):
        for elem in self.e:
            self.assertIsInstance(elem, Element)