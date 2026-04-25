# Pantalla Login.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import sys
import os

# Importar el servicio (ruta)
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Service'))
import UsuarioService

def iniciar_login():
    """Se ejecuta al presionar el botón Entrar"""
    email = entry_email.get().strip()
    password = entry_password.get().strip()

    # Validación básica antes de llamar al servidor
    if not email or not password:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    # Llamar al servicio
    respuesta = UsuarioService.login(email, password)

    if respuesta.get("Success") or respuesta.get("token"):
        messagebox.showinfo("Éxito", "¡Bienvenido!")
        # Aquí se abre la siguiente pantalla y cerrar el login
        root.destroy()
    else:
        error = respuesta.get("error", "Credenciales incorrectas")
        messagebox.showerror("Error al iniciar sesión", error)


#Ventana principal 
root = tb.Window(themename="superhero")
root.title("Iniciar sesión")
root.geometry("420x480")
root.resizable(False, False)

# Centrar la ventana en pantalla
root.place_window_center()

# Frame central (tarjeta del formulario) 
frame = tb.Frame(root, padding=40)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Título 
tb.Label(
    frame,
    text="Iniciar sesión",
    font=("Helvetica", 22, "bold"),
    bootstyle="inverse-default"    # texto claro sobre fondo oscuro
).pack(pady=(0, 5))

tb.Label(
    frame,
    text="Ingresa tus credenciales para continuar",
    font=("Helvetica", 10),
    bootstyle="secondary"
).pack(pady=(0, 25))

# Campo email 
tb.Label(frame, text="Correo electrónico", font=("Helvetica", 10)).pack(anchor="w")
entry_email = tb.Entry(frame, width=32, font=("Helvetica", 11))
entry_email.pack(pady=(4, 16), ipady=6)

# Campo contraseña 
tb.Label(frame, text="Contraseña", font=("Helvetica", 10)).pack(anchor="w")
entry_password = tb.Entry(frame, width=32, font=("Helvetica", 11), show="●")
entry_password.pack(pady=(4, 24), ipady=6)

# Botón entrar 
tb.Button(
    frame,
    text="Entrar",
    bootstyle="success",
    width=28,
    command=iniciar_login
).pack(pady=(0, 12))

# Agrega esta función antes de crear la ventana
def abrir_registro():
    root.destroy()  # cierra el login
    import subprocess
    import sys
    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "Register.py")])

# Enlace a registro 
lbl_registro = tb.Label(
    frame,
    text="¿No tienes cuenta? Regístrate",
    bootstyle="info",
    cursor="hand2",
    font=("Helvetica", 9, "underline")
)
lbl_registro.pack()
lbl_registro.bind("<Button-1>", lambda e: abrir_registro())  # ← clic izquierdo

# Presionar Enter también dispara el login
root.bind("<Return>", lambda e: iniciar_login())

root.mainloop()

