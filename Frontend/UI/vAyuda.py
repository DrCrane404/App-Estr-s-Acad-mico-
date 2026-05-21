# vAyuda.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import sys
import os

root = tb.Window(themename="superhero")
root.title("Ayuda")
root.geometry("600x620")
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

# Pestaña 1: Tutorial 
tab_tutorial = tb.Frame(notebook, padding=20)
notebook.add(tab_tutorial, text="📖 Tutorial")

pasos = [
    ("1. Regístrate", "Crea tu cuenta con tu nombre, correo y contraseña en la pantalla de registro."),
    ("2. Inicia sesión", "Usa tu correo y contraseña para acceder a la app."),
    ("3. Completa el cuestionario", "La primera vez responde el cuestionario de estrés académico para conocer tu nivel."),
    ("4. Gestiona tus tareas", "Agrega, completa y elimina tus tareas desde la pantalla principal."),
    ("5. Revisa tu perfil", "Actualiza tu información personal desde el menú de perfil."),
    ("6. Monitorea tu estrés", "Consulta tu nivel de estrés en la barra de la pantalla principal."),
]

for titulo, descripcion in pasos:
    frame_paso = tb.Frame(tab_tutorial, bootstyle="dark", padding=12)
    frame_paso.pack(fill="x", pady=6)
    tb.Label(frame_paso, text=titulo, font=("Helvetica", 11, "bold"), bootstyle="info").pack(anchor="w")
    tb.Label(frame_paso, text=descripcion, font=("Helvetica", 10), bootstyle="secondary", wraplength=480, justify="left").pack(anchor="w", pady=(4, 0))

# Pestaña 2: FAQ 
tab_faq = tb.Frame(notebook, padding=20)
notebook.add(tab_faq, text="❓ Preguntas frecuentes")

faqs = [
    ("¿Puedo cambiar mi contraseña?", "Sí, desde tu perfil puedes actualizar tu contraseña cuando quieras."),
    ("¿Qué pasa si cierro el cuestionario a medias?", "Tu progreso se guarda automáticamente. La próxima vez continuarás donde lo dejaste."),
    ("¿Las tareas se guardan en el servidor?", "Por ahora las tareas se guardan localmente en tu sesión actual."),
    ("¿Cómo se calcula mi nivel de estrés?", "Con base en tus respuestas del cuestionario en áreas de sueño, académico, emocional, familiar y trabajo."),
    ("¿Puedo hacer el cuestionario más de una vez?", "Sí, puedes repetirlo desde el menú principal para actualizar tu nivel de estrés."),
]

for pregunta, respuesta in faqs:
    frame_faq = tb.Frame(tab_faq, bootstyle="dark", padding=12)
    frame_faq.pack(fill="x", pady=6)
    tb.Label(frame_faq, text=f"❓ {pregunta}", font=("Helvetica", 11, "bold"), bootstyle="warning").pack(anchor="w")
    tb.Label(frame_faq, text=respuesta, font=("Helvetica", 10), bootstyle="secondary", wraplength=480, justify="left").pack(anchor="w", pady=(4, 0))

# Pestaña 3: Contacto 
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