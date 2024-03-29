import os, sys, math
sys.path.append('.\\')

import pygmsh
import openseespy.opensees as ops
import openseespy.postprocessing.Get_Rendering as opsplt
import openseespy.postprocessing.ops_vis as opsv
import pyvista as pv

import opsel.nodes
from opsel.nodes import Node, Nodes
from base import (
    init, solve, 
    print_vertical_displacements, print_reactions,
    CantileverBeam
)


def create_mesh(beam, elem_max_size=0.2):
    num_nodes_horizontal = int(math.ceil(beam.length // elem_max_size) + 1)
    num_nodes_vertical = int(math.ceil(beam.height / elem_max_size) + 1)
    num_nodes_transversal = int(math.ceil(beam.width / elem_max_size) + 1)
    num_div_transversal = num_nodes_transversal - 1
    transversal_elem_size = beam.width / num_nodes_transversal

    with pygmsh.geo.Geometry() as geom:   
        geom.characteristic_length_max = elem_max_size

        points = [geom.add_point((0, 0, 0), mesh_size=1)]
        points += [geom.add_point((beam.length, 0, 0), mesh_size=1)]
        points += [geom.add_point((beam.length, 0, beam.height), mesh_size=1)]
        points += [geom.add_point((0, 0, beam.height), mesh_size=1)]
        
        lines = [geom.add_line(points[i-1], points[i]) for i in [1, 2, 3, 0]]

        cloop = geom.add_curve_loop(lines)
        surface = geom.add_plane_surface(cloop)

        for i, line in enumerate(lines):
            num_nodes = num_nodes_horizontal if i % 2 == 0 else num_nodes_vertical
            geom.set_transfinite_curve(line, num_nodes, "Progression", 1)
        
        geom.set_transfinite_surface(surface, "Left", [])
        geom.extrude(surface, 
            translation_axis=(0, beam.width, 0), 
            num_layers=num_div_transversal, 
            recombine=True)
        
        # Mesh
        geom.set_recombined_surfaces([surface])
        mesh = geom.generate_mesh()
        return mesh


def run():
    model_name = "3d"
    filename = f'./ops/cantilever_beam/{model_name}'
    init(output=filename, ndm=3, ndf=3)

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
        ops.node(i+1, *point)
    
    # Material
    matTag = 1
    ops.nDMaterial('ElasticIsotropic', matTag, beam.elastic_modulus, beam.poisson_ratio)
    
    # Elements
    quad = [c for c in m.cells if c.type == "hexahedron"][0].data
    for i, nodes in enumerate(quad):
        eleTag = i + 1
        eleNodes = [int(n) + 1 for n in nodes]
        ops.element('stdBrick', eleTag, *eleNodes, matTag)
            
    # Boundary conditions
    bc_nodes = opsel.nodes.by_location(x=0)
    for n in bc_nodes.ids():
        ops.fix(n, 1, 1, 1, 1, 1, 1)
    
    # Loading
    load_nodes = opsel.nodes.by_location(z=beam.height)
    current_elem = max(ops.getEleTags()) + 1
    for e in ops.getEleTags():
        ele_nodes = ops.eleNodes(e)
        surface_nodes = Nodes([
            Node(*ops.nodeCoord(n), id=n) 
            for n in ele_nodes if ops.nodeCoord(n)[2] == beam.height
        ])
        if surface_nodes.n > 0:
            # Nodes sorted counterclock-wise
            sorted_nodes = opsel.nodes.sort(surface_nodes)
            #print(sorted_nodes)
            ops.element('SurfaceLoad', current_elem, *sorted_nodes.ids(), +beam.pressure)
            current_elem += 1
    
    # Solution
    loadcase = "DistributedLoad"
    opsplt.createODB(model_name, loadcase)
    solve()

    # List element stresses
    for e in ops.getEleTags()[:2]:
        # List of stresses 
        #   len(stress) = n * 6 = 8 * 6 = 48
        #       n = number of nodes in each element
        #       6 = stress components
        stress = ops.eleResponse(e, 'stresses')
        nodes = ops.eleNodes(e)
        print(f'-----------------Stress array: {len(stress)}')
        for s, n in zip(stress, nodes):
            print(s)
    # Post-processing
    #ops.printModel('-file', filename)
    print(f'\n{filename}')
    print_vertical_displacements(beam, u_i=2)
    print_reactions(beam, reaction_i=2)
    

if __name__ == '__main__':    
    run()