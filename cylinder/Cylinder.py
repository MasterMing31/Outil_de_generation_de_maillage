import sys
import salome
import salome_notebook
from SketchAPI import *
from salome.shaper import model
import SHAPERSTUDY
import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS
import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder
import os

class Cylinder(object):
    """
    
    """

    def __init__(self, radius, height, square_length,n_seg_length, n_seg_axial, n_seg_circum,mesh_format,filename,output_dir):
        """ Initialize the attributes """
        self.radius = radius
        self.height = height
        self.square_length = square_length
        self.n_length = n_seg_length
        self.n_axial = n_seg_axial
        self.n_circum = n_seg_circum
        self.mesh_format = mesh_format
        self.filename = filename
        self.output_dir = output_dir

    def build_mesh(self):

        salome.salome_init()

        notebook = salome_notebook.NoteBook()
        sys.path.insert(0, r'D:/Université/Master_2/Projet numérique')

        ###
        ### SHAPER component
        ###

        model.begin()
        partSet = model.moduleDocument()

        ### Create Part
        Part_1 = model.addPart(partSet)
        Part_1_doc = Part_1.document()

        ### Create Cylinder
        Cylinder_1 = model.addCylinder(Part_1_doc, model.selection("VERTEX", "PartSet/Origin"), model.selection("EDGE", "PartSet/OZ"), self.radius, self.height)

        ### Create Rotation
        Rotation_1 = model.addRotation(Part_1_doc, [model.selection("SOLID", "Cylinder_1_1")], axis = model.selection("EDGE", "PartSet/OZ"), angle = 45, keepSubResults = True)

        ### Create Sketch
        Sketch_1 = model.addSketch(Part_1_doc, model.selection("FACE", "Rotation_1_1/MF:Rotated&Cylinder_1_1/Face_2"))

        ### Create SketchLine
        SketchLine_1 = Sketch_1.addLine(self.square_length/2, -self.square_length/2, -self.square_length/2, -self.square_length/2)

        ### Create SketchProjection
        SketchProjection_1 = Sketch_1.addProjection(model.selection("VERTEX", "[Rotation_1_1/MF:Rotated&Cylinder_1_1/Face_1][Rotation_1_1/MF:Rotated&Cylinder_1_1/Face_2]__cc"), False)
        SketchPoint_1 = SketchProjection_1.createdFeature()

        ### Create SketchLine
        SketchLine_2 = Sketch_1.addLine(-self.square_length/2, -self.square_length/2, -self.square_length/2, self.square_length/2)

        ### Create SketchLine
        SketchLine_3 = Sketch_1.addLine(-self.square_length/2, self.square_length/2, self.square_length/2, self.square_length/2)

        ### Create SketchLine
        SketchLine_4 = Sketch_1.addLine(self.square_length/2, self.square_length/2, self.square_length/2, -self.square_length/2)
        Sketch_1.setCoincident(SketchLine_4.endPoint(), SketchLine_1.startPoint(), True)
        Sketch_1.setCoincident(SketchLine_1.endPoint(), SketchLine_2.startPoint(), True)
        Sketch_1.setCoincident(SketchLine_2.endPoint(), SketchLine_3.startPoint(), True)
        Sketch_1.setCoincident(SketchLine_3.endPoint(), SketchLine_4.startPoint(), True)

        ### Create SketchLine
        SketchLine_5 = Sketch_1.addLine(self.square_length/2, -self.square_length/2, -self.square_length/2, self.square_length/2)
        SketchLine_5.setAuxiliary(True)

        ### Create SketchLine
        SketchLine_6 = Sketch_1.addLine(-self.square_length/2, -self.square_length/2, self.square_length/2, self.square_length/2)
        SketchLine_6.setAuxiliary(True)
        Sketch_1.setCoincident(SketchLine_1.startPoint(), SketchLine_5.startPoint(), True)
        Sketch_1.setCoincident(SketchLine_2.startPoint(), SketchLine_6.startPoint(), True)
        Sketch_1.setCoincident(SketchLine_3.startPoint(), SketchLine_5.endPoint(), True)
        Sketch_1.setCoincident(SketchLine_4.startPoint(), SketchLine_6.endPoint(), True)

        ### Create SketchPoint
        SketchPoint_2 = Sketch_1.addPoint(0, 0)
        SketchPoint_2.setAuxiliary(True)
        Sketch_1.setCoincident(SketchAPI_Point(SketchPoint_1).coordinates(), SketchPoint_2, True)
        Sketch_1.setCoincident(SketchPoint_2.coordinates(), SketchLine_5.result(), True)
        Sketch_1.setCoincident(SketchPoint_2.coordinates(), SketchLine_6.result(), True)
        Sketch_1.setPerpendicular(SketchLine_1.result(), SketchLine_2.result(), True)
        Sketch_1.setPerpendicular(SketchLine_2.result(), SketchLine_3.result(), True)
        Sketch_1.setPerpendicular(SketchLine_3.result(), SketchLine_4.result(), True)
        Sketch_1.setHorizontalDistance(SketchLine_2.endPoint(), SketchPoint_2.coordinates(), self.square_length/2, True)
        Sketch_1.setHorizontalDistance(SketchLine_4.startPoint(), SketchPoint_2.coordinates(), self.square_length/2, True)
        Sketch_1.setVerticalDistance(SketchLine_4.startPoint(), SketchPoint_2.coordinates(), self.square_length/2, True)
        model.do()

        ### Create Extrusion
        Extrusion_1 = model.addExtrusion(Part_1_doc, [model.selection("COMPOUND", "Sketch_1")], model.selection(), 0, self.height, "Faces|Wires")

        ### Create Smash
        Smash_1 = model.addSmash(Part_1_doc, [model.selection("SOLID", "Rotation_1_1")], [model.selection("SOLID", "Extrusion_1_1")], keepSubResults = True)

        ### Create Plane
        Plane_4 = model.addPlane(Part_1_doc, model.selection("FACE", "PartSet/YOZ"), model.selection("EDGE", "PartSet/OZ"), 45)

        ### Create Plane
        Plane_5 = model.addPlane(Part_1_doc, model.selection("FACE", "PartSet/YOZ"), model.selection("EDGE", "PartSet/OZ"), 135)

        ### Create Split
        Split_1 = model.addSplit(Part_1_doc, [model.selection("SOLID", "Smash_1_1_1")], [model.selection("FACE", "Plane_2"), model.selection("FACE", "Plane_1")], keepSubResults = True)

        ### Create Group
        Group_1_objects = [model.selection("FACE", "Split_1_1_3/Modified_Face&Cylinder_1_1/Face_1"),
                        model.selection("FACE", "Split_1_1_2/Modified_Face&Cylinder_1_1/Face_1"),
                        model.selection("FACE", "Split_1_1_4/Modified_Face&Cylinder_1_1/Face_1"),
                        model.selection("FACE", "Split_1_1_5/Modified_Face&Cylinder_1_1/Face_1")]
        Group_1 = model.addGroup(Part_1_doc, "Faces", Group_1_objects)
        Group_1.setName("Walls")
        Group_1.result().setName("Walls")

        ### Create Group
        Group_2_objects = [model.selection("FACE", "Split_1_1_4/Modified_Face&Cylinder_1_1/Face_2"),
                        model.selection("FACE", "Split_1_1_5/Modified_Face&Cylinder_1_1/Face_2"),
                        model.selection("FACE", "Split_1_1_3/Modified_Face&Cylinder_1_1/Face_2"),
                        model.selection("FACE", "Split_1_1_2/Modified_Face&Cylinder_1_1/Face_2"),
                        model.selection("FACE", "Extrusion_1_1/To_Face")]
        Group_2 = model.addGroup(Part_1_doc, "Faces", Group_2_objects)
        Group_2.setName("Outlet")
        Group_2.result().setName("Outlet")

        ### Create Group
        Group_3_objects = [model.selection("FACE", "Split_1_1_3/Modified_Face&Cylinder_1_1/Face_3"),
                        model.selection("FACE", "Split_1_1_5/Modified_Face&Cylinder_1_1/Face_3"),
                        model.selection("FACE", "Split_1_1_4/Modified_Face&Cylinder_1_1/Face_3"),
                        model.selection("FACE", "Split_1_1_2/Modified_Face&Cylinder_1_1/Face_3"),
                        model.selection("FACE", "Extrusion_1_1/From_Face")]
        Group_3 = model.addGroup(Part_1_doc, "Faces", Group_3_objects)
        Group_3.setName("Inlet")
        Group_3.result().setName("Inlet")

        ### Create Group
        Group_4_objects = [model.selection("EDGE", "Split_1_1_2/Generated_Edge&Plane_1/Plane_1&Cylinder_1_1/Face_1"),
                        model.selection("EDGE", "[Split_1_1_5/Modified_Face&Cylinder_1_1/Face_1][Split_1_1_5/Modified_Face&Plane_2/Plane_2]"),
                        model.selection("EDGE", "Split_1_1_5/Generated_Edge&Plane_1/Plane_1&Cylinder_1_1/Face_1"),
                        model.selection("EDGE", "Split_1_1_2/Generated_Edge&Plane_2/Plane_2&Cylinder_1_1/Face_1"),
                        model.selection("EDGE", "[Extrusion_1_1/Generated_Face&Sketch_1/SketchLine_3][Extrusion_1_1/Generated_Face&Sketch_1/SketchLine_2]"),
                        model.selection("EDGE", "[Split_1_1_5/Modified_Face&Plane_2/Plane_2][Extrusion_1_1/Generated_Face&Sketch_1/SketchLine_4]"),
                        model.selection("EDGE", "[Split_1_1_5/Modified_Face&Plane_1/Plane_1][Extrusion_1_1/Generated_Face&Sketch_1/SketchLine_4]"),
                        model.selection("EDGE", "[Extrusion_1_1/Generated_Face&Sketch_1/SketchLine_2][Extrusion_1_1/Generated_Face&Sketch_1/SketchLine_1]")]
        Group_4 = model.addGroup(Part_1_doc, "Edges", Group_4_objects)
        Group_4.setName("n_length")
        Group_4.result().setName("n_length")

        ### Create Group
        Group_5_objects = [model.selection("EDGE", "[Split_1_1_4/Modified_Face&Cylinder_1_1/Face_3][Extrusion_1_1/Generated_Face&Sketch_1/SketchLine_3]"),
                        model.selection("EDGE", "[Extrusion_1_1/Generated_Face&Sketch_1/SketchLine_2][Extrusion_1_1/From_Face]"),
                        model.selection("EDGE", "[Extrusion_1_1/Generated_Face&Sketch_1/SketchLine_1][Extrusion_1_1/From_Face]"),
                        model.selection("EDGE", "[Extrusion_1_1/Generated_Face&Sketch_1/SketchLine_4][Extrusion_1_1/From_Face]"),
                        model.selection("EDGE", "[Split_1_1_5/Modified_Face&Cylinder_1_1/Face_1][Split_1_1_5/Modified_Face&Cylinder_1_1/Face_3]"),
                        model.selection("EDGE", "[Split_1_1_4/Modified_Face&Cylinder_1_1/Face_1][Split_1_1_4/Modified_Face&Cylinder_1_1/Face_3]"),
                        model.selection("EDGE", "[Split_1_1_2/Modified_Face&Cylinder_1_1/Face_1][Split_1_1_2/Modified_Face&Cylinder_1_1/Face_3]"),
                        model.selection("EDGE", "[Split_1_1_3/Modified_Face&Cylinder_1_1/Face_1][Split_1_1_3/Modified_Face&Cylinder_1_1/Face_3]"),
                        model.selection("EDGE", "[Split_1_1_4/Modified_Face&Cylinder_1_1/Face_1][Split_1_1_4/Modified_Face&Cylinder_1_1/Face_2]"),
                        model.selection("EDGE", "[Split_1_1_5/Modified_Face&Cylinder_1_1/Face_1][Split_1_1_5/Modified_Face&Cylinder_1_1/Face_2]"),
                        model.selection("EDGE", "[Split_1_1_3/Modified_Face&Cylinder_1_1/Face_1][Split_1_1_3/Modified_Face&Cylinder_1_1/Face_2]"),
                        model.selection("EDGE", "[Split_1_1_2/Modified_Face&Cylinder_1_1/Face_1][Split_1_1_2/Modified_Face&Cylinder_1_1/Face_2]"),
                        model.selection("EDGE", "[Extrusion_1_1/Generated_Face&Sketch_1/SketchLine_3][Extrusion_1_1/To_Face]"),
                        model.selection("EDGE", "[Extrusion_1_1/Generated_Face&Sketch_1/SketchLine_4][Extrusion_1_1/To_Face]"),
                        model.selection("EDGE", "[Extrusion_1_1/Generated_Face&Sketch_1/SketchLine_2][Extrusion_1_1/To_Face]"),
                        model.selection("EDGE", "[Extrusion_1_1/Generated_Face&Sketch_1/SketchLine_1][Extrusion_1_1/To_Face]")]
        Group_5 = model.addGroup(Part_1_doc, "Edges", Group_5_objects)
        Group_5.setName("n_circum")
        Group_5.result().setName("n_circum")

        ### Create Group
        Group_6_objects = [model.selection("EDGE", "Split_1_1_4/Generated_Edge&Plane_2/Plane_2&Cylinder_1_1/Face_3"),
                        model.selection("EDGE", "Split_1_1_2/Generated_Edge&Plane_1/Plane_1&Cylinder_1_1/Face_3"),
                        model.selection("EDGE", "Split_1_1_2/Generated_Edge&Plane_2/Plane_2&Cylinder_1_1/Face_3"),
                        model.selection("EDGE", "Split_1_1_5/Generated_Edge&Plane_1/Plane_1&Cylinder_1_1/Face_3"),
                        model.selection("EDGE", "Split_1_1_2/Generated_Edge&Plane_2/Plane_2&Cylinder_1_1/Face_2"),
                        model.selection("EDGE", "Split_1_1_5/Generated_Edge&Plane_1/Plane_1&Cylinder_1_1/Face_2"),
                        model.selection("EDGE", "Split_1_1_2/Generated_Edge&Plane_1/Plane_1&Cylinder_1_1/Face_2"),
                        model.selection("EDGE", "Split_1_1_5/Generated_Edge&Plane_2/Plane_2&Cylinder_1_1/Face_2")]
        Group_6 = model.addGroup(Part_1_doc, "Edges", Group_6_objects)
        Group_6.setName("n_axial")
        Group_6.result().setName("n_axial")

        model.end()

        ###
        ### SHAPERSTUDY component
        ###

        model.publishToShaperStudy()

        Split_1_1, Walls, Outlet, Inlet, n_length, n_circum, n_axial, = SHAPERSTUDY.shape(model.featureStringId(Split_1))
        ###
        ### GEOM component
        ###

        geompy = geomBuilder.New()

        O = geompy.MakeVertex(0, 0, 0)
        OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
        OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
        OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
        geompy.addToStudy( O, 'O' )
        geompy.addToStudy( OX, 'OX' )
        geompy.addToStudy( OY, 'OY' )
        geompy.addToStudy( OZ, 'OZ' )

        ###
        ### SMESH component
        ###

        smesh = smeshBuilder.New()
        #smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                        # multiples meshes built in parallel, complex and numerous mesh edition (performance)

        try:
            pass
        except:
            print('ExportSTL() failed. Invalid file name?')
        Mesh_1 = smesh.Mesh(Split_1_1,'Mesh_1')
        Regular_1D = Mesh_1.Segment()
        Number_of_Segments_1 = Regular_1D.NumberOfSegments(15) ##CHECK
        Quadrangle_2D = Mesh_1.Quadrangle(algo=smeshBuilder.QUADRANGLE)
        Hexa_3D = Mesh_1.Hexahedron(algo=smeshBuilder.Hexa)
        Walls_1 = Mesh_1.GroupOnGeom(Walls,'Walls',SMESH.FACE)
        Outlet_1 = Mesh_1.GroupOnGeom(Outlet,'Outlet',SMESH.FACE)
        Inlet_1 = Mesh_1.GroupOnGeom(Inlet,'Inlet',SMESH.FACE)
        n_length_1 = Mesh_1.GroupOnGeom(n_length,'n_length',SMESH.EDGE)
        n_circum_1 = Mesh_1.GroupOnGeom(n_circum,'n_circum',SMESH.EDGE)
        n_axial_1 = Mesh_1.GroupOnGeom(n_axial,'n_axial',SMESH.EDGE)
        Regular_1D_1 = Mesh_1.Segment(geom=n_length)
        n_length_2 = Regular_1D_1.NumberOfSegments(self.n_length)
        Regular_1D_2 = Mesh_1.Segment(geom=n_circum)
        n_circum_2 = Regular_1D_2.NumberOfSegments(self.n_circum)
        Regular_1D_3 = Mesh_1.Segment(geom=n_axial)
        n_axial_2 = Regular_1D_3.NumberOfSegments(self.n_axial)
        isDone = Mesh_1.Compute()
        Mesh_1.CheckCompute()
        [ Walls_1, Outlet_1, Inlet_1, n_length_1, n_circum_1, n_axial_1 ] = Mesh_1.GetGroups()
        n_length_3 = Regular_1D_1.GetSubMesh()
        n_circum_3 = Regular_1D_2.GetSubMesh()
        Sub_mesh_1 = Regular_1D_3.GetSubMesh()


        ## Set names of Mesh objects
        smesh.SetName(n_axial_1, 'n_axial')
        smesh.SetName(Sub_mesh_1, 'Sub-mesh_1')
        smesh.SetName(Number_of_Segments_1, 'Number of Segments_1')
        smesh.SetName(Hexa_3D.GetAlgorithm(), 'Hexa_3D')
        smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
        smesh.SetName(Quadrangle_2D.GetAlgorithm(), 'Quadrangle_2D')
        smesh.SetName(n_circum_1, 'n_circum')
        smesh.SetName(Walls_1, 'Walls')
        smesh.SetName(n_circum_2, 'n_circum')
        smesh.SetName(n_length_2, 'n_length')
        smesh.SetName(Inlet_1, 'Inlet')
        smesh.SetName(n_length_3, 'n_length')
        smesh.SetName(n_axial_2, 'n_axial')
        smesh.SetName(Outlet_1, 'Outlet')
        smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
        smesh.SetName(n_circum_3, 'n_circum')
        smesh.SetName(n_length_1, 'n_length')

        # === EXPORT MESH TO FILE ===

        # Choose export directory and file name
        output_dir = self.output_dir
        filename = self.filename
        os.makedirs(output_dir, exist_ok=True)

        if self.mesh_format == "med":
            export_path = os.path.join(output_dir, self.filename +".med")
            Mesh_1.ExportMED(export_path, auto_groups=True, minor=40)
            print(f"Mesh exported to: {export_path}")
        
        elif self.mesh_format == "unv":
            export_path = os.path.join(output_dir, self.filename +".unv")
            Mesh_1.ExportUNV(export_path)
            print(f"Mesh exported to: {export_path}")

        elif self.mesh_format == "stl":
            export_path = os.path.join(output_dir,self.filename + ".stl")
            Mesh_1.ExportSTL(export_path)
            print(f"Mesh exported to: {export_path}")

        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser()


