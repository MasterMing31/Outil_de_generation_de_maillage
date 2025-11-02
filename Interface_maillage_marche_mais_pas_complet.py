import tkinter as tk
from tkinter import StringVar, Variable, Tk, LabelFrame, ttk, filedialog, Toplevel
from tkinter.ttk import Button, Frame, Label, Entry, Combobox, Radiobutton
from tkinter.messagebox import showinfo, showerror
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

        self.file_path = tk.StringVar()
        self.cyl_radius = Variable()
        self.cyl_height = Variable()
        self.sq_length = Variable()
        self.sq_radius = Variable()
        self.sq_segments = Variable()
        self.extrusion_value = Variable()
        self.mode_extrusion = StringVar(value="Auto")
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

        R1 = tk.Radiobutton(creation, text="Create new file", variable=self.choice,
                            value="create", command=self.update_browse_state)
        R1.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        R2 = tk.Radiobutton(creation, text="Load toml file", variable=self.choice,
                            value="load", command=self.update_browse_state)
        R2.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.browse_btn = ttk.Button(creation, text="Browse",
                                     command=self.load_toml_file, state="disabled")
        self.browse_btn.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(tab, text="Validate", command=self.second_win).grid(row=10, column=1, padx=5, pady=10)

    def update_browse_state(self):
        """Active le bouton Browse uniquement si 'Load toml file' est sélectionné"""
        if self.choice.get() == "load":
            self.browse_btn.config(state="normal")
        else:
            self.browse_btn.config(state="disabled")
            self.reset_fields()  

    def reset_fields(self):
        """Réinitialise toutes les entrées quand on choisit 'Create new file'"""
        self.cyl_radius.set("")
        self.cyl_height.set("")
        self.sq_length.set("")
        self.sq_radius.set("")
        self.sq_segments.set("")
        self.extrusion_value.set("")
        self.mesh_type.set("")
        self.file_name.set("")
        self.file_format.set("")
        self.output_dir.set("")

    def load_toml_file(self):
        file_path = filedialog.askopenfilename(
            title="Select TOML file",
            filetypes=[("TOML files", "*.toml"), ("All files", "*.*")]
        )
        if not file_path:
            return

        self.file_path.set(file_path)
        try:
            with open(file_path, "r") as f:
                data = toml.load(f)
            self.populate_fields(data)
            showinfo("Success", "TOML file loaded successfully!")
        except Exception as e:
            showerror("Error", f"Failed to load TOML file:\n{e}")

    def populate_fields(self, data):
        geom = data.get("Geometry", {})
        mesh = data.get("Mesh", {})
        file_params = data.get("File parameters", {})

        self.cyl_radius.set(geom.get("Cylinder radius", ""))
        self.cyl_height.set(geom.get("Cylinder height", ""))
        self.sq_length.set(geom.get("Square side length", ""))
        self.sq_radius.set(geom.get("Square arc radius", ""))

        self.sq_segments.set(mesh.get("Nb segments in square", ""))
        self.extrusion_value.set(mesh.get("Nb segments for extrusion", ""))
        self.mesh_type.set(mesh.get("Mesh Fineness", ""))

        self.file_name.set(file_params.get("Filename", ""))
        self.file_format.set(file_params.get("File format", ""))
        self.output_dir.set(file_params.get("File directory", ""))

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
        Entry(geometry, textvariable=self.cyl_radius, width=22).grid(row=0, column=1, padx=10, pady=5)

        Label(geometry, text="Cylinder height (m)").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        Entry(geometry, textvariable=self.cyl_height, width=22).grid(row=1, column=1, padx=10, pady=5)

        Label(geometry, text="Square side length (m)").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        Entry(geometry, textvariable=self.sq_length, width=22).grid(row=2, column=1, padx=10, pady=5)

        Label(geometry, text="Square arc radius (m)").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        Entry(geometry, textvariable=self.sq_radius, width=22).grid(row=3, column=1, padx=10, pady=5)

        mesh = LabelFrame(tab1, text="Mesh cells settings")
        mesh.grid(column=1, row=1, padx=20, pady=20)

        Label(mesh, text="Nb segs in square").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        Entry(mesh, textvariable=self.sq_segments, width=15).grid(row=0, column=1, padx=10, pady=5)

        Label(mesh, text="Nb segs for extrusion").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        R3 = tk.Radiobutton(mesh, text="Auto", variable=self.mode_extrusion, value="Auto", command=self.update_entry_state)
        R3.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        R4 = tk.Radiobutton(mesh, text="Custom", variable=self.mode_extrusion, value="Custom", command=self.update_entry_state)
        R4.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.entry_custom = Entry(mesh, textvariable=self.extrusion_value, width=10, state="disabled")
        self.entry_custom.grid(row=2, column=3, padx=10, pady=5)

    def update_entry_state(self):
        if self.mode_extrusion.get() == "Custom":
            self.entry_custom.config(state="normal")
        else:
            self.entry_custom.config(state="disabled")

    def create_tab2(self):
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="File parameters")

        file_param = LabelFrame(tab2, text='File settings')
        file_param.grid(column=0, row=1, padx=20, pady=20)

        Label(file_param, text="File format").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        Label(file_param, text="File name").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        Label(file_param, text="Output directory").grid(row=2, column=0, sticky="e", padx=5, pady=5)

        Entry(file_param, textvariable=self.file_name, width=22).grid(row=1, column=1, padx=10, pady=5)
        Button(file_param, text="Browse", command=self.browse).grid(row=2, column=1, padx=5, pady=10)

        combo = Combobox(file_param, values=self.file_format_list, textvariable=self.file_format, state='readonly')
        combo.grid(row=0, column=1, padx=10, pady=5)
        combo.current(0)

        Button(tab2, text="Generate Mesh", command=self.saveToml).grid(row=10, column=0, padx=5, pady=10)

    def browse(self):
        folder = filedialog.askdirectory(title="Select output directory")
        if folder:
            self.output_dir.set(folder)

    def validate_fields(self):
        missing = []
        invalid = []

        if not self.cyl_radius.get():
            missing.append("Cylinder radius")
        if not self.cyl_height.get():
            missing.append("Cylinder height")
        if not self.sq_length.get():
            missing.append("Square side length")
        if not self.sq_radius.get():
            missing.append("Square arc radius")

        if missing:
            showerror("Missing fields",
                    "Please fill in the following fields:\n- " + "\n- ".join(missing))
            return False

        numeric_fields = {
            "Cylinder radius": self.cyl_radius.get(),
            "Cylinder height": self.cyl_height.get(),
            "Square side length": self.sq_length.get(),
            "Square arc radius": self.sq_radius.get(),
            "Nb segs in square": self.sq_segments.get()
        }

        for name, value in numeric_fields.items():
            try:
                float(value)
            except ValueError:
                invalid.append(name)

        if invalid:
            showerror("Invalid input",
                    "The following fields must be numeric:\n- " + "\n- ".join(invalid))
            return False

        return True

    def saveToml(self):
        
        if not self.validate_fields():
            return
        
        self.getAllVars()
        folder = self.output_dir.get() or os.getcwd()
        filename = self.file_name.get() or "variables"
        full_path = os.path.join(folder, f"{filename}.toml")

        with open(full_path, mode='w') as tomlFile:
            toml.dump(self.geometry_params, tomlFile)
        showinfo("Informations", f"Variables saved to:\n{full_path}")

    def getAllVars(self):
        info_authors = "MELNIC Dan-Christian & MORAG Gabriel"
        info_date = "October 2026"
        self.geometry_params["Informations"] = {"Authors": info_authors, "Date": info_date}
        self.geometry_params["Geometry"] = {
            "Cylinder radius": self.cyl_radius.get(),
            "Cylinder height": self.cyl_height.get(),
            "Square side length": self.sq_length.get(),
            "Square arc radius": self.sq_radius.get()
        }
        self.geometry_params["Mesh"] = {
            "Nb segments in square": self.sq_segments.get(),
            "Nb segments for extrusion": self.extrusion_value.get(),
            "Mesh Fineness": self.mesh_type.get()
        }
        self.geometry_params["File parameters"] = {
            "Filename": self.file_name.get(),
            "File format": self.file_format.get(),
            "File directory": self.output_dir.get()
        }

    def create_tab3(self):
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="Help")

    def create_tab4(self):
        tab4 = ttk.Frame(self.notebook)
        self.notebook.add(tab4, text="Info")


if __name__ == "__main__":
    gui = Tk()
    gui.title('Structured Mesh Generation')
    gui.geometry("300x250")
    myapp = Mesh(gui)
    myapp.mainloop()
