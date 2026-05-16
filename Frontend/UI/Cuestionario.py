# Cuestionario.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Service'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Service', 'CuestionarioInicial'))
from CalculadoraEstres import CalculadoraEstres

# Archivo de progreso 
ARCHIVO_PROGRESO = os.path.join(os.path.dirname(__file__), '..', 'progreso.json')

# Datos 
calculadora = CalculadoraEstres()
preguntas = calculadora.cuestionario["preguntas"]
total = len(preguntas)
respuestas = {}
pregunta_actual = [0]
opcion_seleccionada = [None]

# Ventana principal 
root = tb.Window(themename="superhero")
root.title("Cuestionario de Estrés")
root.geometry("600x620")
root.resizable(False, False)
root.place_window_center()

# Frame principal 
frame = tb.Frame(root, padding=40)
frame.pack(fill="both", expand=True)

# Encabezado 
tb.Label(
    frame,
    text="Cuestionario de Estrés Académico",
    font=("Helvetica", 16, "bold"),
    bootstyle="inverse-default"
).pack(pady=(0, 4))

# Categoría 
lbl_categoria = tb.Label(
    frame,
    text="",
    font=("Helvetica", 10),
    bootstyle="info"
)
lbl_categoria.pack(pady=(0, 8))

# Barra de progreso 
frame_progreso = tb.Frame(frame)
frame_progreso.pack(fill="x", pady=(0, 4))

lbl_progreso = tb.Label(
    frame_progreso,
    text="Pregunta 1 de 23",
    font=("Helvetica", 9),
    bootstyle="secondary"
)
lbl_progreso.pack(anchor="e")

barra = tb.Progressbar(
    frame,
    bootstyle="success-striped",
    value=0,
    maximum=100
)
barra.pack(fill="x", pady=(0, 20))

# Pregunta 
lbl_pregunta = tb.Label(
    frame,
    text="",
    font=("Helvetica", 13, "bold"),
    wraplength=500,
    justify="left"
)
lbl_pregunta.pack(anchor="w", pady=(0, 20))

# Opciones 
frame_opciones = tb.Frame(frame)
frame_opciones.pack(fill="x", pady=(0, 20))

# Botones de navegación 
frame_botones = tb.Frame(frame)
frame_botones.pack(fill="x", pady=(10, 0))

# Funciones de progreso 
def guardar_progreso():
    datos = {
        "pregunta_actual": pregunta_actual[0],
        "respuestas": respuestas
    }
    with open(ARCHIVO_PROGRESO, "w") as f:
        json.dump(datos, f)

def cargar_progreso():
    if os.path.exists(ARCHIVO_PROGRESO):
        with open(ARCHIVO_PROGRESO, "r") as f:
            return json.load(f)
    return None

def borrar_progreso():
    if os.path.exists(ARCHIVO_PROGRESO):
        os.remove(ARCHIVO_PROGRESO)

# Lógica de preguntas 
def mostrar_pregunta(idx):
    pregunta = preguntas[idx]
    opcion_seleccionada[0] = None

    porcentaje = (idx / total) * 100
    barra["value"] = porcentaje
    lbl_progreso.config(text=f"Pregunta {idx + 1} de {total}")

    categorias = {
        "sueño": "😴 Sueño",
        "academico": "📚 Académico",
        "emocional": "💭 Emocional",
        "familiar": "🏠 Familiar",
        "trabajo": "⚡ Trabajo y actividades"
    }
    lbl_categoria.config(text=categorias.get(pregunta["categoria"], pregunta["categoria"].capitalize()))

    lbl_pregunta.config(text=pregunta["texto"])

    for widget in frame_opciones.winfo_children():
        widget.destroy()

    var = tb.IntVar(value=-1)
    opcion_seleccionada[0] = var

    # Si ya respondió esta pregunta, marcar la opción guardada
    id_preg = pregunta["id"]
    if id_preg in respuestas:
        var.set(respuestas[id_preg])

    for i, opcion in enumerate(pregunta["opciones"]):
        tb.Radiobutton(
            frame_opciones,
            text=opcion["texto"],
            variable=var,
            value=i,
            bootstyle="success",
        ).pack(anchor="w", pady=4)

    for widget in frame_botones.winfo_children():
        widget.destroy()

    if idx > 0:
        tb.Button(
            frame_botones,
            text="← Anterior",
            bootstyle="secondary-outline",
            command=lambda: ir_a(idx - 1)
        ).pack(side="left")

    if idx < total - 1:
        tb.Button(
            frame_botones,
            text="Siguiente →",
            bootstyle="success",
            command=lambda: siguiente(idx)
        ).pack(side="right")
    else:
        tb.Button(
            frame_botones,
            text="Ver resultado ✓",
            bootstyle="warning",
            command=lambda: finalizar(idx)
        ).pack(side="right")


def ir_a(idx):
    pregunta_actual[0] = idx
    mostrar_pregunta(idx)


def siguiente(idx):
    var = opcion_seleccionada[0]
    if var is None or var.get() == -1:
        messagebox.showwarning("Sin respuesta", "Por favor selecciona una opción antes de continuar.")
        return
    respuestas[preguntas[idx]["id"]] = var.get()
    guardar_progreso()
    pregunta_actual[0] = idx + 1
    mostrar_pregunta(idx + 1)


def finalizar(idx):
    var = opcion_seleccionada[0]
    if var is None or var.get() == -1:
        messagebox.showwarning("Sin respuesta", "Por favor selecciona una opción antes de continuar.")
        return
    respuestas[preguntas[idx]["id"]] = var.get()
    borrar_progreso()
    mostrar_resultado()


def mostrar_resultado():
    resultado = calculadora.calcular_nivel_estres(respuestas)

    for widget in frame.winfo_children():
        widget.destroy()

    colores = {
        "success": "#28a745",
        "info": "#17a2b8",
        "warning": "#ffc107",
        "danger": "#dc3545"
    }
    color = colores.get(resultado["color"], "#ffffff")

    tb.Label(
        frame,
        text="Resultado de tu cuestionario",
        font=("Helvetica", 16, "bold"),
        bootstyle="inverse-default"
    ).pack(pady=(20, 30))

    tb.Label(
        frame,
        text=f"Nivel de estrés: {resultado['categoria']}",
        font=("Helvetica", 20, "bold"),
        foreground=color
    ).pack(pady=(0, 10))

    tb.Label(
        frame,
        text=f"{resultado['puntuacion']} / 10",
        font=("Helvetica", 40, "bold"),
        foreground=color
    ).pack(pady=(0, 10))

    barra_resultado = tb.Progressbar(
        frame,
        bootstyle=f"{resultado['color']}-striped",
        value=resultado["puntuacion"] * 10,
        maximum=100
    )
    barra_resultado.pack(fill="x", padx=40, pady=(0, 30))

    tb.Label(
        frame,
        text=resultado["recomendacion_principal"],
        font=("Helvetica", 12),
        wraplength=480,
        justify="center",
        bootstyle="secondary"
    ).pack(pady=(0, 40))

    tb.Button(
        frame,
        text="Continuar →",
        bootstyle="success",
        width=20,
        command=ir_al_menu
    ).pack()


def ir_al_menu():
    root.destroy()
    import subprocess
    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "Menu.py")])


# Iniciar cargando progreso si existe 
progreso = cargar_progreso()
if progreso:
    respuestas.update({int(k): v for k, v in progreso["respuestas"].items()})
    pregunta_actual[0] = progreso["pregunta_actual"]
    mostrar_pregunta(pregunta_actual[0])
else:
    mostrar_pregunta(0)

root.mainloop()