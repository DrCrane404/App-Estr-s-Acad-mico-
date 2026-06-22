# Respiracion.py
#Animacion de tecnica de respiracion
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import sys
import os
import math

# Ventana 
root = tb.Window(themename="superhero")
root.title("Técnica de respiración")
root.geometry("420x900")
root.resizable(False, False)
root.place_window_center()

frame = tb.Frame(root, padding=30)
frame.pack(fill="both", expand=True)

tb.Label(
    frame,
    text="🌬️ Técnica de respiración 4-4-4",
    font=("Helvetica", 14, "bold"),
    bootstyle="info"
).pack(pady=(0, 4))

tb.Label(
    frame,
    text="Tómate un momento antes de continuar",
    font=("Helvetica", 10),
    bootstyle="secondary"
).pack(pady=(0, 20))

# Círculo animado 
canvas = tb.Canvas(frame, width=200, height=200, highlightthickness=0)
canvas.pack(pady=(0, 16))

circulo_bg = canvas.create_oval(20, 20, 180, 180, outline="#2d3748", width=3)
circulo = canvas.create_oval(90, 90, 110, 110, fill="#185FA5", outline="")

lbl_instruccion = tb.Label(
    frame,
    text="Prepárate...",
    font=("Helvetica", 16, "bold"),
    bootstyle="info"
)
lbl_instruccion.pack(pady=(0, 8))

lbl_cuenta = tb.Label(
    frame,
    text="",
    font=("Helvetica", 28, "bold"),
)
lbl_cuenta.pack(pady=(0, 16))

barra = tb.Progressbar(frame, bootstyle="info-striped", value=0, maximum=100)
barra.pack(fill="x", pady=(0, 16))

lbl_ciclo = tb.Label(frame, text="Ciclo 1 de 3", font=("Helvetica", 10), bootstyle="secondary")
lbl_ciclo.pack()

# Lógica de animación 
PASOS = [
    ("Inhala", 4, "#185FA5"),
    ("Mantén", 4, "#f6ad55"),
    ("Exhala", 4, "#38a169"),
]

ciclo_actual = [0]
paso_actual = [0]
cuenta_actual = [0]
animando = [True]

MIN_R = 10
MAX_R = 80
CX, CY = 100, 100

def actualizar_circulo(progreso, color):
    r = MIN_R + (MAX_R - MIN_R) * progreso
    canvas.coords(circulo, CX - r, CY - r, CX + r, CY + r)
    canvas.itemconfig(circulo, fill=color)

def tick():
    if not animando[0]:
        return

    nombre, duracion, color = PASOS[paso_actual[0]]
    cuenta = cuenta_actual[0]
    segundos_restantes = duracion - cuenta

    lbl_instruccion.config(text=nombre, bootstyle="info" if nombre == "Inhala" else "warning" if nombre == "Mantén" else "success")
    lbl_cuenta.config(text=str(segundos_restantes + 1))
    barra["value"] = (cuenta / duracion) * 100

    if nombre == "Inhala":
        progreso = cuenta / duracion
    elif nombre == "Exhala":
        progreso = 1 - (cuenta / duracion)
    else:
        progreso = 1.0

    actualizar_circulo(progreso, color)

    cuenta_actual[0] += 1

    if cuenta_actual[0] >= duracion:
        cuenta_actual[0] = 0
        paso_actual[0] += 1

        if paso_actual[0] >= len(PASOS):
            paso_actual[0] = 0
            ciclo_actual[0] += 1
            lbl_ciclo.config(text=f"Ciclo {ciclo_actual[0] + 1} de 3")

            if ciclo_actual[0] >= 3:
                terminar()
                return

    root.after(1000, tick)

def terminar():
    animando[0] = False
    lbl_instruccion.config(text="¡Bien hecho! 🎉", bootstyle="success")
    lbl_cuenta.config(text="")
    barra["value"] = 100
    actualizar_circulo(0.3, "#38a169")

    for widget in frame.winfo_children():
        if isinstance(widget, tb.Button):
            widget.destroy()

    tb.Button(
        frame,
        text="Continuar →",
        bootstyle="success",
        width=20,
        command=abrir_siguiente
    ).pack(pady=(12, 0))

def abrir_siguiente():
    root.destroy()
    import subprocess
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Service'))
    import sesion
    import UsuarioService

    token = sesion.obtener()
    if token:
        nivel = UsuarioService.obtener_nivel_estres(token)
        if nivel.get("existe") == False or nivel.get("Success") == False:
            subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "Cuestionario.py")])
        else:
            subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "Menu.py")])
    else:
        # Viene del registro, siempre va al cuestionario
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "Cuestionario.py")])

tb.Button(
    frame,
    text="Saltar →",
    bootstyle="secondary-outline",
    width=16,
    command=abrir_siguiente
).pack(pady=(0, 0))

# Iniciar animación
root.after(1000, tick)
root.mainloop()