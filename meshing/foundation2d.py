import math
import pygmsh
import pyvista as pv

h1 = 1
in_r = 2
out_r = 2.4
ped_r = 3
slab_r = 10
radius = [in_r, out_r, ped_r, slab_r]

div_in = 5
div_load = 2
div_out = 3
div_slab = 10
div_circ = 12
divs = [div_in, div_load, div_out, div_slab]

with pygmsh.geo.Geometry() as geom:   
    geom.characteristic_length_max = 0.5

    pointc = geom.add_point((0, 0, 0), mesh_size=1)
    pointsh = [pointc] + [geom.add_point((r, 0, 0), mesh_size=1) for r in radius]
    pointsv = [pointc] + [geom.add_point((0, r, 0), mesh_size=1) for r in radius]

    arcs = [geom.add_circle_arc(p, pointc, q) for p, q in zip(pointsh[1:], pointsv[1:])]
    lh = [geom.add_line(p, q) for p, q in zip(pointsh[:-1], pointsh[1:])]
    lv = [geom.add_line(p, q) for p, q in zip(pointsv[:-1], pointsv[1:])]    

    cloops = [geom.add_curve_loop([lh[0], arcs[0], -lv[0]])]
    cloops += [geom.add_curve_loop([h, cext, -v, -cint]) for h, cext, v, cint in zip(lh[1:], arcs[1:], lv[1:], arcs[:-1])]
    surfaces = [geom.add_surface(cloop) for cloop in cloops]

    for a in arcs:
        geom.set_transfinite_curve(a, div_circ, "Progression", 1)

    for h, v, div in zip(lh, lv, divs):
        geom.set_transfinite_curve(h, div, "Progression", 1)
        geom.set_transfinite_curve(v, div, "Progression", 1)

    for s in surfaces[1:]:
        geom.set_transfinite_surface(s, corner_tags=s.curve_loop.curves)
    
    #geom.set_recombined_surfaces(surfaces)
    
    mesh = geom.generate_mesh()

    file_vtk = './meshing/foundation2d.vtk'
    mesh.write(file_vtk)
    grid = pv.read(file_vtk)

    # plot the data with an automatically created Plotter
    grid.plot(show_axes=True, show_edges=True)