# vAyuda.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import sys
import os

root = tb.Window(themename="superhero")
root.title("Ayuda")
root.geometry("620x640")
root.resizable(False, False)
root.place_window_center()

frame = tb.Frame(root, padding=30)
frame.pack(fill="both", expand=True)

tb.Label(
    frame,
    text="Centro de Ayuda",
    font=("Helvetica", 20, "bold"),
    bootstyle="inverse-default"
).pack(pady=(0, 20))

notebook = tb.Notebook(frame, bootstyle="info")
notebook.pack(fill="both", expand=True)

# Pestaña 1: Cómo funciona 
tab_tutorial = tb.Frame(notebook, padding=20)
notebook.add(tab_tutorial, text="📖 Cómo funciona")

pasos = [
    ("1. Regístrate e inicia sesión",
     "Crea tu cuenta con nombre, correo y contraseña. Si olvidas tu contraseña puedes recuperarla desde la pantalla de login."),
    ("2. Técnica de respiración",
     "Al iniciar sesión, la app te guía con una respiración 4-4-4 (inhala 4s → mantén 4s → exhala 4s) para reducir la tensión antes de empezar."),
    ("3. Cuestionario de estrés",
     "La primera vez responderás 23 preguntas sobre sueño, vida académica, estado emocional, familia y actividades. Tu progreso se guarda automáticamente si lo cierras a medias."),
    ("4. Gestiona tus tareas",
     "Crea tareas con nombre, descripción, horas por día, fechas y nivel de estrés. Puedes marcarlas como completadas, editarlas o eliminarlas. También puedes hacerlas públicas para que otros se unan con un código."),
    ("5. Calendario y nivel de estrés",
     "El calendario muestra en rojo los días donde tus tareas suman más de 16 horas (riesgo para el sueño). La barra de estrés combina tu cuestionario (60%) con el estrés de tus tareas activas (40%)."),
    ("6. Perfil",
     "Actualiza tu nombre, usuario, correo y contraseña desde el menú lateral."),
]

for titulo, descripcion in pasos:
    frame_paso = tb.Frame(tab_tutorial, bootstyle="dark", padding=12)
    frame_paso.pack(fill="x", pady=5)
    tb.Label(frame_paso, text=titulo, font=("Helvetica", 11, "bold"), bootstyle="info").pack(anchor="w")
    tb.Label(frame_paso, text=descripcion, font=("Helvetica", 10), bootstyle="secondary", wraplength=520, justify="left").pack(anchor="w", pady=(4, 0))

# Pestaña 2: Preguntas frecuentes 
tab_faq = tb.Frame(notebook, padding=20)
notebook.add(tab_faq, text="❓ Preguntas frecuentes")

faqs = [
    ("¿Puedo cambiar mi contraseña?",
     "Sí, desde tu perfil puedes actualizarla cuando quieras."),
    ("¿Qué pasa si cierro el cuestionario a medias?",
     "Tu progreso se guarda automáticamente y continuarás donde lo dejaste."),
    ("¿Cómo se calcula mi nivel de estrés?",
     "Combina el resultado de tu cuestionario (60%) con el estrés promedio de tus tareas activas (40%). Si duermes menos de 6 horas se aplica una penalización adicional."),
    ("¿Qué significa que un día esté en rojo en el calendario?",
     "Significa que tienes más de 16 horas de tareas asignadas ese día, lo que deja menos de 8 horas para dormir."),
    ("¿Cómo funciona una tarea pública?",
     "Al crearla se genera un código único. Compártelo con quien quieras; ellos pueden buscarte por nombre y unirse ingresando ese código."),
    ("¿Puedo usar la app sin internet?",
     "No, la app requiere conexión al servidor para guardar tareas, calcular el estrés y actualizar tu perfil."),
]

for pregunta, respuesta in faqs:
    frame_faq = tb.Frame(tab_faq, bootstyle="dark", padding=12)
    frame_faq.pack(fill="x", pady=5)
    tb.Label(frame_faq, text=f"❓ {pregunta}", font=("Helvetica", 11, "bold"), bootstyle="warning").pack(anchor="w")
    tb.Label(frame_faq, text=respuesta, font=("Helvetica", 10), bootstyle="secondary", wraplength=520, justify="left").pack(anchor="w", pady=(4, 0))

# Pestaña 3: Líneas de emergencia 
tab_emergencia = tb.Frame(notebook, padding=20)
notebook.add(tab_emergencia, text="🆘 Emergencias")

tb.Label(
    tab_emergencia,
    text="Si el estrés o la ansiedad te rebasan, pide ayuda.\nNo estás solo/a — estas líneas son gratuitas y confidenciales.",
    font=("Helvetica", 11, "bold"),
    justify="center",
    bootstyle="warning"
).pack(pady=(0, 16))

