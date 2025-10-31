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
    Class that creates a hexahedral structured mesh of cylindrical reactor using the SALOME software version 9.15.0.
    The structured mesh is created by dividing the cylinder base in 5 faces. A middle section made of 
    a curvilinial square and 4 arcs of a circle.

    """

    def __init__(self, radius, height, curv_square_length,curv_square_radius,sq_nb_seg,mesh_format,filename,output_dir):
        """ Initialize the attributes """

        # Cylinder parameters
        self.radius = radius
        self.height = height

        # Curvilinial square parameters
        self.csquare_length = curv_square_length
        self.csquare_radius = curv_square_radius

        # Mesh parameters
        self.sq_nb_seg = sq_nb_seg  
        self.mesh_format = mesh_format

        # Output parameters
        self.filename = filename
        self.output_dir = output_dir

    def arc_centers(self,x1, y1, x2, y2, r, normal_dir):
        """Computes the arc centers when given 2 points and the radius of the arc"""

        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        
        if d > 2 * r:
            raise ValueError(" Curvilignial square creation Error : No valid circle arc — points too far apart for this radius.")
        
        h = math.sqrt(r**2 - (d / 2)**2)
        nx, ny = -dy / d, dx / d  # perpendicular direction
        
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
        The main function of the class. It builds the mesh using SALOME functionalities. 
        It first creates the 2D geometry and geometrical components. Then for the mesh generation
        it uses an optimization algorithm in order to achieve a Mean Aspect Ratio as close as possible to 1.
        Once the optimal mesh is computed an extrusion is made and the file is exported to the user-given destination.  
        """

        salome.salome_init()
        notebook = salome_notebook.NoteBook()

        ### GEOM component

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

        # Make the vertices of the curvilinial square
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

        # Make vertices for the centers of the curvilinial square arcs
        Cx1,Cy1 = self.arc_centers(geompy.PointCoordinates(Vertex_5)[0],geompy.PointCoordinates(Vertex_5)[1],
                                    geompy.PointCoordinates(Vertex_6)[0],geompy.PointCoordinates(Vertex_6)[1],self.csquare_radius,(0,-1))
        Cx2,Cy2 = self.arc_centers(geompy.PointCoordinates(Vertex_7)[0],geompy.PointCoordinates(Vertex_7)[1],
                                    geompy.PointCoordinates(Vertex_8)[0],geompy.PointCoordinates(Vertex_8)[1],self.csquare_radius,(0,1))
        Cx3,Cy3 = self.arc_centers(geompy.PointCoordinates(Vertex_6)[0],geompy.PointCoordinates(Vertex_6)[1],
                                    geompy.PointCoordinates(Vertex_7)[0],geompy.PointCoordinates(Vertex_7)[1],self.csquare_radius,(1,0))
        Cx4,Cy4 = self.arc_centers(geompy.PointCoordinates(Vertex_5)[0],geompy.PointCoordinates(Vertex_5)[1],
                                    geompy.PointCoordinates(Vertex_8)[0],geompy.PointCoordinates(Vertex_8)[1],self.csquare_radius,(-1,0))

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

        # Create the inlet group
        Inlet = geompy.CreateGroup(Shell_1, geompy.ShapeType["FACE"])
        face_ids = geompy.SubShapeAllIDs(Shell_1, geompy.ShapeType["FACE"])
        geompy.UnionIDs(Inlet, face_ids)

        #Create the wall group
        Wall = geompy.CreateGroup(Shell_1, geompy.ShapeType["EDGE"])  
        outer_edge_length = 0.5 * math.pi * self.radius
        edges = geompy.SubShapeAll(Shell_1, geompy.ShapeType["EDGE"])
        outer_edges = [e for e in edges if abs(geompy.BasicProperties(e)[0] - outer_edge_length) < 1e-3 ]  
        outer_edges_ids = [geompy.GetSubShapeID(Shell_1, e) for e in outer_edges] 
        geompy.UnionIDs(Wall, outer_edges_ids)

        # Add all the objects to the study (used if the SALOME GUI is opened)
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

        ### SMESH component
    
        smesh = smeshBuilder.New()

        # Test parameters in order to find the optimal mesh
        n_xy_values = list(range(1,self.sq_nb_seg))

        results = []
        meshes = {}  

        for n_xy in n_xy_values:

            # Mesh computing
            Mesh_1 = smesh.Mesh(Shell_1, f"Mesh_{n_xy}")
            Regular_1D = Mesh_1.Segment()

            # Circle/square segments
            NbSegXY = smesh.CreateHypothesis('NumberOfSegments')
            NbSegXY.SetNumberOfSegments(self.sq_nb_seg)

            # Radial segments
            NbSegRadial = smesh.CreateHypothesis('NumberOfSegments')
            NbSegRadial.SetNumberOfSegments(n_xy)  
            NbSegRadial.SetScaleFactor(2)

            # Edges filtering
            edges = geompy.ExtractShapes(Shell_1, geompy.ShapeType["EDGE"], True)
            square_edges = []
            circle_edges = []
            radial_edges = []

            for e in edges:
                vertices = geompy.ExtractShapes(e, geompy.ShapeType["VERTEX"], True)
                v1, v2 = vertices[0], vertices[1]
                x1, y1, z1 = geompy.PointCoordinates(v1)
                x2, y2, z2 = geompy.PointCoordinates(v2)
                r1 = math.hypot(x1, y1)
                r2 = math.hypot(x2, y2)

                if abs(r1 - r2) < 1e-6:
                    circle_edges.append(e)
                else:
                    radial_edges.append(e)

            for e in square_edges + circle_edges:
                Mesh_1.AddHypothesis(NbSegXY, e)

            for e in radial_edges:
                Mesh_1.AddHypothesis(NbSegRadial, e)

            # 2D Quadrangles
            Quadrangle_2D = Mesh_1.Quadrangle(algo=smeshBuilder.QUADRANGLE)

            # Geometrical groups
            Inlet_1 = Mesh_1.GroupOnGeom(Inlet, 'Inlet', SMESH.FACE)
            Wall_1 = Mesh_1.GroupOnGeom(Wall, 'Wall', SMESH.EDGE)

            # Mesh computing
            isDone = Mesh_1.Compute()
            if not isDone:
                print(f"Mesh failed for {n_xy} segments.")
                continue

            # Computing of the aspect ration on the INLET
            inlet_group = None
            for g in Mesh_1.GetGroups():
                if g.GetName() == "Inlet":
                    inlet_group = g
                    break

            if inlet_group is None:
                print(f"Group 'Inlet' not found for {n_xy} segments.")
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


        print("\nResults summary :")
        for n_xy, mean_ar in results:
            print(f"{n_xy} segments, Mean AR = {mean_ar:.4f}")

        # Optimal mesh selection
        best = min(results, key=lambda x: x[1])
        best_n_xy = best[0]
        best_ar = best[1]
        print(f"\nOptimal segments number = {best_n_xy} (Mean AR = {best_ar:.4f})")

        # Removal of the non-optimal meshes
        for n_xy, mesh in meshes.items():
            if n_xy != best_n_xy:
                smesh.RemoveMesh(mesh)

        # Renaming of the optimal Mesh
        Mesh_1 = meshes[best_n_xy]
        Mesh_1.SetName("Mesh")

        # Extrusion
        edge_length = math.pi * self.radius / 2 / n_xy
        center_length = self.csquare_length / self.sq_nb_seg
        mesh_size_xy = (edge_length + center_length) / 2
        n_z = math.ceil(self.height / mesh_size_xy)
        step_height = self.height / n_z

        print(f"Edge length : {edge_length:.2f}")
        print(f"Center length : {center_length:.2f}")
        print(f"Extrusion step : {step_height:.2f}")

        Mesh_1.ExtrusionSweepObjects( [ Mesh_1 ], [ Mesh_1 ], [ Mesh_1 ], [ 0, 0, step_height], n_z, 1, [  ], 1, [  ], [  ], 0 )

        for grp in Mesh_1.GetGroups():
            if grp.GetType() == SMESH.EDGE:   
                Mesh_1.RemoveGroup(grp)
            elif grp.GetType() == SMESH.VOLUME:
                Mesh_1.RemoveGroup(grp)
            elif grp.GetName() == "Inlet_top":
                grp.SetName("Outlet")
            elif grp.GetName() == "Wall_extruded":
                grp.SetName("Wall")

        
        # Export Mesh to file

        # Choose export directory and file name
        os.makedirs(self.output_dir, exist_ok=True)

        if self.mesh_format == "med":
            export_path = os.path.join(self.output_dir, self.filename +".med")
            Mesh_1.ExportMED(export_path, auto_groups=True, minor=40)
            print(f"Mesh exported to: {export_path}")
        
        elif self.mesh_format == "unv":
            export_path = os.path.join(self.output_dir, self.filename +".unv")
            Mesh_1.ExportUNV(export_path)
            print(f"Mesh exported to: {export_path}")

        elif self.mesh_format == "stl":
            export_path = os.path.join(self.output_dir,self.filename + ".stl")
            Mesh_1.ExportSTL(export_path)
            print(f"Mesh exported to: {export_path}")
        
        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser()


