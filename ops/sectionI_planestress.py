import os, sys

import meshio
import openseespy.opensees as ops
import openseespy.postprocessing.Get_Rendering as opsplt
import openseespy.postprocessing.ops_vis as opsv

import matplotlib.pyplot as plt

from select import nodesByLocation
from utils import convert_eol_windows_to_unix

"""
# Meshio
m.points -- list of node coordinates
m.cells -- list of CellBlock (elements)
m.cells[0].type -- type of cell: 'line', 'triangle', ...
m.cells[0].data -- cell nodes number (first node is zero, not one)
"""


def init(output=False):
    # Initialize
    ops.wipe()
    #ops.model('Basic', '-ndm', 2)
    #ops.model('Basic', '-ndm', 3)   # For shell elements in 3d
    ops.model('Basic', '-ndm', 2, '-ndf', 2)   # For plane stress in 2d
    coordTransf = "Linear"  # Linear, PDelta, Corotational
    #ops.geomTransf(coordTransf, 1)
    massType = "-lMass"  # -lMass, -cMass
    # Save results in ParaView format
    if output:
        if not os.path.exists(output):
            os.makedirs(output)
        ops.recorder('PVD', output, 'disp')


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


if __name__ == '__main__':
    
    model_name = "sectionI_planestress"
    init(output=f'./ops/{model_name}')

    # Import mesh
    filename = '.\\ops\\sectionI.msh'
    convert_eol_windows_to_unix(filename)
    m = meshio.read(filename=filename)

    # Convert to opensees mesh
    # Nodes
    for i, point in enumerate(m.points):
        ops.node(i+1, *point)

    # Elements
    emod = 30e6
    nu = 0.2
    h = 0.3
    rho = 2.5
    # Section
    secTag = 1
    ops.section('ElasticMembranePlateSection', secTag, emod, nu, h, rho)
    # Material
    matTag = 1
    ops.nDMaterial('ElasticIsotropic', matTag, emod, nu)
    quad = [c for c in m.cells if c.type == "quad"][0].data
    for i, nodes in enumerate(quad):
        eleTag = i + 1
        eleNodes = [int(n) + 1 for n in nodes]        
        #element('ShellMITC4', eleTag, *eleNodes, secTag)
        #ops.element('ShellMITC4', eleTag, *eleNodes, secTag)
        #ops.element('quad', eleTag, *eleNodes, h, 'PlaneStress', matTag, 0, rho)
        ops.element('quad', eleTag, *eleNodes, h, 'PlaneStress', matTag)

    
    # Boundary conditions
    bc_nodes = nodesByLocation(x=-0.4)
    for n in bc_nodes:
        ops.fix(n, 1, 1, 1, 1, 1, 1)

    # Loading
    pv = 20
    ops.timeSeries('Linear', 1)
    ops.pattern('Plain', 1, 1)
    load_nodes = nodesByLocation(x=0.4)
    for n in load_nodes:
        #ops.load(n, 0, 0, -pv, 0, 0, 0)    # Vertical load (z) producing bending
        ops.load(n, 0, -pv)     # Plane stress vertical load (y)
    
    # Solution
    loadcase = "DistributedLoad"
    #opsplt.createODB(model_name, loadcase)
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
    plt.figure()
    opsv.plot_model()
    plt.axis('equal')
    """
    # - plot deformation
    plt.figure()
    opsv.plot_defo()
    # opsv.plot_defo(sfac, unDefoFlag=1, fmt_undefo='g:')
    plt.axis('equal')

    # get values at OpenSees nodes
    sig_out = opsv.quad_sig_out_per_node()
    print(f'sig_out:\n{sig_out}')"""