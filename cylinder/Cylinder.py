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

    def arc_centers(self,x1, y1, x2, y2, r, normal_dir):

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

    def build_mesh(self):
        """
        """

        ###
        ### This part is generated automatically by SALOME v9.15.0 with dump python functionality
        ###

        salome.salome_init()
        notebook = salome_notebook.NoteBook()
        sys.path.insert(0, r'D:/Universite/Master_2/Projet num')

        ###
        ### GEOM component
        ###
        geompy = geomBuilder.New()

        O = geompy.MakeVertex(0, 0, 0)
        OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
        OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
        OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

        # Make vertices in order to build the arcs of the cylinder
        theta = math.pi / 4
        x_cyl = round(self.radius * math.cos(theta),6)
        y_cyl = round(self.radius * math.sin(theta),6)

        Vertex_1 = geompy.MakeVertex(x_cyl, y_cyl, 0)
        Vertex_2 = geompy.MakeVertex(-x_cyl, y_cyl, 0)
        Vertex_3 = geompy.MakeVertex(-x_cyl, -y_cyl, 0)
        Vertex_4 = geompy.MakeVertex(x_cyl, -y_cyl, 0)

        # Make the vertices of the curvilignial square
        Vertex_5 = geompy.MakeVertex(self.csquare_length / 2, self.csquare_length / 2, 0)
        Vertex_6 = geompy.MakeVertex(-self.csquare_length / 2, self.csquare_length / 2, 0)
        Vertex_7 = geompy.MakeVertex(-self.csquare_length / 2, -self.csquare_length / 2, 0)
        Vertex_8 = geompy.MakeVertex(self.csquare_length / 2, -self.csquare_length / 2, 0)

        Arc_1 = geompy.MakeArcCenter(O, Vertex_2, Vertex_1,False)
        Arc_1_vertex_3 = geompy.GetSubShape(Arc_1, [3])
        Arc_2 = geompy.MakeArcCenter(O, Arc_1_vertex_3, Vertex_4,False)
        Arc_2_vertex_3 = geompy.GetSubShape(Arc_2, [3])
        Arc_3 = geompy.MakeArcCenter(O, Arc_2_vertex_3, Vertex_3,False)
        Arc_3_vertex_3 = geompy.GetSubShape(Arc_3, [3])
        Arc_1_vertex_2 = geompy.GetSubShape(Arc_1, [2])
        Arc_4 = geompy.MakeArcCenter(O, Arc_3_vertex_3, Arc_1_vertex_2,False)

        # Make vertices for the centers of the curvilignial square arcs
        Cx1,Cy1 = self.arc_centers(geompy.PointCoordinates(Vertex_5)[0],geompy.PointCoordinates(Vertex_5)[1],
                                   geompy.PointCoordinates(Vertex_6)[0],geompy.PointCoordinates(Vertex_6)[1],self.radius,(0,-1))
        Cx2,Cy2 = self.arc_centers(geompy.PointCoordinates(Vertex_7)[0],geompy.PointCoordinates(Vertex_7)[1],
                                   geompy.PointCoordinates(Vertex_8)[0],geompy.PointCoordinates(Vertex_8)[1],self.radius,(0,1))
        Cx3,Cy3 = self.arc_centers(geompy.PointCoordinates(Vertex_6)[0],geompy.PointCoordinates(Vertex_6)[1],
                                   geompy.PointCoordinates(Vertex_7)[0],geompy.PointCoordinates(Vertex_7)[1],self.radius,(1,0))
        Cx4,Cy4 = self.arc_centers(geompy.PointCoordinates(Vertex_5)[0],geompy.PointCoordinates(Vertex_5)[1],
                                   geompy.PointCoordinates(Vertex_8)[0],geompy.PointCoordinates(Vertex_8)[1],self.radius,(-1,0))
        
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
        
        smesh = smeshBuilder.New()
        #smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                        # multiples meshes built in parallel, complex and numerous mesh edition (performance)

        #smeshObj_1.SetName( 'Outlet' ) ### not created Object
        Mesh_1 = smesh.Mesh(Shell_1,'Mesh_1')
        Regular_1D = Mesh_1.Segment()
        Number_of_Segments_1 = Regular_1D.NumberOfSegments(15)
        Quadrangle_2D = Mesh_1.Quadrangle(algo=smeshBuilder.QUADRANGLE)
        Inlet_1 = Mesh_1.GroupOnGeom(Inlet,'Inlet',SMESH.FACE)
        isDone = Mesh_1.Compute()
        Mesh_1.CheckCompute()
        
        [ smeshObj_2, Wall_1, Outlet, smeshObj_3 ] = Mesh_1.ExtrusionSweepObjects( [ Mesh_1 ], [ Mesh_1 ], [ Mesh_1 ], [ 0, 0, self.height ], self.z_steps, 1, [  ], 0, [  ], [  ], 0 )
        Mesh_1.RemoveGroup( smeshObj_3 )
        Mesh_1.RemoveGroup( smeshObj_2 )
        Outlet.SetName( 'Outlet' )
        Wall_1.SetName( 'Wall' )

        ## some objects were removed
        aStudyBuilder = salome.myStudy.NewBuilder()
        SO = salome.myStudy.FindObjectIOR(salome.myStudy.ConvertObjectToIOR(smeshObj_3))
        if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
        SO = salome.myStudy.FindObjectIOR(salome.myStudy.ConvertObjectToIOR(smeshObj_2))
        if SO: aStudyBuilder.RemoveObjectWithChildren(SO)

        ## Set names of Mesh objects
        smesh.SetName(Inlet_1, 'Inlet')
        smesh.SetName(Wall_1, 'Wall')
        smesh.SetName(Number_of_Segments_1, 'Number of Segments_1')
        smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
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


