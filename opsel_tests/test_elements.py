import unittest

import openseespy.opensees as ops

from opsel.nodes import Node, Nodes
from opsel.elements import Element, Elements

from .base import init_2d_beam_model


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