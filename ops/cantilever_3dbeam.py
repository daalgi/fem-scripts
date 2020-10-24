import os, sys, math

import numpy as np

import meshio
import pygmsh
import openseespy.opensees as ops
import openseespy.postprocessing.Get_Rendering as opsplt
import openseespy.postprocessing.ops_vis as opsv
import pyvista as pv

import matplotlib.pyplot as plt

from select import nodesByLocation
from utils import convert_eol_windows_to_unix


def init(output=False):
    # Initialize
    ops.wipe()
    #ops.model('Basic', '-ndm', 2)
    ops.model('Basic', '-ndm', 3, '-ndf', 3)   # For shell elements in 3d
    #ops.model('Basic', '-ndm', 2, '-ndf', 2)   # For plane stress in 2d
    coordTransf = "Linear"  # Linear, PDelta, Corotational
    #ops.geomTransf(coordTransf, 1)
    massType = "-lMass"  # -lMass, -cMass
    # Save results in ParaView format
    if output:
        if not os.path.exists(output):
            os.makedirs(output)
        ops.recorder('PVD', output, 'disp')


def create_mesh(length, width, height, elem_max_size=0.5):

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
    m = create_mesh(length=3, width=0.5, height=height, elem_max_size=0.25)
    m.write(file_vtk)
    grid = pv.read(file_vtk)

    # Plot
    #grid.plot(show_axes=True, show_edges=True)

    # Convert to opensees mesh
    # Nodes
    for i, point in enumerate(m.points):
        ops.node(i+1, *point)
    
    # Elements
    emod = 30e6
    nu = 0.2
    h = 0.3
    rho = 2.5
    # Material
    matTag = 1
    ops.nDMaterial('ElasticIsotropic', matTag, emod, nu)
    quad = [c for c in m.cells if c.type == "hexahedron"][0].data
    for i, nodes in enumerate(quad):
        eleTag = i + 1
        eleNodes = [int(n) + 1 for n in nodes]
        ops.element('stdBrick', eleTag, *eleNodes, matTag)
    
    # Boundary conditions
    bc_nodes = nodesByLocation(x=0)
    for n in bc_nodes:
        ops.fix(n, 1, 1, 1, 1, 1, 1)
    
    # Loading
    pressure = 100
    ops.timeSeries('Linear', 1)
    ops.pattern('Plain', 1, 1)
    load_nodes = nodesByLocation(z=height)
    def is_in_surface(coord):
        return coord[2] == height

    

    current_elem = max(ops.getEleTags()) + 1
    for e in ops.getEleTags():
        nodes = ops.eleNodes(e)
        surface_nodes = [n for n in nodes if is_in_surface(ops.nodeCoord(n))]
        if surface_nodes:
            # Nodes sorted counterclock-wise
            #ccw = sorted(surface_nodes, key=lambda k: (k))
            print(surface_nodes, current_elem)
            ops.element('SurfaceLoad', current_elem, *surface_nodes, -pressure)
            current_elem += 1
    
    # Solution
    loadcase = "DistributedLoad"
    opsplt.createODB(model_name, loadcase)
    solve()

    # Post-processing    
    res = ""
    
    """
    for e in ops.getEleTags():
        ni = ops.eleNodes(e)[0]
        res += f'\nNodes: {ops.eleNodes(e)}'
        for index, force in enumerate(ops.eleForce(e)):
            if index % 6 == 0:
                res += f'\nForces Node{index // 6 + 1}: {force:>7.2f} kN'
            elif index % 6 < 3:
                res += f', {force:>7.2f} kN'
            else:
                res += f', {force:>7.2f} kNm'

    print(res)"""
    #opsplt.plot_model("nodes", "elements", Model=model_name)
    
    # - plot model
    #plt.figure()
    #opsv.plot_model()
    #plt.axis('equal')
    
    # - plot deformation
    #plt.figure()
    #opsv.plot_defo()
    # opsv.plot_defo(sfac, unDefoFlag=1, fmt_undefo='g:')
    #plt.axis('equal')
    """
    # get values at OpenSees nodes
    sig_out = opsv.quad_sig_out_per_node()
    print(f'sig_out:\n{sig_out}')"""


if __name__ == '__main__':    
    run()