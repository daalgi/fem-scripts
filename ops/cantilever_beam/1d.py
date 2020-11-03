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
    length_inc = beam.length / num_nodes_horizontal
    ops.node(1, 0, 0)
    for i in range(2, num_nodes_horizontal+2):
        ops.node(i, (i - 1) * length_inc, 0)
        #ops.element('elasticBeamColumn', eleTag, iNode, jNode, A, E, I, transfTag, '-mass', M, massType)
        ops.element('elasticBeamColumn', i-1, i-1, i, beam.area, beam.elastic_modulus, beam.inertia, 1)

    return True


def run():
    model_name = "1d"
    filename = f'./ops/cantilever_beam/{model_name}'
    init(output=filename, ndm=2, ndf=3)

    # Create mesh
    beam = CantileverBeam()
    m = create_mesh(beam=beam)
       
    # Boundary conditions
    bc_nodes = opsel.nodes.by_location(x=0)
    for n in bc_nodes.ids():
        ops.fix(n, 1, 1, 1, 1)
    
    # Loading
    for elem in ops.getEleTags():
        ops.eleLoad('-ele', elem, '-type', '-beamUniform', -beam.pressure*beam.width, 0)
    
    # Solution
    loadcase = "DistributedLoad"
    opsplt.createODB(model_name, loadcase)
    solve()

    # Post-processing
    #ops.printModel('-file', filename)
    print(f'\n{filename}')
    print_vertical_displacements(beam, u_i=1)
    print_reactions(beam, reaction_i=1)
    

if __name__ == '__main__':    
    run()