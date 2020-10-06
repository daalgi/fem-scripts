import meshio
import gmsh
import pygmsh
import pyvista as pv


"""
Command line:

meshio-convert sectionI.msh sectionI2.vtk --output-format vtk --ascii

"""

# read the data
file_msh = './/meshing//sectionI.msh'
mesh = meshio.read(filename=file_msh)
file_vtk = './meshing/sectionI.vtk'
mesh.write(file_vtk)
grid = pv.read(file_vtk)

# plot the data with an automatically created Plotter
grid.plot(show_scalar_bar=False, show_axes=True)