import math
import pygmsh
import gmsh
import pyvista as pv

h1 = 1
in_r = 2
out_r = 2.4
ped_r = 3
slab_r = 10
radius = [in_r, out_r, ped_r, slab_r]

div_in = 5
div_load = 3
div_out = 4
div_slab = 10
div_circ = 12
divs = [div_in, div_load, div_out, div_slab]

with pygmsh.geo.Geometry() as geom:   
    geom.characteristic_length_max = 0.5

    # Points forming the axis of the circle with the given divisions
    pointc = geom.add_point((0, 0, 0), mesh_size=1)
    
    pointsh = [geom.add_point((-r, 0, 0), mesh_size=1) for r in radius[::-1]]
    pointsh += [pointc] + [geom.add_point((r, 0, 0), mesh_size=1) for r in radius]

    pointsv = [geom.add_point((0, -r, 0), mesh_size=1) for r in radius[::-1]]
    pointsv += [pointc] + [geom.add_point((0, r, 0), mesh_size=1) for r in radius]

    # Arcs by quadrant
    #arcs = [geom.add_circle_arc(p, pointc, q) for p, q in zip(pointsh[1:], pointsv[1:])]
    quadrant_divs = len(radius)
    # Arcs for each quadrant from the center outwards
    arcs_q1 = [geom.add_circle_arc(p, pointc, q) for p, q in zip(pointsh[quadrant_divs+1:], pointsv[quadrant_divs+1:])]
    arcs_q2 = [geom.add_circle_arc(p, pointc, q) for p, q in zip(pointsv[quadrant_divs+1:], pointsh[:quadrant_divs][::-1])]
    arcs_q3 = [geom.add_circle_arc(p, pointc, q) for p, q in zip(pointsh[:quadrant_divs][::-1], pointsv[:quadrant_divs][::-1])]
    arcs_q4 = [geom.add_circle_arc(p, pointc, q) for p, q in zip(pointsv[:quadrant_divs][::-1], pointsh[quadrant_divs+1:])]
    arcs = arcs_q1 + arcs_q2 + arcs_q3 + arcs_q4
    arcs_quadrants = [arcs_q1] + [arcs_q2] + [arcs_q3] + [arcs_q4]
    
    # Horizontal lines
    lh = [geom.add_line(p, q) for p, q in zip(pointsh[:-1], pointsh[1:])]
    # Vertical lines
    lv = [geom.add_line(p, q) for p, q in zip(pointsv[:-1], pointsv[1:])]
    # Lines by quadrant
    #   Q1: first -vertical then +horizontal
    #   Q2: first +horizontal then + vertical
    #   Q3: first +vertical then -horizontal
    #   Q4: first -horizontal then -vertical
    sign_quadrants = [[-1, +1], [+1, +1], [+1, -1], [-1, -1]]
    lq1 = [v for v in lv[quadrant_divs:]] + [h for h in lh[quadrant_divs:]]
    lq2 = [h for h in lh[:quadrant_divs][::-1]] + [v for v in lv[quadrant_divs:]]
    lq3 = [v for v in lv[:quadrant_divs][::-1]] + [h for h in lh[:quadrant_divs][::-1]]
    lq4 = [h for h in lh[quadrant_divs:]] + [v for v in lv[:quadrant_divs][::-1]]
    line_quadrants = [lq1] + [lq2] + [lq3] + [lq4]
   
    # Curve loops starting from the smalles arc in each quadrant in counter-clockwise direction
    cloops = []
    for quadrant, (aq, lq, sq) in enumerate(zip(arcs_quadrants, line_quadrants, sign_quadrants)):

        tup = (aq, lq[:quadrant_divs], [None] + aq[:-1], lq[quadrant_divs:])
        for a, l1, a_prev, l2 in zip(*tup):
        
            if a_prev == None:
                if sq[0] == 1 and sq[1] == 1:
                    cloops += [geom.add_curve_loop([a, l1, l2])]
                elif sq[0] == 1 and sq[1] == -1:
                    cloops += [geom.add_curve_loop([a, l1, -l2])]
                elif sq[0] == -1 and sq[1] == 1:
                    cloops += [geom.add_curve_loop([a, -l1, l2])]
                elif sq[0] == -1 and sq[1] == -1:
                    cloops += [geom.add_curve_loop([a, -l1, -l2])]
                
            else:
                if sq[0] == 1 and sq[1] == 1:
                    cloops += [geom.add_curve_loop([a, l1, -a_prev, l2])]
                elif sq[0] == 1 and sq[1] == -1:
                    cloops += [geom.add_curve_loop([a, l1, -a_prev, -l2])]
                elif sq[0] == -1 and sq[1] == 1:
                    cloops += [geom.add_curve_loop([a, -l1, -a_prev, l2])]
                elif sq[0] == -1 and sq[1] == -1:
                    cloops += [geom.add_curve_loop([a, -l1, -a_prev, -l2])]

    # Surfaces of the curve loops                
    surfaces = [geom.add_plane_surface(cloop) for cloop in cloops]

    # Define arc divisions
    for a in arcs:
        geom.set_transfinite_curve(a, div_circ, "Progression", 1)
    
    # Define horizontal and vertical line divisions
    for h, v, div in zip(lh, lv, divs[::-1] + divs):
        if div:
            geom.set_transfinite_curve(h, div, "Progression", 1)
            geom.set_transfinite_curve(v, div, "Progression", 1)
    
    # Define transfinite surfaces
    for s in surfaces:
        geom.set_transfinite_surface(s, "Left", [])        
    
    # Mesh
    # TODO: CopyMeshingMethod 
    # TODO: subdivision algorithm - all quads
    geom.set_recombined_surfaces(surfaces)
    mesh = geom.generate_mesh(algorithm=8)

    # Save mesh in a vtk file
    file_vtk = './meshing/foundation2d.vtk'
    mesh.write(file_vtk)
    grid = pv.read(file_vtk)

    # Plot
    grid.plot(show_axes=True, show_edges=True)