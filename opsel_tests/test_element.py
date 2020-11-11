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