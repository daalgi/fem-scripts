import math
import pygmsh
import pyvista as pv


length = 3.
height = 0.59
width = 0.59

elem_max_size = 0.59
num_nodes_horizontal = int(math.ceil(length // elem_max_size) + 1)
num_nodes_vertical = int(math.ceil(height / elem_max_size) + 1)
num_nodes_transversal = int(math.ceil(width / elem_max_size) + 1)
num_div_transversal = num_nodes_transversal - 1
transversal_elem_size = width / num_nodes_transversal

with pygmsh.geo.Geometry() as geom:   
    geom.characteristic_length_max = elem_max_size

    points = [geom.add_point((0, 0, 0), mesh_size=1)]
    points += [geom.add_point((length, 0, 0), mesh_size=1)]
    points += [geom.add_point((length, 0, height), mesh_size=1)]
    points += [geom.add_point((0, 0, height), mesh_size=1)]
    
    lines = [geom.add_line(points[i-1], points[i]) for i in [1, 2, 3, 0]]

    cloop = geom.add_curve_loop(lines)
    surface = geom.add_plane_surface(cloop)

    for i, line in enumerate(lines):
        num_nodes = num_nodes_horizontal if i % 2 == 0 else num_nodes_vertical
        geom.set_transfinite_curve(line, num_nodes, "Progression", 1)
    
    geom.set_transfinite_surface(surface, "Left", [])
    geom.extrude(surface, 
        translation_axis=(0, width, 0), 
        num_layers=num_div_transversal, 
        recombine=True)
    
    # Mesh
    geom.set_recombined_surfaces([surface])
    mesh = geom.generate_mesh()

    # Save mesh in a vtk file
    file_vtk = './meshing/beam3d.vtk'
    mesh.write(file_vtk)
    grid = pv.read(file_vtk)

    # Plot
    grid.plot(show_axes=True, show_edges=True)