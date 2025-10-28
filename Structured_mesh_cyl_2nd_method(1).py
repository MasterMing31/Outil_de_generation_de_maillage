import sys
import salome
import salome_notebook
import os
import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS
import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder
import numpy as np

def arc_centers(x1, y1, x2, y2, r, normal_dir):

    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    
    if d > 2 * r:
        raise ValueError("No valid circle — points too far apart for this radius.")
    
    h = math.sqrt(r**2 - (d / 2)**2)
    nx, ny = -dy / d, dx / d  # perpendicular direction (unit)
    
    # Two possible centers
    c1 = (mx + h * nx, my + h * ny)
    c2 = (mx - h * nx, my - h * ny)

    # Compute dot product of vector (center-midpoint) with reference normal
    refx, refy = normal_dir
    dot1 = (c1[0] - mx) * refx + (c1[1] - my) * refy
    dot2 = (c2[0] - mx) * refx + (c2[1] - my) * refy
    
    return c1 if dot1 > dot2 else c2 # Corresponds to convex case

csquare_length = 5
csquare_radius = 20
radius = 8
height = 30
z_steps = 15

###
### This part is generated automatically by SALOME v9.15.0 with dump python functionality
###

salome.salome_init()
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'D:/Universite/Master_2/Projet num')

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

# Make vertices in order to build the arcs of the cylinder
theta = math.pi / 4
x_cyl = round(radius * math.cos(theta),6)
y_cyl = round(radius * math.sin(theta),6)

Vertex_1 = geompy.MakeVertex(x_cyl, y_cyl, 0)
Vertex_2 = geompy.MakeVertex(-x_cyl, y_cyl, 0)
Vertex_3 = geompy.MakeVertex(-x_cyl, -y_cyl, 0)
Vertex_4 = geompy.MakeVertex(x_cyl, -y_cyl, 0)

# Make the vertices of the curvilignial square
Vertex_5 = geompy.MakeVertex(csquare_length / 2, csquare_length / 2, 0)
Vertex_6 = geompy.MakeVertex(-csquare_length / 2, csquare_length / 2, 0)
Vertex_7 = geompy.MakeVertex(-csquare_length / 2, -csquare_length / 2, 0)
Vertex_8 = geompy.MakeVertex(csquare_length / 2, -csquare_length / 2, 0)


Arc_1 = geompy.MakeArcCenter(O, Vertex_2, Vertex_1,False)
Arc_1_vertex_3 = geompy.GetSubShape(Arc_1, [3])
Arc_2 = geompy.MakeArcCenter(O, Arc_1_vertex_3, Vertex_4,False)
Arc_2_vertex_3 = geompy.GetSubShape(Arc_2, [3])
Arc_3 = geompy.MakeArcCenter(O, Arc_2_vertex_3, Vertex_3,False)
Arc_3_vertex_3 = geompy.GetSubShape(Arc_3, [3])
Arc_1_vertex_2 = geompy.GetSubShape(Arc_1, [2])
Arc_4 = geompy.MakeArcCenter(O, Arc_3_vertex_3, Arc_1_vertex_2,False)

# Make vertices for the centers of the curvilignial square arcs
Cx1,Cy1 = arc_centers(geompy.PointCoordinates(Vertex_5)[0],geompy.PointCoordinates(Vertex_5)[1],
                            geompy.PointCoordinates(Vertex_6)[0],geompy.PointCoordinates(Vertex_6)[1],radius,(0,-1))
Cx2,Cy2 = arc_centers(geompy.PointCoordinates(Vertex_7)[0],geompy.PointCoordinates(Vertex_7)[1],
                            geompy.PointCoordinates(Vertex_8)[0],geompy.PointCoordinates(Vertex_8)[1],radius,(0,1))
Cx3,Cy3 = arc_centers(geompy.PointCoordinates(Vertex_6)[0],geompy.PointCoordinates(Vertex_6)[1],
                            geompy.PointCoordinates(Vertex_7)[0],geompy.PointCoordinates(Vertex_7)[1],radius,(1,0))
Cx4,Cy4 = arc_centers(geompy.PointCoordinates(Vertex_5)[0],geompy.PointCoordinates(Vertex_5)[1],
                            geompy.PointCoordinates(Vertex_8)[0],geompy.PointCoordinates(Vertex_8)[1],radius,(-1,0))

