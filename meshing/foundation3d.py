import math
import pygmsh
import gmsh
import pyvista as pv

center_r = 1
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

lap_ri = 1.9
lap_ro = 2.4
lap_h = 0.5
y_lap_bot = y_slab_bot + 0.2
y_lap_top = y_lap_bot + lap_h

with pygmsh.geo.Geometry() as geom:   
    geom.characteristic_length_max = 0.1

    section_points = [
        [center_r, 0, y_slab_bot],
        [slab_r, 0, y_slab_bot],
        [slab_r, 0, y_slab_edge_top],
        [ped_r, 0, y_slab_top],
        [center_r, 0, y_slab_top]
    ]
    hole_points = [
        [lap_ri, 0, y_lap_bot],
        [lap_ro, 0, y_lap_bot],
        [lap_ro, 0, y_lap_top],
        [lap_ri, 0, y_lap_top],
    ]
    lap_hole = geom.add_polygon(hole_points, 1, make_surface=False)
    pol = geom.add_polygon(
        section_points, 
        mesh_size=0.1, 
        holes=[lap_hole.curve_loop])     
    
    # vol = geom.revolve(
    #     input_entity=pol, 
    #     rotation_axis=[0, 0, 1], 
    #     point_on_axis=[0, 0, 0],
    #     angle=math.pi/2,
    #     num_layers=20,
    #     recombine=True
    # )

    geom.revolve(
        input_entity=pol, 
        rotation_axis=[0, 0, 1], 
        point_on_axis=[0, 0, 0],
        angle=-math.pi/2,
        num_layers=20,
        recombine=True
    )

    # TODO symmetry
    # TODO fix the mesh at the center
    cp = geom.copy(pol)

    geom.revolve(
        input_entity=cp, 
        rotation_axis=[0, 0, 1], 
        point_on_axis=[0, 0, 0],
        angle=math.pi/2,
        num_layers=20,
        recombine=True
    )
    
    # Mesh
    geom.set_recombined_surfaces([pol.surface])
    #geom.set_recombined_surfaces([cp])
    mesh = geom.generate_mesh(algorithm=8)

    # Save mesh in a vtk file
    file_vtk = './meshing/foundation3d.vtk'
    mesh.write(file_vtk)
    file_med = './salome/foundation3d.med'
    mesh.write(file_med)

    # Plot
    grid = pv.read(file_vtk)
    grid.plot(show_axes=True, show_edges=True)