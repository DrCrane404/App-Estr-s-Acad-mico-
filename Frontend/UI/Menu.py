# Menu.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import sys
import os

root = tb.Window(themename="superhero")
root.title("Menú")
root.geometry("400x500")
root.resizable(False, False)
root.place_window_center()

frame = tb.Frame(root, padding=40)
frame.pack(fill="both", expand=True)

tb.Label(
    frame,
    text="¿A dónde quieres ir?",
    font=("Helvetica", 18, "bold"),
    bootstyle="inverse-default"
).pack(pady=(0, 30))

def abrir(pantalla):
    root.destroy()
    import subprocess
    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), pantalla)])

opciones = [
    ("🏠  Pantalla principal",  "success",   "vPrincipal.py"),
    ("👤  Mi perfil",           "info",      "vPerfil.py"),
    ("📋  Cuestionario",        "warning",   "Cuestionario.py"),
    ("❓  Ayuda",               "secondary", "vAyuda.py"),
]

for texto, estilo, pantalla in opciones:
    tb.Button(
        frame,
        text=texto,
        bootstyle=estilo,
        width=28,
        command=lambda p=pantalla: abrir(p)
    ).pack(pady=8)

tb.Separator(frame).pack(fill="x", pady=20)

def cerrar_sesion():
    from tkinter import messagebox
    if messagebox.askyesno("Cerrar sesión", "¿Estás seguro?"):
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Service'))
        import sesion
        sesion.cerrar()
        root.destroy()
        import subprocess
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "Login.py")])

tb.Button(
    frame,
    text="🚪  Cerrar sesión",
    bootstyle="danger",
    width=28,
    command=cerrar_sesion
).pack()

root.mainloop()