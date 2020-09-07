# fem-scripts

## GMSH
Links:
http://gmsh.info/
https://gitlab.onelab.info/gmsh/gmsh
https://gitlab.onelab.info/gmsh/gmsh/-/tree/master/tutorial/python
https://github.com/nschloe/pygmsh/
http://www2.geo.uni-bonn.de/~wagner/pg/index.html
https://gitlab.onelab.info/gmsh/gmsh/tree/master/demos/api/

Python API
https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/api/gmsh.py

First tutorial
https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/tutorial/python/t1.py

Transfinite meshes
https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/tutorial/python/t6.py

Mesh fields
https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/tutorial/python/t10.py

Unstructured quqdrangular meshes
https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/tutorial/python/t11.py

Embedded points, lines and surfaces
https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/tutorial/python/t15.py

First tutorial with OCC
https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/tutorial/python/t16.py

Quadrangular mesh
https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/tutorial/python/t11.py


## Mesh options
https://gmsh.info/doc/texinfo/gmsh.html#Mesh-options-list

B.3 Mesh options list

gmsh.option.setNumber("Mesh.Algorithm", 5)

Mesh.Algorithm
2D mesh algorithm (1: MeshAdapt, 2: Automatic, 3: Initial mesh only, 5: Delaunay, 6: Frontal-Delaunay, 7: BAMG, 8: Frontal-Delaunay for Quads, 9: Packing of Parallelograms)
Default value: 6
Saved in: General.OptionsFileName

Mesh.Algorithm3D
3D mesh algorithm (1: Delaunay, 3: Initial mesh only, 4: Frontal, 7: MMG3D, 9: R-tree, 10: HXT)
Default value: 1
Saved in: General.OptionsFileName

Mesh.AlgorithmSwitchOnFailure
Switch meshing algorithm on failure? (Currently only for 2D Delaunay-based algorithms, switching to MeshAdapt)
Default value: 1
Saved in: General.OptionsFileName
