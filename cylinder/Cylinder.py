import sys
import salome
import salome_notebook
import os
from SketchAPI import *
from salome.shaper import model
import SHAPERSTUDY
import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

class Cylinder(object):
    """
    
    """

    def __init__(self, radius, height, curv_square_length,curv_square_radius,n_seg,z_steps,mesh_format,filename,output_dir):
        """ Initialize the attributes """
        self.radius = radius
        self.height = height
    
        self.csquare_length = curv_square_length
        self.csquare_radius = curv_square_radius

        self.n_seg = n_seg ## Change to number of cells once figure out how
        self.z_steps = z_steps

        self.mesh_format = mesh_format
        self.filename = filename
        self.output_dir = output_dir

    def build_mesh(self):

        #!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.15.0 with dump python functionality
###


        salome.salome_init()
        
        notebook = salome_notebook.NoteBook()
        sys.path.insert(0, r'D:/Universite/Master_2/Projet num')

        ###
        ### SHAPER component
        ###


        model.begin()
        partSet = model.moduleDocument()

        ### Create Part
        Part_1 = model.addPart(partSet)
        Part_1_doc = Part_1.document()

        ### Create Sketch
        Sketch_1 = model.addSketch(Part_1_doc, model.standardPlane("XOY"))

        ### Create SketchProjection
        SketchProjection_1 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
        SketchPoint_1 = SketchProjection_1.createdFeature()

        # Create the curvilinial square vertices
        ### Create SketchPoint
        SketchPoint_2 = Sketch_1.addPoint(-self.csquare_length/2, self.csquare_length/2)
        SketchPoint_2.setName("SketchPoint_14")
        SketchPoint_2.result().setName("SketchPoint_14")

        ### Create SketchPoint
        SketchPoint_3 = Sketch_1.addPoint(self.csquare_length/2, self.csquare_length/2)
        SketchPoint_3.setName("SketchPoint_15")
        SketchPoint_3.result().setName("SketchPoint_15")

        ### Create SketchPoint
        SketchPoint_4 = Sketch_1.addPoint(-self.csquare_length/2, -self.csquare_length/2)
        SketchPoint_4.setName("SketchPoint_16")
        SketchPoint_4.result().setName("SketchPoint_16")

        ### Create SketchPoint
        SketchPoint_5 = Sketch_1.addPoint(self.csquare_length/2, -self.csquare_length/2)
        SketchPoint_5.setName("SketchPoint_17")
        SketchPoint_5.result().setName("SketchPoint_17")

        #############################################
        # Set constraints for the curvilinial square vertices
        ### Create SketchProjection
        SketchProjection_2 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
        SketchProjection_2.setName("SketchProjection_10")
        SketchProjection_2.result().setName("SketchProjection_10")
        SketchPoint_6 = SketchProjection_2.createdFeature()
        SketchPoint_6.setName("SketchPoint_18")
        SketchPoint_6.result().setName("SketchPoint_18")
        Sketch_1.setHorizontalDistance(SketchAPI_Point(SketchPoint_6).coordinates(), SketchPoint_3.coordinates(), self.csquare_length/2, True)

        ### Create SketchProjection
        SketchProjection_3 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
        SketchProjection_3.setName("SketchProjection_11")
        SketchProjection_3.result().setName("SketchProjection_11")
        SketchPoint_7 = SketchProjection_3.createdFeature()
        SketchPoint_7.setName("SketchPoint_19")
        SketchPoint_7.result().setName("SketchPoint_19")
        Sketch_1.setVerticalDistance(SketchAPI_Point(SketchPoint_7).coordinates(), SketchPoint_3.coordinates(), self.csquare_length/2, True)

        ### Create SketchProjection
        SketchProjection_4 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
        SketchProjection_4.setName("SketchProjection_12")
        SketchProjection_4.result().setName("SketchProjection_12")
        SketchPoint_8 = SketchProjection_4.createdFeature()
        SketchPoint_8.setName("SketchPoint_20")
        SketchPoint_8.result().setName("SketchPoint_20")
        Sketch_1.setHorizontalDistance(SketchAPI_Point(SketchPoint_8).coordinates(), SketchPoint_2.coordinates(), self.csquare_length/2, True)

        ### Create SketchProjection
        SketchProjection_5 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
        SketchProjection_5.setName("SketchProjection_13")
        SketchProjection_5.result().setName("SketchProjection_13")
        SketchPoint_9 = SketchProjection_5.createdFeature()
        SketchPoint_9.setName("SketchPoint_21")
        SketchPoint_9.result().setName("SketchPoint_21")
        Sketch_1.setVerticalDistance(SketchAPI_Point(SketchPoint_9).coordinates(), SketchPoint_2.coordinates(), self.csquare_length/2, True)

        ### Create SketchProjection
        SketchProjection_6 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
        SketchProjection_6.setName("SketchProjection_14")
        SketchProjection_6.result().setName("SketchProjection_14")
        SketchPoint_10 = SketchProjection_6.createdFeature()
        SketchPoint_10.setName("SketchPoint_22")
        SketchPoint_10.result().setName("SketchPoint_22")
        Sketch_1.setHorizontalDistance(SketchAPI_Point(SketchPoint_10).coordinates(), SketchPoint_4.coordinates(), self.csquare_length/2, True)

        ### Create SketchProjection
        SketchProjection_7 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
        SketchProjection_7.setName("SketchProjection_15")
        SketchProjection_7.result().setName("SketchProjection_15")
        SketchPoint_11 = SketchProjection_7.createdFeature()
        SketchPoint_11.setName("SketchPoint_23")
        SketchPoint_11.result().setName("SketchPoint_23")
        Sketch_1.setVerticalDistance(SketchAPI_Point(SketchPoint_11).coordinates(), SketchPoint_4.coordinates(), self.csquare_length/2, True)

        ### Create SketchProjection
        SketchProjection_8 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
        SketchProjection_8.setName("SketchProjection_16")
        SketchProjection_8.result().setName("SketchProjection_16")
        SketchPoint_12 = SketchProjection_8.createdFeature()
        SketchPoint_12.setName("SketchPoint_24")
        SketchPoint_12.result().setName("SketchPoint_24")
        Sketch_1.setHorizontalDistance(SketchAPI_Point(SketchPoint_12).coordinates(), SketchPoint_5.coordinates(), self.csquare_length/2, True)

        ### Create SketchProjection
        SketchProjection_9 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
        SketchProjection_9.setName("SketchProjection_17")
        SketchProjection_9.result().setName("SketchProjection_17")
        SketchPoint_13 = SketchProjection_9.createdFeature()
        SketchPoint_13.setName("SketchPoint_25")
        SketchPoint_13.result().setName("SketchPoint_25")
        Sketch_1.setVerticalDistance(SketchAPI_Point(SketchPoint_13).coordinates(), SketchPoint_5.coordinates(), self.csquare_length/2, True)

        ####################################################

        # Set the arc and radius for the curvilinial square
        ### Create SketchArc
        SketchArc_1 = Sketch_1.addArc(-5.733939980868607e-16, -2.29198715887567, -self.csquare_length/2, self.csquare_length/2, self.csquare_length/2, self.csquare_length/2, True)
        SketchArc_1.setName("SketchArc_5")
        SketchArc_1.result().setName("SketchArc_5")
        SketchArc_1.results()[1].setName("SketchArc_5_2")
        Sketch_1.setCoincident(SketchPoint_2.coordinates(), SketchArc_1.startPoint(), True)
        Sketch_1.setCoincident(SketchPoint_3.coordinates(), SketchArc_1.endPoint(), True)
        Sketch_1.setRadius(SketchArc_1.results()[1], self.csquare_radius, True)

        ### Create SketchArc
        SketchArc_2 = Sketch_1.addArc(-2.291987158875422, 1.891994880818345e-15, self.csquare_length/2, self.csquare_length/2, self.csquare_length/2, -self.csquare_length/2, True)
        SketchArc_2.setName("SketchArc_6")
        SketchArc_2.result().setName("SketchArc_6")
        SketchArc_2.results()[1].setName("SketchArc_6_2")
        Sketch_1.setCoincident(SketchPoint_3.coordinates(), SketchArc_2.startPoint(), True)
        Sketch_1.setCoincident(SketchPoint_5.coordinates(), SketchArc_2.endPoint(), True)
        Sketch_1.setRadius(SketchArc_2.results()[1], self.csquare_radius, True)

        ### Create SketchArc
        SketchArc_3 = Sketch_1.addArc(8.953868408940558e-16, 2.291987158875422, self.csquare_length/2, -self.csquare_length/2, -self.csquare_length/2, -self.csquare_length/2, True)
        SketchArc_3.setName("SketchArc_7")
        SketchArc_3.result().setName("SketchArc_7")
        SketchArc_3.results()[1].setName("SketchArc_7_2")
        Sketch_1.setCoincident(SketchPoint_5.coordinates(), SketchArc_3.startPoint(), True)
        Sketch_1.setCoincident(SketchPoint_4.coordinates(), SketchArc_3.endPoint(), True)
        Sketch_1.setRadius(SketchArc_3.results()[1], self.csquare_radius, True)

        ### Create SketchArc
        SketchArc_4 = Sketch_1.addArc(2.291987158875422, 6.563282325410143e-16, -self.csquare_length/2, -self.csquare_length/2, -self.csquare_length/2, self.csquare_length/2, True)
        SketchArc_4.setName("SketchArc_8")
        SketchArc_4.result().setName("SketchArc_8")
        SketchArc_4.results()[1].setName("SketchArc_8_2")
        Sketch_1.setCoincident(SketchPoint_4.coordinates(), SketchArc_4.startPoint(), True)
        Sketch_1.setCoincident(SketchPoint_2.coordinates(), SketchArc_4.endPoint(), True)
        Sketch_1.setRadius(SketchArc_4.results()[1], self.csquare_radius, True)
        ##########################################################################
        
        ## Create the lines going from the vertices of the curvilignial squre
        ### Create SketchLine
        SketchLine_1 = Sketch_1.addLine(-self.csquare_length/2, self.csquare_length/2, -0.7071067811865476, 0.7071067811865475)
        Sketch_1.setCoincident(SketchPoint_2.coordinates(), SketchLine_1.startPoint(), True)


        ### Create SketchConstraintAngle
        SketchProjection_10 = Sketch_1.addProjection(model.selection("EDGE", "PartSet/OX"), False)
        SketchProjection_10.setName("SketchProjection_18")
        SketchProjection_10.result().setName("SketchProjection_18")

        ### Create SketchConstraintAngle
        SketchLine_2 = SketchProjection_10.createdFeature()

        ### Create SketchConstraintAngle
        Sketch_1.setAngle(SketchLine_1.result(), SketchLine_2.result(), 135, type = "Direct", is_active = True)

        ### Create SketchLine
        SketchLine_3 = Sketch_1.addLine(self.csquare_length/2, self.csquare_length/2, 0.7071067811865476, 0.7071067811865476)
        Sketch_1.setCoincident(SketchPoint_3.coordinates(), SketchLine_3.startPoint(), True)

        ### Create SketchConstraintAngle
        Sketch_1.setAngle(SketchLine_3.result(), SketchLine_2.result(), 45, type = "Direct", is_active = True)

        ### Create SketchLine
        SketchLine_4 = Sketch_1.addLine(-self.csquare_length/2, -self.csquare_length/2, -0.7071067811865474, -0.7071067811865475)
        Sketch_1.setCoincident(SketchPoint_4.coordinates(), SketchLine_4.startPoint(), True)

        ### Create SketchConstraintAngle
        Sketch_1.setAngle(SketchLine_4.result(), SketchLine_2.result(), 135, type = "Direct", is_active = True)

        ### Create SketchLine
        SketchLine_5 = Sketch_1.addLine(self.csquare_length/2, -self.csquare_length/2, 0.7071067811865476, -0.7071067811865476)
        Sketch_1.setCoincident(SketchPoint_5.coordinates(), SketchLine_5.startPoint(), True)

        ### Create SketchConstraintAngle
        Sketch_1.setAngle(SketchLine_5.result(), SketchLine_2.result(), 45, type = "Direct", is_active = True)
        Sketch_1.setEqual(SketchLine_3.result(), SketchLine_1.result(), True)
        Sketch_1.setEqual(SketchLine_4.result(), SketchLine_5.result(), True)
        Sketch_1.setEqual(SketchLine_4.result(), SketchLine_1.result(), True)

        ### Create SketchArc
        SketchArc_5 = Sketch_1.addArc(-2.72489300910411e-18, 0, -0.7071067811865476, 0.7071067811865475, 0.7071067811865476, 0.7071067811865476, True)
        SketchArc_5.setName("SketchArc_9")
        SketchArc_5.result().setName("SketchArc_9")
        SketchArc_5.results()[1].setName("SketchArc_9_2")
        Sketch_1.setCoincident(SketchLine_1.endPoint(), SketchArc_5.startPoint(), True)
        Sketch_1.setCoincident(SketchLine_3.endPoint(), SketchArc_5.endPoint(), True)

        ### Create SketchProjection
        SketchProjection_11 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
        SketchProjection_11.setName("SketchProjection_19")
        SketchProjection_11.result().setName("SketchProjection_19")
        SketchPoint_14 = SketchProjection_11.createdFeature()
        SketchPoint_14.setName("SketchPoint_26")
        SketchPoint_14.result().setName("SketchPoint_26")
        Sketch_1.setVerticalDistance(SketchArc_5.center(), SketchAPI_Point(SketchPoint_14).coordinates(), 0, True)

        ### Create SketchArc
        SketchArc_6 = Sketch_1.addArc(0, 1.293637058843693e-16, 0.7071067811865476, 0.7071067811865476, 0.7071067811865476, -0.7071067811865476, True)
        SketchArc_6.setName("SketchArc_10")
        SketchArc_6.result().setName("SketchArc_10")
        SketchArc_6.results()[1].setName("SketchArc_10_2")
        Sketch_1.setCoincident(SketchLine_3.endPoint(), SketchArc_6.startPoint(), True)
        Sketch_1.setCoincident(SketchLine_5.endPoint(), SketchArc_6.endPoint(), True)

        ### Create SketchProjection
        SketchProjection_12 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
        SketchProjection_12.setName("SketchProjection_20")
        SketchProjection_12.result().setName("SketchProjection_20")
        SketchPoint_15 = SketchProjection_12.createdFeature()
        SketchPoint_15.setName("SketchPoint_27")
        SketchPoint_15.result().setName("SketchPoint_27")
        Sketch_1.setHorizontalDistance(SketchArc_6.center(), SketchAPI_Point(SketchPoint_15).coordinates(), 0, True)

        ### Create SketchArc
        SketchArc_7 = Sketch_1.addArc(-1.525065881249787e-17, 0, 0.7071067811865476, -0.7071067811865476, -0.7071067811865474, -0.7071067811865475, True)
        SketchArc_7.setName("SketchArc_11")
        SketchArc_7.result().setName("SketchArc_11")
        SketchArc_7.results()[1].setName("SketchArc_11_2")
        Sketch_1.setCoincident(SketchLine_5.endPoint(), SketchArc_7.startPoint(), True)
        Sketch_1.setCoincident(SketchLine_4.endPoint(), SketchArc_7.endPoint(), True)

        ### Create SketchProjection
        SketchProjection_13 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
        SketchProjection_13.setName("SketchProjection_21")
        SketchProjection_13.result().setName("SketchProjection_21")
        SketchPoint_16 = SketchProjection_13.createdFeature()
        SketchPoint_16.setName("SketchPoint_28")
        SketchPoint_16.result().setName("SketchPoint_28")
        Sketch_1.setVerticalDistance(SketchArc_7.center(), SketchAPI_Point(SketchPoint_16).coordinates(), 0, True)

        ### Create SketchArc
        SketchArc_8 = Sketch_1.addArc(0, -5.717588927655604e-17, -0.7071067811865474, -0.7071067811865475, -0.7071067811865476, 0.7071067811865475, True)
        SketchArc_8.setName("SketchArc_12")
        SketchArc_8.result().setName("SketchArc_12")
        SketchArc_8.results()[1].setName("SketchArc_12_2")
        Sketch_1.setCoincident(SketchLine_4.endPoint(), SketchArc_8.startPoint(), True)
        Sketch_1.setCoincident(SketchLine_1.endPoint(), SketchArc_8.endPoint(), True)

        ### Create SketchProjection
        SketchProjection_14 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
        SketchProjection_14.setName("SketchProjection_22")
        SketchProjection_14.result().setName("SketchProjection_22")
        SketchPoint_17 = SketchProjection_14.createdFeature()
        SketchPoint_17.setName("SketchPoint_29")
        SketchPoint_17.result().setName("SketchPoint_29")
        Sketch_1.setHorizontalDistance(SketchArc_8.center(), SketchAPI_Point(SketchPoint_17).coordinates(), 0, True)
        Sketch_1.setRadius(SketchArc_8.results()[1], self.radius, True)
        model.do()

        ### Create Face
        Face_1 = model.addFace(Part_1_doc, [model.selection("FACE", "Sketch_1/Face-SketchLine_3f-SketchArc_9_2f-SketchLine_1r-SketchArc_5_2r")])

        ### Create Face
        Face_2 = model.addFace(Part_1_doc, [model.selection("FACE", "Sketch_1/Face-SketchLine_5f-SketchArc_10_2f-SketchLine_3r-SketchArc_6_2r")])

        ### Create Face
        Face_3 = model.addFace(Part_1_doc, [model.selection("FACE", "Sketch_1/Face-SketchLine_4f-SketchArc_11_2f-SketchLine_5r-SketchArc_7_2r")])

        ### Create Face
        Face_4 = model.addFace(Part_1_doc, [model.selection("FACE", "Sketch_1/Face-SketchLine_1f-SketchArc_12_2f-SketchLine_4r-SketchArc_8_2r")])

        ### Create Face
        Face_5 = model.addFace(Part_1_doc, [model.selection("FACE", "Sketch_1/Face-SketchArc_5_2f-SketchArc_8_2f-SketchArc_7_2f-SketchArc_6_2f")])

        ### Create Shell
        Shell_1_objects = [model.selection("FACE", "Face_1_1"),
                        model.selection("FACE", "Face_2_1"),
                        model.selection("FACE", "Face_3_1"),
                        model.selection("FACE", "Face_4_1"),
                        model.selection("FACE", "Face_5_1")]
        Shell_1 = model.addShell(Part_1_doc, Shell_1_objects)

        ### Create Group
        Group_1_objects = [model.selection("FACE", "Shell_1_1/Modified_Face&Face_1_1/Face_1_1"),
                        model.selection("FACE", "Shell_1_1/Modified_Face&Face_2_1/Face_2_1"),
                        model.selection("FACE", "Shell_1_1/Modified_Face&Face_3_1/Face_3_1"),
                        model.selection("FACE", "Shell_1_1/Modified_Face&Face_4_1/Face_4_1")]
        Group_1 = model.addGroup(Part_1_doc, "Faces", Group_1_objects)
        Group_1.setName("Inlet")
        Group_1.result().setName("Inlet")

        ### Create Group
        Group_2_objects = [model.selection("EDGE", "Shell_1_1/Modified_Edge&Sketch_1/SketchArc_9_2"),
                        model.selection("EDGE", "Shell_1_1/Modified_Edge&Sketch_1/SketchArc_10_2"),
                        model.selection("EDGE", "Shell_1_1/Modified_Edge&Sketch_1/SketchArc_11_2"),
                        model.selection("EDGE", "Shell_1_1/Modified_Edge&Sketch_1/SketchArc_12_2")]
        Group_2 = model.addGroup(Part_1_doc, "Edges", Group_2_objects)
        Group_2.setName("Walls")
        Group_2.result().setName("Walls")

        model.end()

        ###
        ### SHAPERSTUDY component
        ###

        model.publishToShaperStudy()
        
        Shell_1_1, Inlet, Walls, = SHAPERSTUDY.shape(model.featureStringId(Shell_1))
        ###
        ### SMESH component
        ###

        smesh = smeshBuilder.New()
        #smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                        # multiples meshes built in parallel, complex and numerous mesh edition (performance)

        #smeshObj_1.SetName( 'Outlet' ) ### not created Object
        #smeshObj_2.SetName( 'Walls' ) ### not created Object
        Mesh_1 = smesh.Mesh(Shell_1_1,'Mesh_1')
        Regular_1D = Mesh_1.Segment()
        Number_of_Segments_1 = Regular_1D.NumberOfSegments(self.n_seg)
        Quadrangle_2D = Mesh_1.Quadrangle(algo=smeshBuilder.QUADRANGLE)
        Inlet_1 = Mesh_1.GroupOnGeom(Inlet,'Inlet',SMESH.FACE)
        isDone = Mesh_1.Compute()
        Mesh_1.CheckCompute()
        [ smeshObj_3, Walls_1, Outlet, smeshObj_4 ] = Mesh_1.ExtrusionSweepObjects( [ Mesh_1 ], [ Mesh_1 ], [ Mesh_1 ], [ 0, 0, self.height ], self.z_steps, 1, [  ], 0, [  ], [  ], 0 )
        Mesh_1.RemoveGroup( smeshObj_4 )
        Mesh_1.RemoveGroup( smeshObj_3 )
        Outlet.SetName( 'Outlet' )
        Walls_1.SetName( 'Walls' )

        ## some objects were removed
        aStudyBuilder = salome.myStudy.NewBuilder()
        SO = salome.myStudy.FindObjectIOR(salome.myStudy.ConvertObjectToIOR(smeshObj_4))
        if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
        SO = salome.myStudy.FindObjectIOR(salome.myStudy.ConvertObjectToIOR(smeshObj_3))
        if SO: aStudyBuilder.RemoveObjectWithChildren(SO)

        ## Set names of Mesh objects
        smesh.SetName(Inlet_1, 'Inlet')
        smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
        smesh.SetName(Walls_1, 'Walls')
        smesh.SetName(Number_of_Segments_1, 'Number of Segments_1')
        smesh.SetName(Outlet, 'Outlet')
        smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
        smesh.SetName(Quadrangle_2D.GetAlgorithm(), 'Quadrangle_2D')


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


