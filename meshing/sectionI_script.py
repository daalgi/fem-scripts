import math, sys
import gmsh

sys.path.append('.\\')
from meshing.sections import (
    section_rectangular, section_I
)

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
mesh = gmsh.model.mesh
occ = gmsh.model.occ
geo = gmsh.model.geo
factory = occ

#_, section = section_rectangular(height=0.8, width=0.3, factory=occ)
section = section_I(height=0.8, width=0.8, flange_th=0.1, web_th=0.05, factory=factory)
factory.synchronize()

"""
# Embed additional lines
if len(section.embedded) > 0:
    for line in section.embedded:
        l = factory.addLine(line[0], line[1])
        factory.synchronize()
        # model.embed(dim, tags, inDim, inTag)
        mesh.embed(1, [l], 2, section.surface)

if len(section.transfinite) > 0:
    for line in section.transfinite:
        mesh.setTransfiniteCurve(line, 5)
"""

#geo.mesh.setTransfiniteCurve(l2, 5)
gmsh.option.setNumber("Mesh.Algorithm", 8)
#gmsh.option.setNumber("Mesh.Algorithm", 1)
#gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.1)
#gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.05)
gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 2) # or 3
#gmsh.option.setNumber("Mesh.Smoothing", 10)
mesh.setRecombine(2, section.surface)
mesh.generate(2)

gmsh.model.setPhysicalName(2, section.surface, "section")

# Open GUI
gmsh.write('./meshing/sectionI.msh')
gmsh.fltk.run()
gmsh.finalize()
