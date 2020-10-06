import openseespy.opensees as ops
from dataclasses import dataclass


@dataclass
class LocationFilter:
    x: float = None
    xmin: float = None
    xmax: float = None
    y: float = None
    ymin: float = None
    ymax: float = None
    z: float = None
    zmin: float = None
    zmax: float = None


def _location(loc: float, coord: float, seltol=1e-7):
    return loc - seltol <= coord <= loc + seltol

def _locationMin(loc: float, coord: float, seltol=1e-7):
    return loc - seltol <= coord

def _locationMax(loc: float, coord: float, seltol=1e-7):
    return coord <= loc + seltol


def _cartesian_to(
    point: tuple, 
    system: str = "cartesian", 
    origin: tuple = (0, 0, 0), 
    rotation: tuple = (0, 0, 0)
):
    system = system.lower()
    
    # Change the origin of the coordinate system
    point = tuple([p - o for p, o in zip(point, origin)])

    # Rotate the system
    
    if system == "cartesian":
        #TODO
        return point
    elif system == "cylindrical":
        #TODO
        return point
    
    return point
        

def nodesByLocation(
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
    nodesByLocation(x=0)
    nodesByLocation(ymin=8, ymax=13)
    nodesByLocation(x=0, ymin=-1, zmax=13)
    """

    conditions = []
    if system == "cylindrical":
        #x, xmin, xmax, y, ymin, ymax, z, zmin, zmax = tuple([])
        pass

    if x is not None:
        conditions.append(lambda c: _location(loc=x, coord=c[0], seltol=seltol))
    if xmin is not None:
        conditions.append(lambda c: _locationMin(loc=xmin, coord=c[0], seltol=seltol))
    if xmax is not None:
        conditions.append(lambda c: _locationMax(loc=xmax, coord=c[0], seltol=seltol))

    if y is not None:
        conditions.append(lambda c: _location(loc=y, coord=c[1], seltol=seltol))
    if ymin is not None:
        conditions.append(lambda c: _locationMin(loc=ymin, coord=c[1], seltol=seltol))
    if ymax is not None:
        conditions.append(lambda c: _locationMax(loc=ymax, coord=c[1], seltol=seltol))

    if z is not None:
        conditions.append(lambda c: _location(loc=z, coord=c[2], seltol=seltol))
    if zmin is not None:
        conditions.append(lambda c: _locationMin(loc=zmin, coord=c[2], seltol=seltol))
    if zmax is not None:
        conditions.append(lambda c: _locationMax(loc=zmax, coord=c[2], seltol=seltol))

    return [
        n for n in ops.getNodeTags() 
        if all(
            condition(
                _cartesian_to(
                    point=ops.nodeCoord(n), 
                    system=system, 
                    origin=origin,
                    rotation=rotation
                    )
                ) for condition in conditions
            )
        ]