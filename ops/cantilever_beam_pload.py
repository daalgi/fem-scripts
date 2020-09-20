import openseespy.opensees as ops
import openseespy.postprocessing.Get_Rendering as opsplt

def init():
    # Initialize
    ops.wipe()
    ops.model('Basic', '-ndm', 2)
    coordTransf = "Linear"  # Linear, PDelta, Corotational
    ops.geomTransf(coordTransf, 1)
    massType = "-lMass"  # -lMass, -cMass

def mesh(length, divisions, area, emod, iz):
    length_inc = length / divisions
    ops.node(1, 0, 0)
    for i in range(2, divisions+2):
        ops.node(i, (i - 1) * length_inc, 0)
        #ops.element('elasticBeamColumn', eleTag, iNode, jNode, A, E, I, transfTag, '-mass', M, massType)
        ops.element('elasticBeamColumn', i-1, i-1, i, area, emod, iz, 1)

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
    length = 7.8
    height = 0.8
    width = 0.3

    divisions = 7
    length_inc = length / divisions

    # Section
    area = width * height
    iz = width * height ** 3 / 12

    # Material
    emod = 30.e6

    # Create model mesh
    init()
    mesh(length=length, divisions=divisions, area=area, emod=emod, iz=iz)

    # Boundary conditions
    ops.fix(1, 1, 1, 1)

    # Loading
    fv = 50
    ops.timeSeries('Linear', 1)
    ops.pattern('Plain', 1, 1)
    ops.load(divisions+1, 0, -fv, 0)

    # Solution
    solve()

    model_name = "CantileverBeam"
    loadcase = "PointLoad"
    opsplt.createODB(model_name, loadcase)
    res = ""
    for i, e in enumerate(ops.getEleTags()):
        n = ops.eleNodes(e)[0]
        res += f'\nNode: {n:>3.0f}'
        res += f'\tCoordX: {ops.nodeCoord(n)[0]:>5.2f} m'
        res += f'\t\tUy: {1e3 * ops.nodeDisp(n)[1]:>7.2f} mm'
        res += f'\t\tMz: {ops.eleForce(e)[2]:>7.2f} kNm'
        if i == divisions-1:
            n = ops.eleNodes(e)[1]
            res += f'\nNode: {n:>3.0f}'
            res += f'\tCoordX: {ops.nodeCoord(n)[0]:>5.2f} m'
            res += f'\t\tUy: {1e3 * ops.nodeDisp(n)[1]:>7.2f} mm'
            res += f'\t\tMz: {ops.eleForce(e)[5]:>7.2f} kNm'
    res += '\n'
    
    uymax = -fv * length ** 3 / 3 / emod / iz * 1e3
    res += f'\nTheoretical Uy,max: {uymax:>7.2f} mm'
    res += f'\nUy,max ratio:       {uymax  / (1e3 * ops.nodeDisp(divisions+1)[1]):>10.6f}'
    res += '\n'

    mzmax = fv * length
    res += f'\nTheoretical Mz,max: {mzmax:>7.2f} kNm'
    res += f'\nMz,max ratio:       {mzmax  / ops.eleForce(1)[2]:>10.6f}'
    res += '\n'
    print(res)