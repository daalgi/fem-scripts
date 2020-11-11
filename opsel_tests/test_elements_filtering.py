import unittest

import openseespy.opensees as ops

import opsel.elements

from .base import init_2d_beam_model


class TestFiltering(unittest.TestCase):
    def setUp(self):
        init_2d_beam_model()
        # element1 node ids = [1, 5, 107, 106]

    def test_composed_by_nodes(self):        
        nodes = [1, 5, 107, 106]
        e = opsel.elements.composed_by_nodes(nodes)
        self.assertIsInstance(e, opsel.elements.Elements)
        self.assertEqual(e.n, 1)
        self.assertIsInstance(e.get(0), opsel.elements.Element)
        self.assertEqual(e.get(0).id, 1)

    def test_containing_nodes(self):
        nodes = [1]
        e = opsel.elements.containing_nodes(nodes)
        self.assertIsInstance(e, opsel.elements.Elements)
        self.assertEqual(e.n, 1)
        self.assertIsInstance(e.get(0), opsel.elements.Element)
        self.assertEqual(e.get(0).id, 1)

        nodes = [5]
        e = opsel.elements.containing_nodes(nodes)
        self.assertIsInstance(e, opsel.elements.Elements)
        self.assertEqual(e.n, 2)
        self.assertIsInstance(e.get(0), opsel.elements.Element)
        self.assertEqual(e.get(0).id, 1)
        self.assertIsInstance(e.get(1), opsel.elements.Element)
        self.assertEqual(e.get(1).id, 5)    