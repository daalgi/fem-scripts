import meshio
import pygmsh
import pyvista as pv

project_folder = "/home/daalgi/tut/fem/aster/00frame"

with pygmsh.geo.Geometry() as geom:
    # geom.characteristic_length_max = 0.5

    length = 10
    mesh_size = 5

    geom.characteristic_length_max = mesh_size
    beam = geom.add_line(
        geom.add_point((0, 0, 0), mesh_size=mesh_size),
        geom.add_point((length, 0, 0), mesh_size=mesh_size),
    )

    geom.add_physical(beam, "beam")
    # geom.add_physical(beam.points[0], "left_bc")
    # geom.add_physical(beam.points[1], "right_bc")

    # geom.set_transfinite_curve(beam, 10, "Progression", 1)
    mesh = geom.generate_mesh()
    print(mesh)
    # Save mesh in a vtk file
    file_vtk = "./salome/beam1d.vtk"
    mesh.write(file_vtk)
    file_med = "./salome/beam1d.med"
    mesh.write(file_med)

    # Plot
    grid = pv.read(file_vtk)
    grid.plot(show_axes=True, show_edges=True)

