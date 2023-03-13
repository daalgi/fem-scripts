import pygmsh
import pyvista as pv

project_folder = "/home/daalgi/tut/fem/aster/00frame"

with pygmsh.geo.Geometry() as geom:
    # geom.characteristic_length_max = 0.5

    points = [
        (0, -1000, 0),
        (0, -1000, 1000),
        (0, -500, 1000),
        (0, 0, 1000),
        (0, 500, 1000),
        (0, 1000, 1000),
        (0, 1000, 0),
    ]
    lines = []
    mesh_size = 100

    n = len(points)
    prev = geom.add_point(points[0], mesh_size=mesh_size)
    for i in range(1, n):
        curr = geom.add_point(points[i], mesh_size=mesh_size)
        lines.append(geom.add_line(prev, curr))
        prev = curr
    
    # geom.symmetrize(lines, coefficients=(0, 1, 0, 0))

    mesh = geom.generate_mesh()

    # Save mesh in a vtk file
    file_vtk = './salome/frame.vtk'
    mesh.write(file_vtk)
    file_med = './salome/frame.med'
    mesh.write(file_med)

    # Plot
    grid = pv.read(file_vtk)
    grid.plot(show_axes=True, show_edges=True)