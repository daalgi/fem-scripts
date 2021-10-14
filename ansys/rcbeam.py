import os, sys
sys.path.append('.\\')

import pyansys
import pyvista as pv
from ansys.base import init, Beam

beam = Beam(6, 0.6, 0.3)
jobname = 'rcbeam'
mapdl, define = init(jobname=jobname)

mapdl.prep7()
mapdl.block(0, beam.length, 0, beam.height, 0, beam.width)

