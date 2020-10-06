from select import nodesByLocation

import openseespy.opensees as ops
import openseespy.postprocessing.Get_Rendering as opsplt


from dataclasses import dataclass
import os


def init(output=False):
    # Initialize
    ops.wipe()
    #ops.model('Basic', '-ndm', 2)
    ops.model('Basic', '-ndm', 3)
    coordTransf = "Linear"  # Linear, PDelta, Corotational
    #ops.geomTransf(coordTransf, 1)
    massType = "-lMass"  # -lMass, -cMass
    # Save results in ParaView format
    if output:
        if not os.path.exists(output):
            os.makedirs(output)
        ops.recorder('PVD', output, 'disp')

def mesh(h, emod=30e6, nu=0.2, rho=2.5):
    crds = [
        1, 0, 0, 0,
        2, 7, 0, 0,
        3, 7, 5, 0,
        4, 0, 5, 0,
    ]
    # block2D(numX, numY, startNode, startEle, eleType, *eleArgs, *crds)
    #ops.block2D(10, 10, 1, 1, 'shell', crds)
    
    ops.node(1, 0, 0, 0)
    ops.node(2, 7, 0, 0)
    ops.node(3, 7, 5, 0)
    ops.node(4, 0, 5, 0)
    nodes = [1, 2, 3, 4]
    ops.section('ElasticMembranePlateSection', 1, emod, nu, h, rho)
    ops.element('ShellMITC4', 1, *nodes, 1)

    #nDMaterial('ElasticIsotropic', matTag, E, nu, rho=0.0)
    #ops.nDMaterial('ElasticIsotropic', 1, emod, nu, rho)
    #element('quad', eleTag, *eleNodes, thick, type, matTag, <pressure=0.0, rho=0.0, b1=0.0, b2=0.0>)
    #ops.element('quad', 1, 1, 2, 3, 4, h, 'PlaneStrain', 1, 0, rho)
    

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
    # Geometry   

    # Create model mesh
    model_name = "shell"
    init(output=f"./ops/{model_name}")
    mesh(h=0.5)
    
    # Boundary conditions
    for n in ops.getNodeTags():
        if ops.nodeCoord(n)[0] == 0:
            ops.fix(n, 1, 1, 1, 1, 1, 1)    
    
    # Loading
    pv = 20
    ops.timeSeries('Linear', 1)
    ops.pattern('Plain', 1, 1)
    ops.load(3, 0, 0, -pv/2, 0, 0, 0)
    ops.load(2, 0, 0, -pv, 0, 0, 0)
    
    # Solution
    loadcase = "DistributedLoad"
    opsplt.createODB(model_name, loadcase)
    solve()
    
    # Post-processing    
    res = ""
    
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
        

    res += '\n'
    selection = nodesByLocation(xmin=1, ymin=5)
    for s in selection:
        res += f'\nNode {s}, location: {ops.nodeCoord(s)}'
    print(res)
    #opsplt.plot_model("nodes", "elements", Model=model_name)