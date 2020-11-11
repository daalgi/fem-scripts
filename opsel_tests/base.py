import os, sys, math
sys.path.append('.\\')
from dataclasses import dataclass

import pygmsh
import openseespy.opensees as ops

import opsel.nodes
import opsel.elements
from opsel.nodes import Node, Nodes


@dataclass
class CantileverBeam:
    length: float = 10
    width: float = 0.3
    height: float = 0.8
    pressure: float = 10    # kPa
    elastic_modulus: float = 30e6 # kPa
    poisson_ratio: float = 0.2

    def __post_init__(self):
        self.area = self.width * self.height
        self.inertia = self.width * self.height ** 3 / 12
        
        # Reactions
        self.reaction_fz = self.pressure * self.width * self.length
        self.reaction_mx = self.pressure * self.width * self.length ** 2 / 2
        
        # Maximum vertical displacement
        vmax = 1.5 * self.pressure * self.length ** 4
        vmax /= self.elastic_modulus * self.height ** 3
        self.vmax = vmax


def init_2d_beam_model(
    beam: CantileverBeam = CantileverBeam(), 
    elem_max_size=0.2
):

    # Initialize ops model
    ops.wipe()
    ops.model('Basic', '-ndm', 2, '-ndf', 2)
    coordTransf = "Linear"  # Linear, PDelta, Corotational
    massType = "-lMass"  # -lMass, -cMass

    # Generate the mesh
    num_nodes_horizontal = int(math.ceil(beam.length // elem_max_size) + 1)
    num_nodes_vertical = int(math.ceil(beam.height / elem_max_size) + 1)

    with pygmsh.geo.Geometry() as geom:   
        geom.characteristic_length_max = elem_max_size

        points = [geom.add_point((0, 0, 0), mesh_size=1)]
        points += [geom.add_point((beam.length, 0, 0), mesh_size=1)]
        points += [geom.add_point((beam.length, beam.height, 0), mesh_size=1)]
        #points += [geom.add_point((beam.length, 0, beam.height), mesh_size=1)]
        points += [geom.add_point((0, beam.height, 0), mesh_size=1)]
        #points += [geom.add_point((0, 0, beam.height), mesh_size=1)]
        
        lines = [geom.add_line(points[i-1], points[i]) for i in [1, 2, 3, 0]]

        cloop = geom.add_curve_loop(lines)
        surface = geom.add_plane_surface(cloop)

        for i, line in enumerate(lines):
            num_nodes = num_nodes_horizontal if i % 2 == 0 else num_nodes_vertical
            geom.set_transfinite_curve(line, num_nodes, "Progression", 1)
        
        geom.set_transfinite_surface(surface, "Left", [])
                
        # Mesh
        geom.set_recombined_surfaces([surface])
        mesh = geom.generate_mesh()

        # Convert to opensees mesh
        # Nodes
        for i, point in enumerate(mesh.points):
            ops.node(i+1, *point[:-1])
        
        # Material
        matTag = 1
        ops.nDMaterial('ElasticIsotropic', matTag, beam.elastic_modulus, beam.poisson_ratio)
        
        # Elements
        quad = [c for c in mesh.cells if c.type == "quad"][0].data
        for i, nodes in enumerate(quad):
            eleTag = i + 1
            eleNodes = [int(n) + 1 for n in nodes]
            #ops.element('quad', eleTag, *eleNodes, h, 'PlaneStress', matTag, 0, rho)
            ops.element('quad', eleTag, *eleNodes, beam.width, 'PlaneStress', matTag)
                