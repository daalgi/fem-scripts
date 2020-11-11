import os, sys, math
sys.path.append('.\\')

import pygmsh
import openseespy.opensees as ops
import openseespy.postprocessing.Get_Rendering as opsplt
import openseespy.postprocessing.ops_vis as opsv
import pyvista as pv

import opsel.nodes
import opsel.elements
from opsel.nodes import Node, Nodes
from base import (
    init, solve, 
    print_vertical_displacements, print_reactions,
    CantileverBeam
)


def create_mesh(beam, elem_max_size=0.2):
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
        return mesh


def run():
    model_name = "2d"
    filename = f'./ops/cantilever_beam/{model_name}'
    init(output=filename, ndm=2, ndf=2)

    # Create mesh
    beam = CantileverBeam()
    m = create_mesh(beam=beam)
    file_vtk = f'{filename}.vtk'
    m.write(file_vtk)
    grid = pv.read(file_vtk)

    # Plot
    #grid.plot(show_axes=True, show_edges=True)

    # Convert to opensees mesh
    # Nodes
    for i, point in enumerate(m.points):
        ops.node(i+1, *point[:-1])
    
    # Material
    matTag = 1
    ops.nDMaterial('ElasticIsotropic', matTag, beam.elastic_modulus, beam.poisson_ratio)
    
    # Elements
    quad = [c for c in m.cells if c.type == "quad"][0].data
    for i, nodes in enumerate(quad):
        eleTag = i + 1
        eleNodes = [int(n) + 1 for n in nodes]
        #ops.element('quad', eleTag, *eleNodes, h, 'PlaneStress', matTag, 0, rho)
        ops.element('quad', eleTag, *eleNodes, beam.width, 'PlaneStress', matTag)
            
    # Boundary conditions
    bc_nodes = opsel.nodes.by_location(x=0)
    for n in bc_nodes.ids():
        ops.fix(n, 1, 1, 1, 1, 1, 1)
    
    # Loading
    load_nodes = opsel.nodes.by_location(y=beam.height)
    current_elem = max(ops.getEleTags()) + 1
    for n in load_nodes:
        #ops.load(n, 0, -beam.pressure)
        #print('\n', n, ops.nodeCoord(n))        
        ops.load(n.id, 0, -beam.pressure * beam.width)# * 0.2)
        #print(n)
    
    # TODO test opsel.elements
    #elem = opsel.elements.composed_by(opsel.nodes.by_location(xmax=5).ids())
    elem = opsel.elements.containing(load_nodes.ids())
    print(elem)
    
    """    
    # Solution
    loadcase = "DistributedLoad"
    opsplt.createODB(model_name, loadcase)
    solve()
    
    # Post-processing
    ops.printModel('-file', f'{filename}.txt')
    print(f'\n{filename}')
    print_vertical_displacements(beam, u_i=1)
    print_reactions(beam, reaction_i=1)
    """

if __name__ == '__main__':    
    run()