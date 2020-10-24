from dataclasses import dataclass
import math
import numpy as np
import openseespy.opensees as ops

from opsel.base import (
    compare_coord, compare_coord_max, compare_coord_min, cartesian_to
)

@dataclass
class Node:
    x: float
    y: float
    z: float = 0
    id: int = 1

    def coord(self):
        return [self.x, self.y, self.z]

    def vector_to(self, point):
        if isinstance(point, Node):
            return [point.x - self.x, point.y - self.y, point.z - self.z]
        elif any(isinstance(point, t) for t in [tuple, list]):
            return [point[0] - self.x, point[1] - self.y, point[2] - self.z]
        raise ValueError("Incorrect point")


@dataclass
class Nodes:
    array: list

    def __post_init__(self):
        self.n = len(self.array)

    def ids(self):
        return [n.id for n in self.array]

    def x(self):
        return [n.x for n in self.array]

    def y(self):
        return [n.y for n in self.array]

    def z(self):
        return [n.z for n in self.array]

    def get(self, i):
        return self.array[i]

    def center(self):
        return Node(
            x=sum(self.x())/self.n,
            y=sum(self.y())/self.n,
            z=sum(self.z())/self.n)

    def __add__(self, node):
        if isinstance(node, Node):
            return Nodes(self.array + [node])
        if isinstance(node, Nodes):
            return Nodes(self.array + node.array)
        raise ValueError("Incorrect type")

    def __iter__(self):
        return iter(self.array)

    


def sort(nodes: Nodes, clockwise: bool = False):
    """ 
    Sort the nodes of a convex polygon
    """
    # Interior point of the polygon
    if nodes.n < 3:
        raise ValueError("The list should have at least 3 nodes")
    center = nodes.center()

    # First point taken as a reference
    ref = nodes.get(0).coord()

    # Axis
    normal = np.cross(ref, nodes.get(1).coord())
    normal = normal / math.hypot(*normal)
    xaxis = np.subtract(ref, center.coord())
    xaxis = xaxis / math.hypot(*xaxis)
    yaxis = np.cross(xaxis, normal)

    # Angles of each point in the defined x and y axes
    pi2 = math.pi * 2
    angles = [math.atan2(
        np.dot(yaxis, center.vector_to(n)),
        np.dot(xaxis, center.vector_to(n))) % pi2
        for n in nodes]

    # Sort counter clockwise or clockwise
    sorted_indeces = np.argsort(angles)
    if clockwise:
        # TODO first node equal to the fist node passed, then sort clockwise
        sorted_indeces = np.flip(sorted_indeces)

    return Nodes([nodes.get(i) for i in sorted_indeces])


def by_location(
    x: float = None, xmin: float = None, xmax: float = None, 
    y: float = None, ymin: float = None, ymax: float = None, 
    z: float = None, zmin: float = None, zmax: float = None,
    system: str = "cartesian", origin: tuple = (0, 0, 0), rotation: tuple = (0, 0, 0),
    seltol: float = 1e-7
):
    """
    Returns a list of nodes filtered by location in a local system of reference
    given by the arguments system, origin and rotation.

    Keyword arguments:
    filter locations: x, xmin, xmax, y, ymin, ymax, z, zmin, zmax
    system -- string with the name of the coordinate system "cartesian" or "cylindrical"
    origin -- tuple with the global cartesian coordinates of the local system of reference's origin
    rotation -- tuple with the rotation angles in radians of the local system of reference
    seltol -- float with the selection tolerance

    Examples:
    nodes.by_location(x=0)
    nodes.by_location(ymin=8, ymax=13)
    nodes.by_location(x=0, ymin=-1, zmax=13)
    """

    conditions = []
    if system == "cylindrical":
        #x, xmin, xmax, y, ymin, ymax, z, zmin, zmax = tuple([])
        pass

    if x is not None:
        conditions.append(lambda c: compare_coord(loc=x, coord=c[0], seltol=seltol))
    if xmin is not None:
        conditions.append(lambda c: compare_coord_min(loc=xmin, coord=c[0], seltol=seltol))
    if xmax is not None:
        conditions.append(lambda c: compare_coord_max(loc=xmax, coord=c[0], seltol=seltol))

    if y is not None:
        conditions.append(lambda c: compare_coord(loc=y, coord=c[1], seltol=seltol))
    if ymin is not None:
        conditions.append(lambda c: compare_coord_min(loc=ymin, coord=c[1], seltol=seltol))
    if ymax is not None:
        conditions.append(lambda c: compare_coord_max(loc=ymax, coord=c[1], seltol=seltol))

    if z is not None:
        conditions.append(lambda c: compare_coord(loc=z, coord=c[2], seltol=seltol))
    if zmin is not None:
        conditions.append(lambda c: compare_coord_min(loc=zmin, coord=c[2], seltol=seltol))
    if zmax is not None:
        conditions.append(lambda c: compare_coord_max(loc=zmax, coord=c[2], seltol=seltol))

    return [
        n for n in ops.getNodeTags() 
        if all(
            condition(
                cartesian_to(
                    point=ops.nodeCoord(n), 
                    system=system, 
                    origin=origin,
                    rotation=rotation
                    )
                ) for condition in conditions
            )
        ]