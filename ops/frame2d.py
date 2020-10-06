import openseespy.opensees as ops
import openseespy.postprocessing.Get_Rendering as opsplt

from dataclasses import dataclass
import os


@dataclass
class BeamElement:
    length: float
    area: float
    inertia: float
    elastic_modulus: float = 30e6

@dataclass
class Frame:
    stories: int
    spans: int

def init(output=False):
    # Initialize
    ops.wipe()
    ops.model('Basic', '-ndm', 2)
    coordTransf = "Linear"  # Linear, PDelta, Corotational
    ops.geomTransf(coordTransf, 1)
    massType = "-lMass"  # -lMass, -cMass
    # Save results in ParaView format
    if output:
        if not os.path.exists(output):
            os.makedirs(output)
        ops.recorder('PVD', output, 'disp')

def mesh(beams: BeamElement, columns: BeamElement, frame: Frame):
    node_counter = 0
    beam_ele = 0
    column_ele = frame.spans * frame.stories
    for story in range(0, frame.stories + 1):
        for span in range(0, frame.spans + 1):
            node_counter += 1
            ops.node(node_counter, span * beams.length, story * columns.length)
            if story > 0:
                column_ele += 1
                ops.element(
                    'elasticBeamColumn', column_ele, node_counter-frame.spans-1, node_counter,
                    columns.area, columns.elastic_modulus, columns.inertia, 1
                )
            if story > 0 and span > 0:
                beam_ele += 1
                ops.element(
                    'elasticBeamColumn', beam_ele, node_counter-1, node_counter, 
                    beams.area, beams.elastic_modulus, beams.inertia, 1
                )

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
    beams = BeamElement(length=7, area=0.4*0.3, inertia=0.3*0.4**3/12)
    columns = BeamElement(length=5, area=0.3*0.3, inertia=0.3**4/12)
    frame = Frame(stories=8, spans=5)

    # Create model mesh
    model_name = "frame2d"
    init(output=f"./ops/{model_name}")
    mesh(beams=beams, columns=columns, frame=frame)
    
    # Boundary conditions
    for n in ops.getNodeTags():
        if ops.nodeCoord(n)[1] == 0:
            ops.fix(n, 1, 1, 1)    
    
    # Loading
    loadcase = "distributedLoad"
    qv = 4 * 4
    ops.timeSeries('Linear', 1)
    ops.pattern('Plain', 1, 1)
    for elem in ops.getEleTags():
        nodes = ops.eleNodes(elem)
        if ops.nodeCoord(nodes[0])[1] == ops.nodeCoord(nodes[1])[1]:
            ops.eleLoad('-ele', elem, '-type', '-beamUniform', -qv, 0)
    
    # Solution
    opsplt.createODB(model_name, loadcase)
    solve()
    
    # Post-processing    
    res = ""
    """for i, n in enumerate(ops.getNodeTags()):
        res += f'\nNode: {n:>3.0f}'
        res += f'\tCoords: {ops.nodeCoord(n)}'
    """
    for e in ops.getEleTags():
        ni = ops.eleNodes(e)[0]
        nj = ops.eleNodes(e)[1]
        if ops.nodeCoord(ni)[0] == 0 == ops.nodeCoord(nj)[0]:
            res += f'\nColumn: {e:>3.0f}'
            res += f'\tCoordY: {ops.nodeCoord(ni)[1]:>5.2f} m'
            res += f'\t\tUybot: {1e3 * ops.nodeDisp(ni)[1]:>7.2f} mm'
            res += f'\t\tNtop: {ops.eleForce(e)[3]:>7.2f} kN'
            res += f'\t\tNbot: {ops.eleForce(e)[0]:>7.2f} kN'
            res += f'\t\tMztop: {ops.eleForce(e)[5]:>7.2f} kNm'
            res += f'\t\tMzbot: {ops.eleForce(e)[2]:>7.2f} kNm'

    res += '\n'
    #print(res)
    #opsplt.plot_model("nodes", "elements", Model=model_name)
    #opsplt.plot_deformedshape(Model=model_name, LoadCase=loadcase, overlap=True, tstep=0.0, scale=10.0)