"""
Run a script launching SALOME in TUI mode (text mode):
    -t: text mode
    -w1: kills CORBA servers at the end of the script
`./salome -t -w1 myscript.py`

Launch the current script
./salome_meca-lgpl-2021.0.0-2-20211014-scibian-9 -t -w1 /home/daalgi/dev/scripts/fem-scripts/salome/run.py
"""
import sys

# from dataclasses import dataclass


# @dataclass
# class Paths:
#     base: str = "/media/daalgi/disk/opt/salome_meca"
#     salome_launch: str = "/media/daalgi/disk/opt/devscripts"
#     as_run: str = "/Salome-V2021-s9/tools/Code_aster_stable-1540/lib/aster/as_run"
#     asterpy: str = "/Salome-V2021-s9/tools/Code_aster_stable-1540/lib/aster/"
#     # salome: str = "/Salome-V2021-s9/modules/KERNEL_V9_7_0/bin/salome"
#     # salome2: str = "/appli_V2021/bin/salome"
#     # salome: str = "/appli_V2021/lib/python3.6/site-packages/salome/salome/"
#     salome: str = "/appli_V2021/lib/python3.6/site-packages/salome/"


# folders = [
#     Paths.asterpy,
#     Paths.salome,
#     # Paths.salome2,
# ]

# for folder in folders:
#     sys.path.append(Paths.base + folder)

# from code_aster import
# import code_aster
# print(code_aster.__dict__)

import salome

salome.salome_init()
import salome_notebook

notebook = salome_notebook.NoteBook()
sys.path.insert(0, r"/home/daalgi/fem/00")

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Face_1 = geompy.MakeFaceHW(50, 100, 1)
geompy.TranslateDXDYDZ(Face_1, 25, 50, 0)
Disk_1 = geompy.MakeDiskR(20, 1)
platehole = geompy.MakeCutList(Face_1, [Disk_1], True)
edge_x = geompy.CreateGroup(platehole, geompy.ShapeType["EDGE"])
geompy.UnionIDs(edge_x, [10])
edge_y = geompy.CreateGroup(platehole, geompy.ShapeType["EDGE"])
geompy.UnionIDs(edge_y, [3])
edge_load = geompy.CreateGroup(platehole, geompy.ShapeType["EDGE"])
geompy.UnionIDs(edge_load, [6])
[edge_x, edge_y, edge_load] = geompy.GetExistingSubObjects(platehole, False)
geompy.addToStudy(O, "O")
geompy.addToStudy(OX, "OX")
geompy.addToStudy(OY, "OY")
geompy.addToStudy(OZ, "OZ")
geompy.addToStudy(Face_1, "Face_1")
geompy.addToStudy(Disk_1, "Disk_1")
geompy.addToStudy(platehole, "platehole")
geompy.addToStudyInFather(platehole, edge_x, "edge_x")
geompy.addToStudyInFather(platehole, edge_y, "edge_y")
geompy.addToStudyInFather(platehole, edge_load, "edge_load")

###
### SMESH component
###

import SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
# smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
# multiples meshes built in parallel, complex and numerous mesh edition (performance)

