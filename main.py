"""
Projet Numérique
Auteur: MORAG & MELNIC
Date: Octobre 2025
Outil de génération de maillage sur Salomé

"""
from Cylinder import Cylinder

cyl  = Cylinder(radius=10,height=10,csquare_length=5,csquare_radius=3,n_seg=20,z_steps=10,mesh_format="stl",filename="Mesh",
                output_dir=r"D:\SALOME")
cyl.build_mesh()



