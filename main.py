"""
Projet Numérique
Auteur: MORAG & MELNIC
Date: Octobre 2025
Outil de génération de maillage sur Salomé

"""
from cylinder.Cylinder import Cylinder

cyl  = Cylinder(radius=10,height=10,curv_square_length=5,curv_square_radius=20,sq_nb_seg=20,mesh_format="stl",filename="Mesh",
                output_dir=r"D:\Universite\Master_2\Projet num\Maillage")
cyl.build_mesh()



