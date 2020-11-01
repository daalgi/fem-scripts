import os, sys, math
sys.path.append('.\\')

import numpy as np

import meshio
import pygmsh
import openseespy.opensees as ops
import openseespy.postprocessing.Get_Rendering as opsplt
import openseespy.postprocessing.ops_vis as opsv
import pyvista as pv

import matplotlib.pyplot as plt

#from select import nodesByLocation
import opsel.nodes
from opsel.nodes import Node, Nodes


def init(output=False):
    # Initialize
    ops.wipe()
    #ops.model('Basic', '-ndm', 2)
    ops.model('Basic', '-ndm', 3, '-ndf', 3)   # For shell elements in 3d
    coordTransf = "Linear"  # Linear, PDelta, Corotational
    #ops.geomTransf(coordTransf, 1)
    massType = "-lMass"  # -lMass, -cMass
    # Save results in ParaView format
    if output:
        if not os.path.exists(output):
            os.makedirs(output)
        ops.recorder('PVD', output, 'disp', 'pressure')


def create_mesh(length, width, height, elem_max_size=0.2):

    num_nodes_horizontal = int(math.ceil(length // elem_max_size) + 1)
    num_nodes_vertical = int(math.ceil(height / elem_max_size) + 1)
    num_nodes_transversal = int(math.ceil(width / elem_max_size) + 1)
    num_div_transversal = num_nodes_transversal - 1
    transversal_elem_size = width / num_nodes_transversal

    with pygmsh.geo.Geometry() as geom:   
        geom.characteristic_length_max = elem_max_size

        points = [geom.add_point((0, 0, 0), mesh_size=1)]
        points += [geom.add_point((length, 0, 0), mesh_size=1)]
        points += [geom.add_point((length, 0, height), mesh_size=1)]
        points += [geom.add_point((0, 0, height), mesh_size=1)]
        
        lines = [geom.add_line(points[i-1], points[i]) for i in [1, 2, 3, 0]]

        cloop = geom.add_curve_loop(lines)
        surface = geom.add_plane_surface(cloop)

        for i, line in enumerate(lines):
            num_nodes = num_nodes_horizontal if i % 2 == 0 else num_nodes_vertical
            geom.set_transfinite_curve(line, num_nodes, "Progression", 1)
        
        geom.set_transfinite_surface(surface, "Left", [])
        geom.extrude(surface, 
            translation_axis=(0, width, 0), 
            num_layers=num_div_transversal, 
            recombine=True)
        
        # Mesh
        geom.set_recombined_surfaces([surface])
        mesh = geom.generate_mesh()
        return mesh


def solve():
    # create SOE
    ops.system("BandSPD")

    # create DOF number
    ops.numberer("RCM")

    # create constraint handler
    ops.constraints("Plain")

    # create integrator
    ops.integrator("LoadControl", 1.0)

    # create algorithm
    ops.algorithm("Linear")

    # create analysis object
    ops.analysis("Static")

    # perform the analysis
    ops.analyze(1)


def run():
    model_name = "cantilever_3dbeam"
    init(output=f'./ops/{model_name}')

    # Create mesh
    file_vtk = '.\\ops\\cantilever_3dbeam.vtk'
    #convert_eol_windows_to_unix(filename)
    height=1#2
    width=0.2
    length=10 
    m = create_mesh(length=length, width=width, height=height, elem_max_size=0.25)
    m.write(file_vtk)
    grid = pv.read(file_vtk)

    # Plot
    #grid.plot(show_axes=True, show_edges=True)

    # Convert to opensees mesh
    # Nodes
    for i, point in enumerate(m.points):
        ops.node(i+1, *point)
    
    # Material
    emod = 30e6
    nu = 0.2
    h = 0.3
    rho = 2.5
    matTag = 1
    ops.nDMaterial('ElasticIsotropic', matTag, emod, nu)
    
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
    pressure = 100
    ops.timeSeries('Linear', 1)
    ops.pattern('Plain', 1, 1)

    load_nodes = opsel.nodes.by_location(z=height)
    current_elem = max(ops.getEleTags()) + 1
    for e in ops.getEleTags():
        ele_nodes = ops.eleNodes(e)
        surface_nodes = Nodes([
            Node(*ops.nodeCoord(n), id=n) 
            for n in ele_nodes if ops.nodeCoord(n)[2] == height
            ])
        if surface_nodes.n > 0:
            # Nodes sorted counterclock-wise
            sorted_nodes = opsel.nodes.sort(surface_nodes)
            #print(sorted_nodes)
            ops.element('SurfaceLoad', current_elem, *sorted_nodes.ids(), +pressure)
            current_elem += 1
    
    # Solution
    loadcase = "DistributedLoad"
    opsplt.createODB(model_name, loadcase)
    solve()

    
    ops.reactions()
    for n in opsel.nodes.by_location(x=0):
        print(ops.nodeReaction(n.id))

    ops.printModel('-file', f'./ops/{model_name}.txt')
    # Post-processing
    res = ''
    res += "\n\nReactions"
    fz = sum([ops.nodeReaction(n.id)[2] for n in opsel.nodes.by_location(x=0)])
    print(sum([ops.nodeReaction(n.id)[0] for n in opsel.nodes.by_location(x=0)]))
    print(sum([ops.nodeReaction(n.id)[1] for n in opsel.nodes.by_location(x=0)]))
    print(sum([ops.nodeReaction(n.id)[2] for n in opsel.nodes.by_location(x=0)]))
    #res += f'{fz*1e3:>8.2f} kN'


    res += "\n\nMaximum vertical displacement"

    # Theoretical maximum vertical displacement
    vmax = 1.5 * pressure * length ** 4 / emod / height ** 3
    res += f'\nTheoretical: {vmax*1e3:>8.4f} mm'

    # Simulation maximum vertical displacement
    vmaxfem = max([abs(ops.nodeDisp(n)[2]) for n in ops.getNodeTags()])
    res += f'\nSimulation:  {vmaxfem*1e3:>8.4f} mm'
    
    print(res)


if __name__ == '__main__':    
    run()