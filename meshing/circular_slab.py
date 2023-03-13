import math
import pygmsh
import pyvista as pv


with pygmsh.geo.Geometry() as geom:
    geom.characteristic_length_max = 0.5
    """
    p = geom.add_point([0, 0, 0])
    q = geom.add_point([10, 0, 0])
    l = geom.add_line(p, q)
    c = geom.revolve(
        input_entity=l, rotation_axis=[0, 0, 1], point_on_axis=[0, 0, 0], angle=math.pi/2)
    
    #cp = geom.copy(c)
    #geom.symmetrize(c, [0, 0, 0, 1])
    mesh = geom.generate_mesh()
    #gmsh.model.geo.synchronize()
    """
    
    #radius = [2, 2.2, 2.4, 3, 10]
    #radius = [10]
    radius = [3, 10]
    circles = []
    for r in radius:
        circles.append(geom.add_circle([0, 0, 0], radius=r, num_sections=48))

    for circle in circles[:-1]:
        for arc in circle.curve_loop.curves:
            geom.in_surface(arc, circles[-1].plane_surface)

    """c = geom.add_disk(x0=[0, 0, 0], radius0=10)
    #ci = geom.add_circle([0, 0, 0], radius=5, num_sections=48)
    #ci = geom.add_disk(x0=[0, 0, 0], radius0=5)
    re = geom.add_rectangle(x0=[-2, -2, 0], a=4, b=6)
    #geom.in_surface()
    #geom.boolean_union([c, re])
    """
    # mesh = geom.generate_mesh(remove_lower_dim_cells=True)
    mesh = geom.generate_mesh()
    
    file_vtk = './meshing/circular_slab.vtk'
    mesh.write(file_vtk)
    grid = pv.read(file_vtk)

    # plot the data with an automatically created Plotter
    grid.plot(show_axes=True, show_edges=True)
