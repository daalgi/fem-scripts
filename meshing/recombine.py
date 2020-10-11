import pygmsh
import pyvista as pv


radius_in = 0.5
radius_out = 1
div_lines = 3
div_arc = 12

with pygmsh.geo.Geometry() as geom:   

    # Points forming the axis of the circle
    p1 = geom.add_point((0, 0, 0), mesh_size=1)
    p2 = geom.add_point((radius_in, 0, 0), mesh_size=1)
    p3 = geom.add_point((radius_out, 0, 0), mesh_size=1)
    p4 = geom.add_point((0, radius_in, 0), mesh_size=1)    
    p5 = geom.add_point((0, radius_out, 0), mesh_size=1)
        
    # Lines
    l1 = geom.add_line(p2, p3)
    l2 = geom.add_line(p4, p5)
    c1 = geom.add_circle_arc(p2, p1, p4)
    c2 = geom.add_circle_arc(p3, p1, p5)
    
    # Curve loop
    cloop = geom.add_curve_loop([l1, c2, -l2, -c1])

    # Surfaces of the curve loops
    # NOTE: Must add_plane_surface (PlaneSurface class), 
    # which has the parameter dim_tags
    # necessary for using set_recombined_surface
    surface = geom.add_plane_surface(cloop)

    # Define arc divisions
    geom.set_transfinite_curve(c1, div_arc+1, "Progression", 1)
    geom.set_transfinite_curve(c2, div_arc+1, "Progression", 1)
    
    # Define horizontal and vertical line divisions
    geom.set_transfinite_curve(l1, div_lines+1, "Progression", 1)
    geom.set_transfinite_curve(l2, div_lines+1, "Progression", 1)
    
    # Define transfinite surfaces
    geom.set_transfinite_surface(surface, "Left", [])
    
    # Mesh
    geom.set_recombined_surfaces([surface])
    mesh = geom.generate_mesh()

    # Save mesh in a vtk file
    file_vtk = './meshing/recombine.vtk'
    mesh.write(file_vtk)
    grid = pv.read(file_vtk)

    # Plot
    grid.plot(show_axes=True, show_edges=True)