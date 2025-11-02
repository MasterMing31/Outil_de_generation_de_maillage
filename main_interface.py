import subprocess
import tkinter as tk
from tkinter import StringVar, Variable, Tk, LabelFrame, ttk, filedialog, Toplevel
from tkinter.ttk import Button, Frame, Label, Entry, Combobox, Radiobutton
from tkinter.messagebox import showinfo, showerror
import os
from Interface_maillage_marche_mais_pas_complet import Mesh

gui = Tk()
gui.title('Structured Mesh Generation')
gui.geometry("300x250")
myapp = Mesh(gui)
myapp.mainloop()