Vertex_9 = geompy.MakeVertex(Cx2, Cy2, 0)
Vertex_10 = geompy.MakeVertex(Cx1, Cy1, 0)
Vertex_11 = geompy.MakeVertex(Cx3, Cy3, 0)
Vertex_12 = geompy.MakeVertex(Cx4, Cy4, 0)

Arc_5 = geompy.MakeArcCenter(Vertex_9, Vertex_7, Vertex_8,False)
Arc_5_vertex_3 = geompy.GetSubShape(Arc_5, [3])
Arc_6 = geompy.MakeArcCenter(Vertex_12, Vertex_5, Arc_5_vertex_3,False)
Arc_5_vertex_2 = geompy.GetSubShape(Arc_5, [2])
Arc_7 = geompy.MakeArcCenter(Vertex_11, Arc_5_vertex_2, Vertex_6,False)
Arc_7_vertex_3 = geompy.GetSubShape(Arc_7, [3])
Arc_6_vertex_2 = geompy.GetSubShape(Arc_6, [2])
Arc_8 = geompy.MakeArcCenter(Vertex_10, Arc_7_vertex_3, Arc_6_vertex_2,False)
Arc_4_vertex_3 = geompy.GetSubShape(Arc_4, [3])
Line_1 = geompy.MakeLineTwoPnt(Arc_7_vertex_3, Arc_4_vertex_3)
Line_2 = geompy.MakeLineTwoPnt(Arc_6_vertex_2, Arc_1_vertex_3)
Arc_3_vertex_2 = geompy.GetSubShape(Arc_3, [2])
Line_3 = geompy.MakeLineTwoPnt(Arc_5_vertex_3, Arc_3_vertex_2)
Line_4 = geompy.MakeLineTwoPnt(Arc_5_vertex_2, Arc_3_vertex_3)
Face_1 = geompy.MakeFaceWires([Arc_1, Arc_8, Line_1, Line_2], 1)
Face_2 = geompy.MakeFaceWires([Arc_2, Arc_6, Line_2, Line_3], 1)
Face_3 = geompy.MakeFaceWires([Arc_3, Arc_5, Line_3, Line_4], 1)
Face_4 = geompy.MakeFaceWires([Arc_4, Arc_7, Line_1, Line_4], 1)
Face_5 = geompy.MakeFaceWires([Arc_5, Arc_6, Arc_7, Arc_8], 1)
Shell_1 = geompy.MakeShell([Face_1, Face_2, Face_3, Face_4, Face_5])
Inlet = geompy.CreateGroup(Shell_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(Inlet, [2, 12, 19, 26, 30])
Wall = geompy.CreateGroup(Shell_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(Wall, [7, 14, 21, 28])
[Inlet, Wall] = geompy.GetExistingSubObjects(Shell_1, False)
[Inlet, Wall] = geompy.GetExistingSubObjects(Shell_1, False)
[Inlet, Wall] = geompy.GetExistingSubObjects(Shell_1, False)
[Inlet, Wall] = geompy.GetExistingSubObjects(Shell_1, False)
[Inlet, Wall] = geompy.GetExistingSubObjects(Shell_1, False)
[Inlet, Wall] = geompy.GetExistingSubObjects(Shell_1, False)
[Inlet, Wall] = geompy.GetExistingSubObjects(Shell_1, False)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Vertex_3, 'Vertex_3' )
geompy.addToStudy( Vertex_2, 'Vertex_2' )
geompy.addToStudy( Vertex_1, 'Vertex_1' )
geompy.addToStudy( Arc_1, 'Arc_1' )
geompy.addToStudyInFather( Arc_1, Arc_1_vertex_2, 'Arc_1:vertex_2' )
geompy.addToStudyInFather( Arc_1, Arc_1_vertex_3, 'Arc_1:vertex_3' )
geompy.addToStudy( Vertex_9, 'Vertex_9' )
geompy.addToStudy( Vertex_10, 'Vertex_10' )
geompy.addToStudy( Vertex_4, 'Vertex_4' )
geompy.addToStudy( Arc_2, 'Arc_2' )
geompy.addToStudyInFather( Arc_2, Arc_2_vertex_3, 'Arc_2:vertex_3' )
geompy.addToStudy( Arc_3, 'Arc_3' )
geompy.addToStudyInFather( Arc_3, Arc_3_vertex_3, 'Arc_3:vertex_3' )
geompy.addToStudy( Arc_4, 'Arc_4' )
geompy.addToStudy( Vertex_7, 'Vertex_7' )
geompy.addToStudy( Vertex_12, 'Vertex_12' )
geompy.addToStudy( Vertex_8, 'Vertex_8' )
geompy.addToStudy( Arc_5, 'Arc_5' )
geompy.addToStudyInFather( Arc_5, Arc_5_vertex_2, 'Arc_5:vertex_2' )
geompy.addToStudy( Vertex_5, 'Vertex_5' )
geompy.addToStudyInFather( Arc_5, Arc_5_vertex_3, 'Arc_5:vertex_3' )
geompy.addToStudy( Vertex_11, 'Vertex_11' )
geompy.addToStudy( Vertex_6, 'Vertex_6' )
geompy.addToStudy( Arc_7, 'Arc_7' )
geompy.addToStudyInFather( Arc_7, Arc_7_vertex_3, 'Arc_7:vertex_3' )
geompy.addToStudy( Arc_6, 'Arc_6' )
geompy.addToStudyInFather( Arc_6, Arc_6_vertex_2, 'Arc_6:vertex_2' )
geompy.addToStudy( Arc_8, 'Arc_8' )
geompy.addToStudyInFather( Arc_4, Arc_4_vertex_3, 'Arc_4:vertex_3' )
geompy.addToStudy( Line_1, 'Line_1' )
geompy.addToStudy( Line_2, 'Line_2' )
geompy.addToStudyInFather( Arc_3, Arc_3_vertex_2, 'Arc_3:vertex_2' )
geompy.addToStudy( Line_3, 'Line_3' )
geompy.addToStudy( Line_4, 'Line_4' )
geompy.addToStudy( Face_1, 'Face_1' )
geompy.addToStudy( Face_2, 'Face_2' )
geompy.addToStudy( Face_3, 'Face_3' )
geompy.addToStudy( Face_4, 'Face_4' )
geompy.addToStudy( Face_5, 'Face_5' )
geompy.addToStudy( Shell_1, 'Shell_1' )
geompy.addToStudyInFather( Shell_1, Inlet, 'Inlet' )
geompy.addToStudyInFather( Shell_1, Wall, 'Wall' )

###
### SMESH component
###

import SMESH, SALOMEDS
from salome.smesh import smeshBuilder


import salome
import GEOM
import SMESH
from salome.smesh import smeshBuilder
import math

# smesh = smeshBuilder.New()

# height = 50

# n_xy_values = [1, 2,3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# results = []

# for n_xy in n_xy_values:
#     Mesh_1 = smesh.Mesh(Shell_1, f"Mesh_{n_xy}")

#     Regular_1D = Mesh_1.Segment()

#     # Segments pour le carré
#     NbSegXY = smesh.CreateHypothesis('NumberOfSegments')
#     NbSegXY.SetNumberOfSegments(15)

#     # Segments pour le bord du cylindre
#     NbSegRadial = smesh.CreateHypothesis('NumberOfSegments')
#     NbSegRadial.SetNumberOfSegments(n_xy) 
#     NbSegRadial.SetScaleFactor(2)

#     # Tri des arêtes
#     edges = geompy.ExtractShapes(Shell_1, geompy.ShapeType["EDGE"], True)
#     edges_carre = []
#     edges_cercle = []
#     edges_radiales = []

#     for e in edges:
#         vertices = geompy.ExtractShapes(e, geompy.ShapeType["VERTEX"], True)
#         v1, v2 = vertices[0], vertices[1]
#         x1, y1, z1 = geompy.PointCoordinates(v1)
#         x2, y2, z2 = geompy.PointCoordinates(v2)
#         r1 = math.hypot(x1, y1)
#         r2 = math.hypot(x2, y2)

#         if abs(r1 - r2) < 1e-6:
#             edges_cercle.append(e)
#         elif max(r1, r2) < 0.6 * max(r1, r2, r1, r2):
#             edges_carre.append(e)
#         else:
#             edges_radiales.append(e)

#     for e in edges_carre + edges_cercle:
#         Mesh_1.AddHypothesis(NbSegXY, e)

#     for e in edges_radiales:
#         Mesh_1.AddHypothesis(NbSegRadial, e)

#     Quadrangle_2D = Mesh_1.Quadrangle(algo=smeshBuilder.QUADRANGLE)
#     Inlet_1 = Mesh_1.GroupOnGeom(Inlet, 'Inlet', SMESH.FACE)
#     Wall_1 = Mesh_1.GroupOnGeom(Wall, 'Wall', SMESH.EDGE)

#     # Calcul du maillage
#     isDone = Mesh_1.Compute()
#     if not isDone:
#         print(f"Échec du maillage pour {n_xy} segments.")
#         continue

#     # Calcul de l’aspect ratio sur INLET 
#     inlet_group = None
#     for g in Mesh_1.GetGroups():
#         if g.GetName() == "Inlet":
#             inlet_group = g
#             break

#     if inlet_group is None:
#         raise ValueError("Le groupe 'Inlet' n'a pas été trouvé dans le maillage.")

#     inlet_ids = inlet_group.GetIDs()

#     ar_list = []
#     for elem_id in inlet_ids:
#         ar = Mesh_1.GetAspectRatio(elem_id)
#         if ar < 1.0:
#             ar = 1.0 / ar
#         ar_list.append(ar)

#     mean_ar = sum(ar_list) / len(ar_list)
#     results.append((n_xy, mean_ar))

# # Résumé final
# print("\nRésumé des résultats")
# for n_xy, mean_ar in results:
#     print(f"{n_xy} segments donne AR moyen = {mean_ar:.4f}")

# best = min(results, key=lambda x: x[1])
# print(f"\nNombre de segments optimal = {best[0]} (AR moyen = {best[1]:.4f})")


import salome
import GEOM
import SMESH
from salome.smesh import smeshBuilder
import math

smesh = smeshBuilder.New()

height = 50

# === Paramètres à tester ===
n_xy_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

results = []
meshes = {}  # pour stocker les maillages calculés

for n_xy in n_xy_values:

    # Création du maillage
    Mesh_1 = smesh.Mesh(Shell_1, f"Mesh_{n_xy}")
    Regular_1D = Mesh_1.Segment()

    # Segments sur carré/cercle
    NbSegXY = smesh.CreateHypothesis('NumberOfSegments')
    NbSegXY.SetNumberOfSegments(15)

    # Segments sur les rayons
    NbSegRadial = smesh.CreateHypothesis('NumberOfSegments')
    NbSegRadial.SetNumberOfSegments(n_xy)  
    NbSegRadial.SetScaleFactor(4)

    # Tri des arêtes
    edges = geompy.ExtractShapes(Shell_1, geompy.ShapeType["EDGE"], True)
    edges_carre = []
    edges_cercle = []
    edges_radiales = []

    for e in edges:
        vertices = geompy.ExtractShapes(e, geompy.ShapeType["VERTEX"], True)
        v1, v2 = vertices[0], vertices[1]
        x1, y1, z1 = geompy.PointCoordinates(v1)
        x2, y2, z2 = geompy.PointCoordinates(v2)
        r1 = math.hypot(x1, y1)
        r2 = math.hypot(x2, y2)

        if abs(r1 - r2) < 1e-6:
            edges_cercle.append(e)
        else:
            edges_radiales.append(e)

    for e in edges_carre + edges_cercle:
        Mesh_1.AddHypothesis(NbSegXY, e)

    for e in edges_radiales:
        Mesh_1.AddHypothesis(NbSegRadial, e)

    # 2D Quadrangles
    Quadrangle_2D = Mesh_1.Quadrangle(algo=smeshBuilder.QUADRANGLE)

    # Groupes géométriques
    Inlet_1 = Mesh_1.GroupOnGeom(Inlet, 'Inlet', SMESH.FACE)
    Wall_1 = Mesh_1.GroupOnGeom(Wall, 'Wall', SMESH.EDGE)

    # Calcul du maillage
    isDone = Mesh_1.Compute()
    if not isDone:
        print(f"Échec du maillage pour {n_xy} segments.")
        continue

    # Calcul de l’aspect ratio sur INLET
    inlet_group = None
    for g in Mesh_1.GetGroups():
        if g.GetName() == "Inlet":
            inlet_group = g
            break

    if inlet_group is None:
        print(f"Groupe 'Inlet' introuvable pour {n_xy} segments.")
        continue

    inlet_ids = inlet_group.GetIDs()

    ar_list = []
    for elem_id in inlet_ids:
        ar = Mesh_1.GetAspectRatio(elem_id)
        if ar < 1.0:
            ar = 1.0 / ar
        ar_list.append(ar)

    mean_ar = sum(ar_list) / len(ar_list)
    results.append((n_xy, mean_ar))
    meshes[n_xy] = Mesh_1


print("\nRésumé des résultats")
for n_xy, mean_ar in results:
    print(f"{n_xy} segments, AR moyen = {mean_ar:.4f}")

# Sélection du meilleur maillage
best = min(results, key=lambda x: x[1])
best_n_xy = best[0]
best_ar = best[1]
print(f"\nNombre de segments optimal = {best_n_xy} (AR moyen = {best_ar:.4f})")

# Suppression des autres maillages
for n_xy, mesh in meshes.items():
    if n_xy != best_n_xy:
        smesh.RemoveMesh(mesh)

# Renommage du meilleur maillage
Mesh_1 = meshes[best_n_xy]
Mesh_1.SetName("Mesh")

print("\nMaillage optimal conservé sous le nom 'Mesh'.")


# smesh = smeshBuilder.New()

# n_xy = 15
# height = 50

# Mesh_1 = smesh.Mesh(Shell_1, 'Mesh_1')

# # Hypothèses 1D
# Regular_1D = Mesh_1.Segment()

# # Deux hypothèses : 15 et 10 segments
# NbSeg15 = smesh.CreateHypothesis('NumberOfSegments')
# NbSeg15.SetNumberOfSegments(15)

# NbSeg13 = smesh.CreateHypothesis('NumberOfSegments')
# NbSeg13.SetNumberOfSegments(9)
# NbSeg13.SetScaleFactor(4)

# edges = geompy.ExtractShapes(Shell_1, geompy.ShapeType["EDGE"], True)

# edges_carre = []
# edges_cercle = []
# edges_radiales = []

# for e in edges:
#     vertices = geompy.ExtractShapes(e, geompy.ShapeType["VERTEX"], True)
#     v1, v2 = vertices[0], vertices[1]
    
#     x1, y1, z1 = geompy.PointCoordinates(v1)
#     x2, y2, z2 = geompy.PointCoordinates(v2)

#     r1 = (x1**2 + y1**2)**0.5
#     r2 = (x2**2 + y2**2)**0.5

#     if abs(r1 - r2) < 1e-6:
#         edges_cercle.append(e)
#     elif max(r1, r2) < 0.6 * max(r1, r2, r1, r2):
#         edges_carre.append(e)
#     else:
#         edges_radiales.append(e)


# for e in edges_carre + edges_cercle:
#     Mesh_1.AddHypothesis(NbSeg15, e)

# for e in edges_radiales:
#     Mesh_1.AddHypothesis(NbSeg13, e)

# Quadrangle_2D = Mesh_1.Quadrangle(algo=smeshBuilder.QUADRANGLE)
# Inlet_1 = Mesh_1.GroupOnGeom(Inlet, 'Inlet', SMESH.FACE)
# Wall_1 = Mesh_1.GroupOnGeom(Wall, 'Wall', SMESH.EDGE)
# isDone = Mesh_1.Compute()
# Mesh_1.CheckCompute()
# [Inlet_1, Wall_1] = Mesh_1.GetGroups()

# # Aspect Ratio statistics on INLET group
# inlet_group = Mesh_1.GroupOnGeom(Inlet, "INLET", SMESH.FACE)
# inlet_ids = inlet_group.GetIDs()
# ar_list = []

# for elem_id in inlet_ids:
#     ar = Mesh_1.GetAspectRatio(elem_id)
#     if ar < 1.0:
#         ar = 1.0 / ar
#     ar_list.append(ar)

# mean_ar = sum(ar_list) / len(ar_list)
# print("Aspect Ratio statistics for INLET group :")
# print("Mean Aspect Ratio =", mean_ar)
# print("AR Min =", min(ar_list), "\nAR Max =", max(ar_list))

# Extrusion
edge_length = math.pi * radius / 2 
mesh_size_xy = edge_length / n_xy
n_z = math.ceil(height / mesh_size_xy)
step_height = height / n_z

Mesh_1.ExtrusionSweepObjects( [ Mesh_1 ], [ Mesh_1 ], [ Mesh_1 ], [ 0, 0, step_height], n_z, 1, [  ], 1, [  ], [  ], 0 )







for grp in Mesh_1.GetGroups():
    if grp.GetType() == SMESH.EDGE:   
        Mesh_1.RemoveGroup(grp)
    elif grp.GetType() == SMESH.VOLUME:
        Mesh_1.RemoveGroup(grp)
if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
