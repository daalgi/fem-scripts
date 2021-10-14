import os, sys
sys.path.append('.\\')

import pyansys
from ansys.base import init


wd = 'C:\\z10'
jobname = 'global'

mapdl = init(working_directory=wd, jobname=jobname)
mapdl.resume(f'{jobname}.db')
mapdl.post1()

mapdl.set(1, 1)
mapdl.esel('S', 'MAT', vmin=1)

#mapdl.eplot()
#mapdl.wait(1)

# POST-PROCESSING
resFile = os.path.join(mapdl.path, f'{jobname}.rst')
res = pyansys.read_binary(resFile)



