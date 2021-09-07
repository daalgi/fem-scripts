import math
from dataclasses import dataclass

import pygmsh
import pyvista as pv


FILE_VTK = './meshing/anchors_failure_cone.vtk'

@dataclass
class Cone:
    length: float = 10
    rbot: float = 0.2
    xtop: float = 4 # radius to the top center point in plan view
    ztop: float = 0 # vertical coordinate Z of the top center point
    circumferential_angle: float = 0 # in degrees
    vertical_angle: float = 0 # in degrees
    apex_angle: float = 80 # in degrees

    def __post_init__(self):
        # Circumferential angle (in plan view) trigonometry functions
        anglec_rad = self.circumferential_angle * math.pi / 180
        cosc = math.cos(anglec_rad)
        sinc = math.sin(anglec_rad)

        # Vertical angle (in elevation view) trigonometry functions
        anglev_rad = self.vertical_angle * math.pi / 180
        cosv = math.cos(anglev_rad)
        sinv = math.sin(anglev_rad)

        # Height (vertical projection)
        self.height = self.length * cosv

        # Center point at the bottom
        self.ptop = (
            self.xtop * cosc,
            self.xtop * sinc,
            self.ztop
        )
        self.pbot = (
            self.ptop[0] + self.length * cosc * sinv, 
            self.ptop[1], # + self.length * sinc * cosv, 
            self.ptop[2] - self.height
        )

        # Axis
        self.axis = tuple([t-b for t, b in zip(self.ptop, self.pbot)])        

        # rtop Failure surface
        self.rtop = self.length * math.sin(self.apex_angle / 2 * math.pi / 180)

    def rotate(self, circumferential_angle: float):
        return Cone(
            length=self.length, 
            rbot=self.rbot,
            xtop=self.xtop, 
            ztop=self.ztop,            
            circumferential_angle=circumferential_angle,
            vertical_angle=self.vertical_angle,
            apex_angle=self.apex_angle
        )


@dataclass
class CircleOfCones:
    ref: Cone = Cone()
    num: int = 20

    def __post_init__(self):
        angle = 360 / self.num
        angles = [n * angle for n in range(self.num)]
        self.array = [self.ref.rotate(circumferential_angle=a) for a in angles]

    def get(self, i):
        return self.array[i]


def mesh_circle_of_cones(
    circle_of_cones: list, 
    mesh_length_max: float = 3.5,
    mesh_file: str = None, 
    save_mesh: bool = True
):
    if not all(isinstance(coc, CircleOfCones) for coc in circle_of_cones):
        raise ValueError("circle_of_cones must be a list of CircleOfCones objects")

    if mesh_file is None:
        mesh_file = FILE_VTK

    with pygmsh.occ.Geometry() as geom:
        geom.characteristic_length_max = mesh_length_max

        cones = [
            geom.add_cone(
                center=c.pbot,
                axis=c.axis,
                radius0=c.rbot,
                radius1=c.rtop
            ) 
            for coc in circle_of_cones
            for c in coc.array             
        ]
        
        if len(cones) > 0:
            union = geom.boolean_union(cones)

        mesh = geom.generate_mesh()

        if save_mesh:
            mesh.write(mesh_file)
        
        return mesh


if __name__ == "__main__":
    # Example
    ref_in = Cone(xtop=3.5)
    ref_out = Cone(xtop=5.1)
    num = 10
    circle_of_cones = [
        #CircleOfCones(ref=ref_in, num=num),
        CircleOfCones(ref=ref_out, num=num)
    ]
    mesh = mesh_circle_of_cones(circle_of_cones)
    grid = pv.read(FILE_VTK)
    grid.plot(show_scalar_bar=True, show_axes=False, show_edges=True)
