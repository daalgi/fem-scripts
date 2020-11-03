from dataclasses import dataclass
import os

import openseespy.opensees as ops
import opsel.nodes

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


def init(output=False, ndm=3, ndf=3):
    # Initialize
    ops.wipe()
    ops.model('Basic', '-ndm', ndm, '-ndf', ndf)
    coordTransf = "Linear"  # Linear, PDelta, Corotational
    if ndm == 2 and ndf == 3:
        ops.geomTransf(coordTransf, 1)
    massType = "-lMass"  # -lMass, -cMass

    # Loading
    ops.timeSeries('Linear', 1)
    ops.pattern('Plain', 1, 1)

    # Save results in ParaView format
    if output:
        if not os.path.exists(output):
            os.makedirs(output)
        ops.recorder('PVD', output, 'disp', 'pressure')


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


def print_vertical_displacements(beam, u_i=2):
    res = "\nMaximum vertical displacement"

    # Theoretical maximum vertical displacement
    res += f'\nTheoretical: {beam.vmax*1e3:>8.4f} mm'

    # Simulation maximum vertical displacement
    vmax_fem = max([abs(ops.nodeDisp(n)[u_i]) for n in ops.getNodeTags()])
    res += f'\nSimulation:  {vmax_fem*1e3:>8.4f} mm'
    
    print(res)


def print_reactions(beam, reaction_i=2):
    res = "\nReactions"

    # Theoretical maximum vertical displacement
    res += f'\nTheoretical: \tFz = {beam.reaction_fz:>8.2f} kN\t\tMx = {beam.reaction_mx:>8.2f} kNm'

    # Simulation maximum vertical displacement
    fz = sum([ops.nodeReaction(n.id)[reaction_i] for n in opsel.nodes.by_location(x=0)])
    res += f'\nSimulation:  \tFz = {fz:>8.2f} kN' #\t\tMx = {mx():>8.2f} kNm'
    
    print(res)
    """
    for n in opsel.nodes.by_location(x=0):
        print(ops.nodeReaction(n.id))
    """