# ellpsoid with holes
import pygmsh, math
import pyvista as pv


FILE_VTK = './meshing/ellipsoid_with_holes.vtk'

with pygmsh.occ.Geometry() as geom:
    geom.characteristic_length_max = 0.1
    ellipsoid = geom.add_ellipsoid([0.0, 0.0, 0.0], [1.0, 0.7, 0.5])

    cylinders = [
        geom.add_cone(
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
            1.0,
            0.3,
            mesh_size=0.1,
            angle=1.25 * math.pi,
        ),
        geom.add_cylinder([-1.0, 0.0, 0.0], [2.0, 0.0, 0.0], 0.3),
        geom.add_cylinder([0.0, -1.0, 0.0], [0.0, 2.0, 0.0], 0.3),
        geom.add_cylinder([0.0, 0.0, -1.0], [0.0, 0.0, 2.0], 0.3),
    ]
    geom.boolean_difference(ellipsoid, geom.boolean_union(cylinders))

    mesh = geom.generate_mesh()
    
    mesh.write(FILE_VTK)

    grid = pv.read(FILE_VTK)
    grid.plot(show_scalar_bar=True, show_axes=False, show_edges=True)