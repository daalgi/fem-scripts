import math, sys
import gmsh

sys.path.append('.\\')
from meshing.sections import (
    section_rectangular, section_I
)

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
model = gmsh.model
occ = model.occ
geo = model.geo

#_, _, section = section_rectangular(height=0.8, width=0.3, factory=occ)
_, _, section = section_I(height=0.8, width=0.3, flange_th=0.1, web_th=0.05, factory=occ)

#geo.mesh.setTransfiniteCurve(l2, 5)
gmsh.option.setNumber("Mesh.Algorithm", 8)
#gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.1)
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.05)
gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 3) # or 3
gmsh.option.setNumber("Mesh.Smoothing", 10)
gmsh.model.mesh.setRecombine(2, section)
model.mesh.generate(2)

# Open GUI
gmsh.fltk.run()
gmsh.finalize()
