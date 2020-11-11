import unittest, math

import openseespy.opensees as ops

from opsel.nodes import Node, Nodes, sort
import opsel.elements 
from opsel.elements import Element, Elements

from .base import init_2d_beam_model


class TestElement(unittest.TestCase):

    def setUp(self):
        init_2d_beam_model()

    def test_init(self):
        e = Element(1)
        self.assertEqual(e.id, 1)
        self.assertIsInstance(e.nodes, Nodes)
        self.assertIsInstance(e.nodes.get(0), Node)
        self.assertEqual(e.nodes.n, 4)

    def test_nodes_in_list(self):
        e = Element(1)
        # element node ids = [1, 5, 107, 106,]
        
        nodes = e.nodes.ids() + list(range(8, 88))
        self.assertTrue(e.nodes_in_list(nodes))

        nodes = [1, 5, 105, 106]
        self.assertFalse(e.nodes_in_list(nodes))

        nodes = [1, 5]
        self.assertFalse(e.nodes_in_list(nodes))

        nodes = [10, 11]
        self.assertFalse(e.nodes_in_list(nodes))

    def test_any_node_in_list(self):
        e = Element(1)
        # element node ids = [1, 5, 107, 106,]

        nodes = e.nodes.ids() + list(range(8, 88))
        self.assertTrue(e.any_node_in_list(nodes))

        nodes = [1, 5, 105, 106]
        self.assertTrue(e.any_node_in_list(nodes))

        nodes = [1, 5]
        self.assertTrue(e.any_node_in_list(nodes))

        nodes = [10, 11]
        self.assertFalse(e.any_node_in_list(nodes))