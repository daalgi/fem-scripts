from dataclasses import dataclass
import math
import numpy as np
import openseespy.opensees as ops

from opsel.base import (
    compare_coord, compare_coord_max, compare_coord_min, cartesian_to
)


@dataclass
class Node:
    x: float = 0
    y: float = 0
    z: float = 0
    id: int = 1

    def coord(self, numpyArray=False):
        if numpyArray:
            return np.array([self.x, self.y, self.z])
        return [self.x, self.y, self.z]

    def vector_to(self, point):
        if isinstance(point, Node):
            return [point.x - self.x, point.y - self.y, point.z - self.z]
        elif any(isinstance(point, t) for t in [tuple, list]):
            return [point[0] - self.x, point[1] - self.y, point[2] - self.z]
        raise ValueError("Incorrect point")


@dataclass
class Nodes:
    array: list = None

    def __post_init__(self):
        self.n = len(self.array) if self.array is not None else 0
        if self.n == 0:
            self.array = []

    def ids(self):
        return [n.id for n in self.array]

    def coords(self, numpyArray=False):
        return [n.coords(numpyArray) for n in self.array]

    def x(self):
        return [n.x for n in self.array]

    def y(self):
        return [n.y for n in self.array]

    def z(self):
        return [n.z for n in self.array]

    def xmin(self):
        return min(self.x()) if self.n > 0 else None

    def xmax(self):
        return max(self.x()) if self.n > 0 else None

    def ymin(self):
        return min(self.y()) if self.n > 0 else None

    def ymax(self):
        return max(self.y()) if self.n > 0 else None

    def zmin(self):
        return min(self.z()) if self.n > 0 else None

    def zmax(self):
        return max(self.z()) if self.n > 0 else None
    
    def get(self, i):
        return self.array[i]

    def center(self):
        return Node(
            x=sum(self.x())/self.n,
            y=sum(self.y())/self.n,
            z=sum(self.z())/self.n)

    def append(self, node):
        if isinstance(node, Node):
            self.array.append(node)
        raise ValueError("Incorrect type")

    def __add__(self, other):
        """
        if isinstance(other, int):
            return Nodes(self.array + [Node(other)])
        elif isinstance(other, list):
            if all(isinstance(o, int) for o in other):
                return Nodes(self.array + [Node(n) for n in other])
        """
        if isinstance(other, Node):
            return Nodes(self.array + [other])
        elif isinstance(other, Nodes):
            return Nodes(self.array + other.array)
        raise ValueError("Incorrect type")

    def __sub__(self, other):
        if isinstance(other, int):
            return Nodes([n for n in self.array if n.id != other])
        elif isinstance(other, list):
            if all(isinstance(o, int) for o in other):
                return Nodes([n for n in self.array if n.id not in other])
        elif isinstance(other, Node):
            return Nodes([n for n in self.array if n.id != other.id])
        elif isinstance(other, Nodes):
            return Nodes([n for n in self.array if n.id not in other.ids()])
        raise ValueError("Incorrect type")

    def __iter__(self):
        return iter(self.array)

    def filter_by_location(self, 
        x: float = None, xmin: float = None, xmax: float = None, 
        y: float = None, ymin: float = None, ymax: float = None, 
        z: float = None, zmin: float = None, zmax: float = None,
        origin: tuple = (0, 0, 0), 
        rotation_axis: tuple = (0, 0, 0),
        rotation_angle: float = 0,
        system: str = "cartesian",
        seltol: float = 1e-7
    ):
        return by_location(
            x=x, xmin=xmin, xmax=xmax, 
            y=y, ymin=ymin, ymax=ymax, 
            z=z, zmin=zmin, zmax=zmax,
            node_list=self,
            origin=origin, 
            rotation_axis=rotation_axis, 
            rotation_angle=rotation_angle,
            system=system,
            seltol= seltol
        )

    def sort(self, 
        counterclockwise: bool = True, 
        clockwise: bool = False,
        x: bool = False,
        y: bool = False,
        z: bool = False
    ):
        # TODO develop and test
        pass


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
    normal = normal / np.linalg.norm(normal)
    xaxis = np.subtract(ref, center.coord())
    xaxis = xaxis / np.linalg.norm(xaxis)
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
    node_list: list = None,
    origin: tuple = (0, 0, 0), 
    rotation_axis: tuple = (0, 0, 0),
    rotation_angle: float = 0,
    system: str = "cartesian",
    seltol: float = 1e-7
):
    """
    Returns a list of nodes filtered by location in a local system of reference
    given by the arguments system, origin and rotation.

    Keyword arguments:
    filter locations in the local system: x, xmin, xmax, y, ymin, ymax, z, zmin, zmax
    system -- string with the name of the coordinate system "cartesian" or "cylindrical"
    origin -- tuple with the global cartesian coordinates of the local system of reference's origin
    rotation -- tuple with the rotation angles in radians of the local system of reference
    seltol -- float with the selection tolerance
    
    returns -- an instance of Nodes, containing the filtered nodes.

    Examples:
    nodes.by_location(x=0)
    nodes.by_location(ymin=8, ymax=13)
    nodes.by_location(x=0, ymin=-1, zmax=13)
    """

    conditions = []
    # TODO cylindrical coordinate system
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

    
    if isinstance(node_list, Nodes):
        # If the node_list is an instance of Nodes
        # it's assumed that the coordinates are stored,
        # so no need to retrieve them from ops.nodeCoord
        # TODO test speed of both approaches

        # Return an instance of Nodes with the filtered nodes
        return Nodes([n for n in node_list
            if all(
                condition(
                    cartesian_to(
                        point=n.coord(), 
                        system=system, 
                        origin=origin,
                        rotation_axis=rotation_axis,
                        rotation_angle=rotation_angle
                        )
                    ) for condition in conditions
                )
            ])    

    # If node_list is None, get the node tags from the model
    if node_list is None:
        node_list = ops.getNodeTags()

    # Return an instance of Nodes with the filtered nodes
    return Nodes([
        Node(*ops.nodeCoord(n), id=n) 
        for n in node_list
        if all(
            condition(
                cartesian_to(
                    point=ops.nodeCoord(n), 
                    system=system, 
                    origin=origin,
                    rotation_axis=rotation_axis,
                    rotation_angle=rotation_angle
                    )
                ) for condition in conditions
            )
        ])