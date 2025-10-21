"""
Interface graphique pour le projet numérique 
auteurs : MORAG & MELNIC
date : octobre 2025
description : affiche une interface graphique pour rentrer les paramètres pour le maillage
"""

# from cylinder import Cylinder
from tkinter import StringVar, Variable, Tk, LabelFrame
from tkinter.ttk import Button, Frame, Label, Entry, Combobox
from tkinter.messagebox import showinfo

# Test de l'exportation des paramètres
class Cylinder(object):
    def __init__(self, geo_params, mesh_params):
        self.radius = geo_params["Cylinder radius"]
        self.height = geo_params["Cylinder height"]
        self.length = geo_params["Square side length"]
        self.min_cell_size = mesh_params["Min cell size"]
        self.max_cell_size = mesh_params["Max cell size"]
        self.type = mesh_params["Mesh type"]
        
    def results(self):
        print(self.radius)
        print(self.height)
        print(self.length)
        print(self.min_cell_size)
        print(self.max_cell_size)
        print(self.type)

# -----------------------------------------------------------------------
#   CLASS DEFINITION
# -----------------------------------------------------------------------
class Mesh(Frame):

    # --- Constructor of the class
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.geometry_params = {}
        self.mesh_params = {}
        self.radius = Variable()
        self.height = Variable()
        self.length = Variable()
        self.min_cell_size = Variable()
        self.max_cell_size = Variable()
        self.type = StringVar()
        self.mesh_type = ["Triangular", "Quadrilateral", "Tetrahedral", "Hexahedral"]
        self.initialize_widgets()

    # --- Method to initialize widgets
    def initialize_widgets(self):
        """
        initialize widgets
        """
        # Geometry parameters
        geometry = LabelFrame(self, text='Geometry')
        geometry.grid(column=0, row=1, padx=20, pady=20)
        Label(geometry, text="Cylinder radius (m)").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        Label(geometry, text="Cylinder height (m)").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        Label(geometry, text="Square side length (m)").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        Entry(geometry, textvariable=self.radius, width=5).grid(row=0, column=1, padx=10, pady=5)
        Entry(geometry, textvariable=self.height, width=5).grid(row=1, column=1, padx=10, pady=5)
        Entry(geometry, textvariable=self.length, width=5).grid(row=2, column=1, padx=10, pady=5)

        # Mesh parameters
        mesh = LabelFrame(self, text="Mesh cells settings")
        mesh.grid(column=1, row=1, padx=20, pady=20)
        Label(mesh, text="min value").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        Label(mesh, text="max value").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        Label(mesh, text="mesh type").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        Entry(mesh, textvariable=self.min_cell_size, width=5).grid(row=0, column=1, padx=10, pady=5)
        Entry(mesh, textvariable=self.max_cell_size, width=5).grid(row=1, column=1, padx=10, pady=5)
        combo = Combobox(mesh, values=self.mesh_type, textvariable=self.type, state='readonly')
        combo.grid(row=2, column=1, padx=10, pady=5)
        combo.current(0)
        
        # Save button
        Button(self, text="Generate Mesh", command=self.saveFile).grid(row=10, column=1, padx=5, pady=10)

    def getAllVars(self):
        """
        Get all variables after pressing button
        """
        self.geometry_params["Cylinder radius"] = self.radius.get()
        self.geometry_params["Cylinder height"] = self.height.get()
        self.geometry_params["Square side length"] = self.height.get()
        self.mesh_params["Min cell size"] = self.min_cell_size.get()
        self.mesh_params["Max cell size"] = self.max_cell_size.get()
        self.mesh_params["Mesh type"] = self.type.get()
        print("Geometry parameters", self.geometry_params)
        print("Mesh parameters", self.mesh_params)

    def saveFile(self):
        """
        Saves Python File
        """
        self.getAllVars()
        file = Cylinder(self.geometry_params, self.mesh_params)
        file.results()


if __name__ == "__main__":
    gui = Tk()
    gui.title('Génération de maillage structuré')
    gui.geometry("500x200")
    myapp = Mesh(gui)
    myapp.mainloop()
