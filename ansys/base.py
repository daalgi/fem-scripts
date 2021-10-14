import os
from dataclasses import dataclass
import pyansys


ANSYS_PATHS = [
    'C:\\Program Files\\ANSYS Inc\\ANSYS 2020R1\\v201\\ansys\\bin\\winx64\\MAPDL.exe',
    'C:\\Program Files\\ANSYS Inc\\ANSYS 2020R1\\v201\\ansys\\bin\\winx64\\MAPDL.exe',
    'C:\\Program Files\\ANSYS Inc\\ANSYS 2019R2\\v192\\ansys\\bin\\winx64\\MAPDL.exe',
    'C:\\Program Files\\ANSYS Inc\\ANSYS 2018R2\\v182\\ansys\\bin\\winx64\\MAPDL.exe',
    'C:\\Program Files\\ANSYS Inc\\ANSYS 2020R2\\v202\\ansys\\bin\\winx64\\MAPDL.exe'
]

def init(
    ansys_path: str = None, 
    working_directory: str = None, 
    jobname: str = "model",
    loglevel: str = "ERROR"
    ):
    if not ansys_path:
        ansys_path = ANSYS_PATHS[0]
    pyansys.change_default_ansys_path(ansys_path)

    if not working_directory:
        working_directory = os.getcwd() + f'\\temp\\{jobname}'

    if not os.path.exists(working_directory):
        os.makedirs(working_directory)

    mapdl = pyansys.launch_mapdl(
        run_location=working_directory, 
        override=True,
        jobname=jobname,
        loglevel=loglevel
    )
    mapdl.finish()
    mapdl.clear()
    define = Definer(mapdl)
    return mapdl, define


@dataclass
class Beam:
    length: float = 6
    height: float = 0.6
    width: float = 0.3


class Definer:
    def __init__(self, mapdl):
        self.mapdl = mapdl

    def elastic_material(self, num: int, ex: float, pr: float, dens: float = None):
        self.mapdl.prep7()
        self.mapdl.mp('EX', num, ex)
        self.mapdl.mp('PRXY', num, pr)
        if dens:
            self.mapdl.mp('DENS', num, dens)
    
    def drucker_prager_concrete_material(self, num, fuc: float,
        fut: float = None, fbc: float = None,
        delta_c: float = 0.25, delta_t: float = 1.0):
        """
        Keyword arguments:
        num -- material id number
        fuc -- uniaxial compressive strength
        fut -- uniaxial tensile strength
        fbc -- biaxial compressive strength
        """
        # Drucker-Prager concrete strength parameters
        self.mapdl.run(f"TB, CONCR, {num}, , , DP")
        if not fut:
            fut = 0.3 * fuc ** (2./3)
        if not fbc:
            fbc = 1.15 * fuc
        self.mapdl.tbdata(num, fuc, fut, fbc)

        # Drucker-Prager concrete dilatation



    def reinforcement_section(self, secnum: int, matnum: int, area: float, discrete: bool = True):
        self.mapdl.prep7()
        if discrete:
            self.mapdl.sectype(secnum, "REINF", "DISCRETE")
            self.mapdl.secdata(matnum, area, "MESH")
        else:
            #self.mapdl.sectype(num, "REINF", "SMEARED")
            raise NotImplementedError
        
