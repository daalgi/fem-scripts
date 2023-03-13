"""
https://www.code-aster.org/forum2/viewtopic.php?id=26184

I would like to use the new feature of 
Code_aster v15.4 : to be able to use Code_Aster 
directly from an external Python console.

As presented in the following training :
    Module 5 : Development training - 20 - 
    New architecture of code_aster - 
    What's new in 15.3.

...

Je n'ai pas réussi à utiliser le code_aster présent 
dans le container, mais cela marche avec un 
code_aster compilé.

Run this script from the `salome shell` to
have access to `as_run` (and `code_aster`?)
)
```
singularity shell salome
salome shell
python dev/scripts/fem-scripts/salome/run_aster.py
```
"""
import sys

# aster_folder = "/media/daalgi/disk/opt/salome_meca/Salome-V2021-s9/tools/Code_aster_stable-1540/lib/aster/code_aster"
aster_folder = "/opt/salome_meca/Salome-V2021-s9/tools/Code_aster_stable-1540/lib/aster/code_aster"
sys.path.append(aster_folder)
print(sys.path)
# Position the environment in a shell
#export PREFIX=/home
import code_aster
# from code_aster.Commands import *
# code_aster.init()
# mesh = code_aster.Mesh()
# # mesh.readMedFile('test001f.mmed')
# mesh.readMedFile('beam1d.med')
# print(mesh)