Mesh_1 = smesh.Mesh(platehole)
NETGEN_1D_2D = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_1D2D)
NETGEN_2D_Parameters_1 = NETGEN_1D_2D.Parameters()
NETGEN_2D_Parameters_1.SetMaxSize(6)
NETGEN_2D_Parameters_1.SetMinSize(3.13836)
NETGEN_2D_Parameters_1.SetSecondOrder(0)
NETGEN_2D_Parameters_1.SetOptimize(1)
NETGEN_2D_Parameters_1.SetFineness(2)
NETGEN_2D_Parameters_1.SetChordalError(-1)
NETGEN_2D_Parameters_1.SetChordalErrorEnabled(0)
NETGEN_2D_Parameters_1.SetUseSurfaceCurvature(1)
NETGEN_2D_Parameters_1.SetFuseEdges(1)
NETGEN_2D_Parameters_1.SetWorstElemMeasure(0)
NETGEN_2D_Parameters_1.SetUseDelauney(0)
NETGEN_2D_Parameters_1.SetCheckChartBoundary(232)
NETGEN_2D_Parameters_1.SetQuadAllowed(0)
NETGEN_2D_Parameters_1.SetWorstElemMeasure(32541)
NETGEN_2D_Parameters_1.SetCheckChartBoundary(168)
edge_x_1 = Mesh_1.GroupOnGeom(edge_x, "edge_x", SMESH.EDGE)
edge_y_1 = Mesh_1.GroupOnGeom(edge_y, "edge_y", SMESH.EDGE)
edge_load_1 = Mesh_1.GroupOnGeom(edge_load, "edge_load", SMESH.EDGE)
isDone = Mesh_1.Compute()
[edge_x_1, edge_y_1, edge_load_1] = Mesh_1.GetGroups()
smeshObj_1 = Mesh_1.GroupOnGeom(edge_x, "edge_x", SMESH.EDGE)
smeshObj_2 = Mesh_1.GroupOnGeom(edge_y, "edge_y", SMESH.EDGE)
smeshObj_3 = Mesh_1.GroupOnGeom(edge_load, "edge_load", SMESH.EDGE)
edge_x_2 = Mesh_1.GroupOnGeom(edge_x, "edge_x", SMESH.NODE)
edge_y_2 = Mesh_1.GroupOnGeom(edge_y, "edge_y", SMESH.NODE)
edge_load_2 = Mesh_1.GroupOnGeom(edge_load, "edge_load", SMESH.NODE)
Mesh_1.ConvertToQuadratic(0)
Mesh_1.ConvertToQuadratic(0, Mesh_1, True)
Mesh_1.ConvertToQuadratic(0)
Mesh_1.RemoveGroup(smeshObj_3)
Mesh_1.RemoveGroup(smeshObj_2)
Mesh_1.RemoveGroup(smeshObj_1)
smesh.SetName(Mesh_1, "Mesh_1")
try:
    Mesh_1.ExportMED(
        r"/home/daalgi/fem/00/ex01-platehole.med",
        auto_groups=0,
        version=0,
        overwrite=1,
        meshPart=None,
        autoDimension=1,
    )
    pass
except:
    print("ExportMED() failed. Invalid file name?")
[edge_x_1, edge_y_1, edge_load_1, edge_x_2, edge_y_2, edge_load_2] = Mesh_1.GetGroups()
smesh.SetName(Mesh_1, "Mesh_1")

## some objects were removed
aStudyBuilder = salome.myStudy.NewBuilder()
SO = salome.myStudy.FindObjectIOR(salome.myStudy.ConvertObjectToIOR(smeshObj_2))
if SO:
    aStudyBuilder.RemoveObjectWithChildren(SO)
SO = salome.myStudy.FindObjectIOR(salome.myStudy.ConvertObjectToIOR(smeshObj_1))
if SO:
    aStudyBuilder.RemoveObjectWithChildren(SO)
SO = salome.myStudy.FindObjectIOR(salome.myStudy.ConvertObjectToIOR(smeshObj_3))
if SO:
    aStudyBuilder.RemoveObjectWithChildren(SO)

## Set names of Mesh objects
smesh.SetName(NETGEN_1D_2D.GetAlgorithm(), "NETGEN 1D-2D")
smesh.SetName(NETGEN_2D_Parameters_1, "NETGEN 2D Parameters_1")
smesh.SetName(Mesh_1.GetMesh(), "Mesh_1")
smesh.SetName(edge_x_1, "edge_x")
smesh.SetName(edge_load_1, "edge_load")
smesh.SetName(edge_y_1, "edge_y")
smesh.SetName(edge_y_2, "edge_y")
smesh.SetName(edge_load_2, "edge_load")
smesh.SetName(edge_x_2, "edge_x")
