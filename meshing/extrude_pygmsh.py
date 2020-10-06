import meshio
import gmsh
import pygmsh
import pyvista as pv


with pygmsh.occ.Geometry() as geom:
    geom.characteristic_length_max = 0.05

    rectangle = geom.add_rectangle([-1.0, -1.0, 0.0], 2.0, 2.0, corner_radius=0.2)
    disk1 = geom.add_disk([-1.2, 0.0, 0.0], 0.5)
    disk2 = geom.add_disk([+1.2, 0.0, 0.0], 0.5, 0.3)

    disk3 = geom.add_disk([0.0, -0.9, 0.0], 0.5)
    disk4 = geom.add_disk([0.0, +0.9, 0.0], 0.5)
    
    #elements = [rectangle, disk1, disk2, disk3, disk4]
    #geom.set_recombined_surfaces([e.surface for e in elements])

    flat = geom.boolean_difference(
        geom.boolean_union([rectangle, disk1, disk2]),
        geom.boolean_union([disk3, disk4]),
    )

    #geom.set_recombined_surfaces([flat.surface])

    gmsh.option.setNumber("Mesh.Algorithm", 8)
    gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 3) # or 3
    #gmsh.model.mesh.setRecombine(2, flat)

    geom.extrude(flat, [0, 0, 0.3], num_layers=2, recombine=True)
    """
    ## mesh options: http://gmsh.info/doc/texinfo/gmsh.html#Mesh-options-list
    # quads
    geom.add_raw_code('Mesh.RecombineAll = 1;')
    # hex
    geom.add_raw_code('Mesh.Recombine3DAll = 1;')
    # uses DelQuad algorithm, instead of default Blossom for regular meshing
    # 1=MeshAdapt, 2=Automatic, 5=Delaunay, 6=Frontal, 7=BAMG, 8=DelQuad
    geom.add_raw_code('Mesh.Algorithm = 8;')
    # uses frontal hex - outcommented as it will distort mesh
    # 1=Delaunay, 2=New Delaunay, 4=Frontal, 5=Frontal Delaunay, 6=Frontal Hex, 7=MMG3D, 9=R-tree
    #geom.add_raw_code('Mesh.Algorithm3D = 6;')
    # turns off mesh smoothing - outcommented as it will distort mesh
    #geom.add_raw_code('Mesh.Smoothing = 0;')
    # mesh element order 1=linear,2=quadratic,.. (example works for linear elements only)
    geom.add_raw_code('Mesh.ElementOrder = 1;')
    # add lateral surfaces to extrude output
    geom.add_raw_code('Geometry.ExtrudeReturnLateralEntities = 1;')
    """
    gmsh.model.geo.synchronize()
    mesh = geom.generate_mesh()

    file_vtk = './meshing/extrude.vtk'
    mesh.write(file_vtk)
    grid = pv.read(file_vtk)

    # plot the data with an automatically created Plotter
    grid.plot(show_scalar_bar=True, show_axes=False)