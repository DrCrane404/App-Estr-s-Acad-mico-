# Pantalla Register.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import sys
import os

# Importar el servicio (ruta)
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Service'))
import UsuarioService

def register():
    """Se ejecuta al presionar el botón Entrar"""
    name = entry_name.get().strip()
    username = entry_username.get().strip()
    email = entry_email.get().strip()
    password = entry_password.get().strip()
    confirm = entry_confirm.get().strip()
    r_question =combo_question.get().strip()
    r_answer = entry_answer.get().strip()
    

    # Validación básica antes de llamar al servidor
    if not all ([name, username, email, password, confirm, r_question, r_answer]):
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return
    
    if password != confirm:
        messagebox.showerror("Error", "Las contraseñas no coinciden.")
        return

    if len(password) < 6:
        messagebox.showwarning("Error", "La contraseña debe ser de al menos 6 caracteres")

    # Llamar al servicio
    respuesta = UsuarioService.login(name, username, email, password, confirm, r_question, r_answer)

    if respuesta.get("Success") or respuesta.get("token"):
        messagebox.showinfo("Registro exitoso", f"¡Bienvenido, {name}! Tu cuenta fue creada.")
        # Aquí se abre la siguiente pantalla y cerrar el login
        root.destroy()
    else:
        error = respuesta.get("error", "No se pudo completar el registro.")
        messagebox.showerror("Error al registarse", error)


#Ventana principal 
root = tb.Window(themename="superhero")
root.title("Registro")
root.geometry("460x620")
root.resizable(False, False)
root.place_window_center()

# Frame central 
frame = tb.Frame(root, padding=40)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Título 
tb.Label(
    frame,
    text="Crear cuenta",
    font=("Helvetica", 22, "bold"),
    bootstyle="inverse-default"
).pack(pady=(0, 5))

tb.Label(
    frame,
    text="Completa los datos para registrarte",
    font=("Helvetica", 10),
    bootstyle="secondary"
).pack(pady=(0, 20))

# Nombre completo 
tb.Label(frame, text="Nombre completo", font=("Helvetica", 10)).pack(anchor="w")
entry_name = tb.Entry(frame, width=35, font=("Helvetica", 11))
entry_name.pack(pady=(4, 12), ipady=6)

# Username 
tb.Label(frame, text="Nombre de usuario", font=("Helvetica", 10)).pack(anchor="w")
entry_username = tb.Entry(frame, width=35, font=("Helvetica", 11))
entry_username.pack(pady=(4, 12), ipady=6)

# Email 
tb.Label(frame, text="Correo electrónico", font=("Helvetica", 10)).pack(anchor="w")
entry_email = tb.Entry(frame, width=35, font=("Helvetica", 11))
entry_email.pack(pady=(4, 12), ipady=6)

# Contraseña 
tb.Label(frame, text="Contraseña", font=("Helvetica", 10)).pack(anchor="w")
entry_password = tb.Entry(frame, width=35, font=("Helvetica", 11), show="●")
entry_password.pack(pady=(4, 12), ipady=6)

# Confirmar contraseña 
tb.Label(frame, text="Confirmar contraseña", font=("Helvetica", 10)).pack(anchor="w")
entry_confirm = tb.Entry(frame, width=35, font=("Helvetica", 11), show="●")
entry_confirm.pack(pady=(4, 12), ipady=6)

# Pregunta de seguridad 
tb.Label(frame, text="Pregunta de seguridad", font=("Helvetica", 10)).pack(anchor="w")
preguntas = [
    "¿Cuál es el nombre de tu primera mascota?",
    "¿En qué ciudad naciste?",
    "¿Cuál es el apellido de tu madre?",
    "¿Cuál fue tu primer trabajo?",
    "¿Cuál es tu comida favorita?"
]
combo_question = tb.Combobox(frame, values=preguntas, width=33, font=("Helvetica", 10), state="readonly")
combo_question.pack(pady=(4, 12), ipady=4)

# Respuesta de seguridad 
tb.Label(frame, text="Respuesta", font=("Helvetica", 10)).pack(anchor="w")
entry_answer = tb.Entry(frame, width=35, font=("Helvetica", 11))
entry_answer.pack(pady=(4, 20), ipady=6)

# Botón registrarse 
tb.Button(
    frame,
    text="Registrarse",
    bootstyle="success",
    width=30,
    command=register
).pack(pady=(0, 12))

# Función para volver al login
def abrir_login():
    root.destroy()
    import subprocess
    import sys
    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "Login.py")])

# Enlace a login 
lbl_login = tb.Label(
    frame,
    text="¿Ya tienes cuenta? Inicia sesión",
    bootstyle="info",
    cursor="hand2",
    font=("Helvetica", 9, "underline")
)
lbl_login.pack()
lbl_login.bind("<Button-1>", lambda e: abrir_login())

root.bind("<Return>", lambda e: register())

root.mainloop()