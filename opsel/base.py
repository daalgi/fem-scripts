def compare_coord(loc: float, coord: float, seltol=1e-7):
    return loc - seltol <= coord <= loc + seltol

def compare_coord_min(loc: float, coord: float, seltol=1e-7):
    return loc - seltol <= coord

def compare_coord_max(loc: float, coord: float, seltol=1e-7):
    return coord <= loc + seltol

def cartesian_to(
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