contactos = [
    ("🇲🇽 SAPTEL",              "55 5259-8121",        "Crisis emocionales · 24 horas · 365 días",            "danger"),
    ("🇲🇽 Línea de la Vida",    "800 290 0024",        "Salud mental · Gobierno federal · 24/7 · Gratuita",   "warning"),
    ("🇲🇽 IMSS Salud Mental",   "800 762 4000",        "Orientación para derechohabientes",                   "info"),
    ("🏫 Orientación escolar",  "Tu departamento de servicios estudiantiles", "Muchas universidades ofrecen atención psicológica gratuita.", "success"),
]

for nombre, numero, descripcion, estilo in contactos:
    frame_c = tb.Frame(tab_emergencia, bootstyle="dark", padding=14)
    frame_c.pack(fill="x", pady=5)
    tb.Label(frame_c, text=nombre, font=("Helvetica", 11, "bold"), bootstyle=estilo).pack(anchor="w")
    tb.Label(frame_c, text=numero, font=("Helvetica", 14, "bold")).pack(anchor="w", pady=(4, 2))
    tb.Label(frame_c, text=descripcion, font=("Helvetica", 10), bootstyle="secondary").pack(anchor="w")

# Pestaña 4: Técnicas rápidas 
tab_tecnicas = tb.Frame(notebook, padding=20)
notebook.add(tab_tecnicas, text="🧘 Técnicas rápidas")

tb.Label(
    tab_tecnicas,
    text="Cuando sientas que el estrés sube, prueba alguna de estas:",
    font=("Helvetica", 11, "bold"),
).pack(pady=(0, 14))

tecnicas = [
    ("🌬️ Respiración 4-4-4",
     "Inhala 4s → Mantén 4s → Exhala 4s. Repite 3 veces. Reduce la frecuencia cardíaca en minutos."),
    ("🖐️ Técnica 5-4-3-2-1",
     "Nombra 5 cosas que ves, 4 que tocas, 3 que escuchas, 2 que hueles y 1 que saboreas. Ancla tu mente al presente."),
    ("💧 Toma agua",
     "La deshidratación leve eleva el cortisol (hormona del estrés). Un vaso de agua puede marcar la diferencia."),
    ("🚶 Camina 5 minutos",
     "El movimiento físico libera endorfinas y rompe el ciclo de tensión mental."),
    ("✍️ Escribe lo que sientes",
     "Dedica 2 minutos a escribir qué te preocupa. Externalizar los pensamientos reduce su carga emocional."),
]

for titulo, descripcion in tecnicas:
    frame_t = tb.Frame(tab_tecnicas, bootstyle="dark", padding=12)
    frame_t.pack(fill="x", pady=5)
    tb.Label(frame_t, text=titulo, font=("Helvetica", 11, "bold"), bootstyle="info").pack(anchor="w")
    tb.Label(frame_t, text=descripcion, font=("Helvetica", 10), bootstyle="secondary", wraplength=520, justify="left").pack(anchor="w", pady=(4, 0))

# Contacto 
tab_contacto = tb.Frame(notebook, padding=20)
notebook.add(tab_contacto, text="📧 Contacto")

tb.Label(tab_contacto, text="¿Tienes algún problema o sugerencia?", font=("Helvetica", 13, "bold")).pack(pady=(0, 20))
tb.Label(tab_contacto, text="Correo de soporte:", font=("Helvetica", 10), bootstyle="secondary").pack(anchor="w")
tb.Label(tab_contacto, text="soporte@estresacademico.com", font=("Helvetica", 11), bootstyle="info").pack(anchor="w", pady=(4, 16))
tb.Label(tab_contacto, text="Tu mensaje:", font=("Helvetica", 10), bootstyle="secondary").pack(anchor="w")
texto_mensaje = tb.Text(tab_contacto, width=50, height=6, font=("Helvetica", 11))
texto_mensaje.pack(pady=(4, 16))

def enviar_mensaje():
    from tkinter import messagebox
    mensaje = texto_mensaje.get("1.0", "end").strip()
    if not mensaje:
        messagebox.showwarning("Vacío", "Escribe un mensaje antes de enviar.")
        return
    messagebox.showinfo("Enviado", "Tu mensaje fue enviado. Te responderemos pronto.")
    texto_mensaje.delete("1.0", "end")

tb.Button(tab_contacto, text="Enviar mensaje", bootstyle="info", width=20, command=enviar_mensaje).pack()

# Volver 
def volver():
    root.destroy()
    import subprocess
    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "vPrincipal.py")])

lbl_volver = tb.Label(frame, text="← Volver", bootstyle="info", cursor="hand2", font=("Helvetica", 9, "underline"))
lbl_volver.pack(pady=(12, 0))
lbl_volver.bind("<Button-1>", lambda e: volver())

root.mainloop()