import math
import numpy as np


def compare_coord(loc: float, coord: float, seltol=1e-7):
    return loc - seltol <= coord <= loc + seltol

def compare_coord_min(loc: float, coord: float, seltol=1e-7):
    return loc - seltol <= coord

def compare_coord_max(loc: float, coord: float, seltol=1e-7):
    return coord <= loc + seltol

def rotate(point: tuple, rotation_axis: tuple = (0, 0, 0), rotation_angle: float = 0):
    """
    Rotation defined by:
    - Its axis: a vector along this axis is unchanged by the rotation.
    - Its angle: the amount of rotation about that axis (Euler rotation theorem).
    """
    rotation_axis_modulus = np.linalg.norm(rotation_axis)

    if rotation_angle % (2 * math.pi) != 0 and rotation_axis_modulus != 0:
        # Rotation matrix from axis and angle
        u = np.asarray(rotation_axis) / rotation_axis_modulus
        c = math.cos(rotation_angle)
        one_minus_c = 1 - c
        s = math.sin(rotation_angle)

        m11 = c + u[0]*u[0]*one_minus_c
        m22 = c + u[1]*u[1]*one_minus_c
        m33 = c + u[2]*u[2]*one_minus_c

        m12 = u[0]*u[1]*one_minus_c - u[2]*s
        m21 = u[0]*u[1]*one_minus_c + u[2]*s

        m13 = u[0]*u[2]*one_minus_c + u[1]*s
        m31 = u[0]*u[2]*one_minus_c - u[1]*s

        m23 = u[1]*u[2]*one_minus_c - u[0]*s
        m32 = u[1]*u[2]*one_minus_c + u[0]*s
        
        rot_matrix = np.array([
            [m11, m12, m13],
            [m21, m22, m23],
            [m31, m32, m33]
        ])
        point = rot_matrix.dot(point)

    return [*point]

def cartesian_to(
    point: tuple, 
    origin: tuple = (0, 0, 0), 
    rotation_axis: tuple = (0, 0, 0),
    rotation_angle: float = 0,
    system: str = "cartesian" 
):
    """
    Transforms the coordinates of a point to a different coordinate system, which can be 
    displaced (given by the origin tuple), 
    rotated (given by the rotation_axis and rotation_angle parameters)
    and/or expressed in cylindrical coordinates (radius, angle, z).
    """    
    # Change the origin of the coordinate system
    if origin != (0, 0, 0):
        point = tuple([p - o for p, o in zip(point, origin)])

    # Rotate the coordinate system
    point = rotate(point, rotation_axis, rotation_angle)
    
    # Change to cylindrical coordinates (radius, angle, z)
    if system.lower() == "cylindrical":
        #TODO
        return point
    
    return [*point]