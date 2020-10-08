import pyansys
import os

ANSYS_PATH = 'C:\\Program Files\\ANSYS Inc\\ANSYS 2020R1\\v201\\ansys\\bin\\winx64\\MAPDL.exe'

def init(ansys_path: str = None, working_directory: str = None, jobname: str = ""):
    if not ansys_path:
        ansys_path = ANSYS_PATH
    pyansys.change_default_ansys_path(ansys_path)

    if not working_directory:
        working_directory = os.getcwd()
    mapdl = pyansys.launch_mapdl(
        run_location=working_directory, 
        override=True,
        jobname=jobname
    )
    mapdl.finish()
    mapdl.clear()
    return mapdl


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



