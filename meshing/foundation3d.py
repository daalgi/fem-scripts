import math
import pygmsh
import gmsh
import pyvista as pv

slab_r = 9
slab_h_edge = 0.5
slab_h_slope = 2
ped_h = 0.8
ped_r = 3
y_ped_top = 0
y_ped_bot = y_ped_top - ped_h
y_slab_top = y_ped_bot
y_slab_edge_top = y_slab_top - slab_h_slope
y_slab_bot = y_slab_edge_top - slab_h_edge

with pygmsh.geo.Geometry() as geom:   
    geom.characteristic_length_max = 0.1

    points = [
        [0, 0, y_slab_bot],
        [slab_r, 0, y_slab_bot],
        [slab_r, 0, y_slab_edge_top],
        [ped_r, 0, y_slab_top],
        [0, 0, y_slab_top]
    ]
    pol = geom.add_polygon(points, mesh_size=0.2)     
    
    vol = geom.revolve(
        input_entity=pol, 
        rotation_axis=[0, 0, 1], 
        point_on_axis=[0, 0, 0],
        angle=math.pi/2,
        num_layers=20,
        recombine=True
        )

    # TODO symmetry
    # TODO fix the mesh at the center
    #geom.miror(vol, [1, 0, 0, 0])

    
    # Mesh
    geom.set_recombined_surfaces([pol.surface])
    mesh = geom.generate_mesh(algorithm=8)

    # Save mesh in a vtk file
    file_vtk = './meshing/foundation3d.vtk'
    mesh.write(file_vtk)
    grid = pv.read(file_vtk)

    # Plot
    grid.plot(show_axes=True, show_edges=True)