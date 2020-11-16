from dataclasses import dataclass
from enum import Enum

import numpy as np
import openseespy.opensees as ops

from opsel.nodes import Nodes, Node
from opsel.base import tetrahedron_volume


class ElementType(Enum):
    point: 1
    line: 2
    triangular: 3
    quadrilateral: 4
    tetrahedron: 5
    hexahedron: 6
    

@dataclass
class Element:
    id: int = 1
    shape: ElementType = None

    def __post_init__(self):
        self.nodes = Nodes([Node(*ops.nodeCoord(n), id=n) for n in ops.eleNodes(self.id)])
        self.dim = None
        self.type = None
        self.material = None
        self.section = None
        self.system = None
      
    def nodes_in_list(self, nodes):#: Nodes):
        nodes = nodes_ids(nodes)
        return all(n in nodes for n in self.nodes.ids())

    def any_node_in_list(self, nodes):#: Nodes):
        nodes = nodes_ids(nodes)
        return any(n in nodes for n in self.nodes.ids())

    def volume(self):
        if self.shape is ElementType.tetrahedron:
            # Only valid for elements with nodes at the vertices
            # TODO implement for elements with midside nodes
            if self.nodes.n == 4:
                #https://stackoverflow.com/questions/9866452/calculate-volume-of-any-tetrahedron-given-4-points
                return tetrahedron_volume(*self.nodes.coords(numpyArray=True))

        elif self.shape is ElementType.hexahedron:
            # TODO
            pass
        
        # Not a volumetric element, so zero volume
        return 0

    def centroid(self):
        # Only valid for elements with nodes at the vertices
        # TODO implement for elements with midside nodes
        # TODO test
        return self.nodes.center()


@dataclass
class Elements:
    array: list = None

    """
    TODO:
    - Select elements by material, type, section, centroid location, nodes location,
    - Select nodes belonging to:
        - the elements with a given material
        - the elements with a given section
        - the elements of a given type    
        - a given list of element numbers
    """

    def __post_init__(self):
        self.n = len(self.array) if self.array is not None else 0
        if self.n == 0:
            self.array = []

    def ids(self):
        return [e.id for e in self.array]

    def get(self, i):
        return self.array[i]

    def volume(self):
        # TODO test
        return sum(e.volume() for e in self.array)

    def __add__(self, other):
        if isinstance(other, int):
            return Elements(self.array + [Element(other)])
        elif isinstance(other, list):
            if all(isinstance(o, int) for o in other):
                return Elements(self.array + [Element(e) for e in other])
        elif isinstance(other, Element):
            return Elements(self.array + [other])
        elif isinstance(other, Elements):
            return Elements(self.array + other.array)
        raise ValueError("Incorrect type")

    def __sub__(self, other):
        if isinstance(other, int):
            return Elements([e for e in self.array if e.id != other])
        elif isinstance(other, list):
            if all(isinstance(o, int) for o in other):
                return Elements([e for e in self.array if e.id not in other])
        elif isinstance(other, Element):
            return Elements([e for e in self.array if e.id != other.id])
        elif isinstance(other, Elements):
            return Elements([e for e in self.array if e.id not in other.ids()])
        raise ValueError("Incorrect type")

    def __iter__(self):
        return iter(self.array)
    

def nodes_ids(nodes):
    if isinstance(nodes, Nodes):
        return nodes.ids()
    elif isinstance(nodes, list):
        return nodes
    else:
        raise ValueError("Incorrect argument: nodes must be a list or an instance of Nodes")


def composed_by_nodes(nodes: list, element_list: list = None):
    """
    Returns an instance of Elements containing the filtered elements whose nodes are all included in the given list of nodes.

    Keyword arguments:
    nodes -- list of node numbers
    element_list -- list of element numbers to be filtered. If not defined, all the model elements are considered.
    """
    if element_list is None:
        element_list = ops.getEleTags()

    return Elements([Element(e) 
        for e in element_list 
        if Element(e).nodes_in_list(nodes)])


def containing_nodes(nodes: list, element_list: list = None):
    """
    Returns an instance of Elements containing the filtered elements having at least one node included in the given list of nodes.

    Keyword arguments:
    nodes -- list of node numbers
    element_list -- list of element numbers to be filtered. If not defined, all the model elements are considered.
    """
    if element_list is None:
        element_list = ops.getEleTags()

    return Elements([Element(e) 
        for e in element_list
        if Element(e).any_node_in_list(nodes)])