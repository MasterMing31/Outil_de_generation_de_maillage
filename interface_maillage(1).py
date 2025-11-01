"""
Interface graphique pour le projet numérique 
auteurs : MORAG & MELNIC
date : octobre 2025
description : affiche une interface graphique pour rentrer les paramètres pour le maillage
"""

# from cylinder import Cylinder
import tkinter as tk
from tkinter import StringVar, Variable, Tk, LabelFrame, ttk, filedialog, Toplevel
from tkinter.ttk import Button, Frame, Label, Entry, Combobox, Radiobutton
from tkinter.messagebox import showinfo
import toml, os


class Mesh(Frame):
    """Interface to get parameters for mesh"""
    def __init__(self, master):
        super().__init__(master)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self.grid()
        self.geometry_params = {}
        self.mesh_params = {}
        self.choice = tk.StringVar(value="create")
        self.cyl_radius = Variable()
        self.cyl_height = Variable()
        self.sq_length = Variable()
        self.sq_radius = Variable()
        self.sq_segments = Variable()
        self.extrusion_segments = StringVar()
        self.mesh_type_list = ["Very coarse", "Coarse", "Moderate", "Fine", "Very fine", "Custom"]
        self.mesh_type = StringVar()
        self.file_format_list = ["med", "unv", "stl"]
        self.file_format = StringVar()
        self.file_name = StringVar()
        self.output_dir = StringVar()
        self.first()
        self.create_tab3()

    def first(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Creation")
        creation = LabelFrame(tab, text="Option")
        creation.grid(column=1, row=1, padx=20, pady=20)
        R1 = Radiobutton(creation, text="Create new file", variable=self.choice, value="create")
        R1.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        R2 = Radiobutton(creation, text="Load toml file", variable=self.choice, value="load")
        R2.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        Button(creation, text="Browse", command=self.load_toml_file).grid(row=1, column=1, padx=10, pady=5)
        Button(tab, text="Validate", command=self.second_win).grid(row=10, column=1, padx=5, pady=10)


    def load_toml_file(self):
        """Ouvre un explorateur Windows pour choisir un fichier TOML"""
        filepath = filedialog.askopenfilename(
            title="Select TOML file",
            filetypes=[("TOML files", "*.toml"), ("All files", "*.*")]
        )
        if filepath:
            self.toml_path.set(filepath)
            print("Fichier sélectionné :", filepath)

    def second_win(self):
        second_window = tk.Toplevel(self)
        second_window.title("Parameters")

        self.notebook = ttk.Notebook(second_window)
        self.notebook.pack(expand=True, fill="both")

        self.create_tab1()
        self.create_tab2()
        self.create_tab3()
        self.create_tab4()

    def create_tab1(self):
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Geometry and Mesh parameters")

        geometry = ttk.LabelFrame(tab1, text='Geometry')
        geometry.grid(column=0, row=1, padx=20, pady=20)
        Label(geometry, text="Cylinder radius (m)").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        Label(geometry, text="Cylinder height (m)").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        Label(geometry, text="Square side length (m)").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        Label(geometry, text="Square arc radius (m)").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        Entry(geometry, textvariable=self.cyl_radius, width=22).grid(row=0, column=1, padx=10, pady=5)
        Entry(geometry, textvariable=self.cyl_height, width=22).grid(row=1, column=1, padx=10, pady=5)
        Entry(geometry, textvariable=self.sq_length, width=22).grid(row=2, column=1, padx=10, pady=5)
        Entry(geometry, textvariable=self.sq_radius, width=22).grid(row=3, column=1, padx=10, pady=5)

        # Mesh parameters
        mesh = LabelFrame(tab1, text="Mesh cells settings")
        mesh.grid(column=1, row=1, padx=20, pady=20)
        Label(mesh, text="Nb segs in square").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        Label(mesh, text="Nb segs for extrusion").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        Entry(mesh, textvariable=self.sq_segments, width=15).grid(row=0, column=1, padx=10, pady=5)
        R3 = Radiobutton(mesh, text="Auto", variable=self.extrusion_segments, value="Auto")
        R3.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        R4 = Radiobutton(mesh, text="Custom", variable=self.extrusion_segments, value="Custom")
        R4.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        Entry(mesh, textvariable=self.extrusion_segments, width=10).grid(row=2, column=3, padx=10, pady=5)


    def create_tab2(self):
        """Deuxième onglet"""
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="File parameters")

        # Geometry parameters
        file_param = LabelFrame(tab2, text='File settings')
        file_param.grid(column=0, row=1, padx=20, pady=20)
        Label(file_param, text="File format").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        Label(file_param, text="File name").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        Label(file_param, text="output_dir").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        Entry(file_param, textvariable=self.file_name, width=22).grid(row=1, column=1, padx=10, pady=5)
        Button(file_param, text="Browse", command=self.browse).grid(row=2, column=1, padx=5, pady=10)
        combo = Combobox(file_param, values=self.file_format_list, textvariable=self.file_format, state='readonly')
        combo.grid(row=0, column=1, padx=10, pady=5)
        combo.current(1)
        Button(tab2, text="Generate Mesh", command=self.saveToml).grid(row=10, column=0, padx=5, pady=10)

    def create_tab3(self):
        """Troisème onglet"""
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="Help")

    def create_tab4(self):
        """Quatrième onglet"""
        tab4 = ttk.Frame(self.notebook)
        self.notebook.add(tab4, text="Info")

    def browse(self):
        folder = filedialog.askdirectory(title="Select output directory")
        if folder:
            self.output_dir.set(folder)
        # self.save_file()

    # def save_file(self):
    #     folder = self.output_dir.get()
    #     filename = self.file_name.get()
    #     full_path = os.path.join(folder, filename)

    def saveToml(self):
        self.getAllVars()
        filename = "variables.toml"
        folder = self.output_dir.get()
        full_path = os.path.join(folder, filename)
        with open(full_path, mode='w') as tomlFile:
            toml.dump(self.geometry_params, tomlFile)
        showinfo("Informations", "Variables saved to\n" + str(filename))

    def getAllVars(self):
        """
        Get all variables after pressing button
        """
        # self.geometry_params["Cylinder radius"] = self.cyl_radius.get()
        # self.geometry_params["Cylinder height"] = self.cyl_height.get()
        info_authors = "MELNIC Dan-Christian & MORAG Gabriel"
        info_date = "October 2026"
        self.geometry_params["Informations"] = {"Authors": info_authors,
                                                "Date": info_date}
        self.geometry_params["Geometry"] = {"Cylinder radius": self.cyl_radius.get(), 
                                            "Cylinder height": self.cyl_height.get(),
                                            "Square side length": self.sq_length.get(),
                                            "Square arc radius": self.sq_radius.get()}
        self.geometry_params["Mesh"] = {"Nb segments in square": self.sq_segments.get(),
                                        "Nb segments for extrusion": self.extrusion_segments.get(),
                                        "Mesh Fineness": self.mesh_type.get()}
        self.geometry_params["File parameters"] = {"Filename": self.file_name.get(),
                                                   "File format": self.file_format.get(),
                                                   "File directory": self.output_dir.get()}
        print("Geometry parameters", self.geometry_params)
        print("Mesh parameters", self.mesh_params)


if __name__ == "__main__":
    gui = Tk()
    gui.title('Structured Mesh Generation')
    gui.geometry("250x200")
    myapp = Mesh(gui)
    myapp.mainloop()
