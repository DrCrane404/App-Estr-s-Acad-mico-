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

def recuperar_contraseña():
    """Abre una ventana emergente para recuperar la contraseña en dos pasos."""
    ventana = tb.Toplevel(root)
    ventana.title("Recuperar contraseña")
    ventana.geometry("380x320")
    ventana.resizable(False, False)
    ventana.place_window_center()
    ventana.grab_set()  # bloquea la ventana principal mientras esta está abierta

    frame = tb.Frame(ventana, padding=30)
    frame.pack(fill="both", expand=True)

    tb.Label(frame, text="Recuperar contraseña", font=("Helvetica", 16, "bold")).pack(pady=(0, 5))
    tb.Label(frame, text="Ingresa tu correo para recibir un código", font=("Helvetica", 9),
             bootstyle="secondary").pack(pady=(0, 20))

    # --- Paso 1: Email ---
    tb.Label(frame, text="Correo electrónico", font=("Helvetica", 10)).pack(anchor="w")
    entry_rec_email = tb.Entry(frame, width=30, font=("Helvetica", 11))
    entry_rec_email.pack(pady=(4, 12), ipady=5)

    # --- Paso 2: Código + nueva contraseña (ocultos al inicio) ---
    frame_paso2 = tb.Frame(frame)  # se muestra solo después de enviar el código

    tb.Label(frame_paso2, text="Código recibido", font=("Helvetica", 10)).pack(anchor="w")
    entry_codigo = tb.Entry(frame_paso2, width=30, font=("Helvetica", 11))
    entry_codigo.pack(pady=(4, 10), ipady=5)

    tb.Label(frame_paso2, text="Nueva contraseña", font=("Helvetica", 10)).pack(anchor="w")
    entry_nueva = tb.Entry(frame_paso2, width=30, font=("Helvetica", 11), show="●")
    entry_nueva.pack(pady=(4, 16), ipady=5)

    def enviar_codigo():
        email = entry_rec_email.get().strip()
        if not email:
            messagebox.showwarning("Campo vacío", "Ingresa tu correo.", parent=ventana)
            return

        respuesta = UsuarioService.solicitar_codigo_recuperacion(email)

        if respuesta.get("Success"):
            messagebox.showinfo("Código enviado",
                                f"Se envió un código a {email}. Revisa tu correo.", parent=ventana)
            btn_enviar.config(state="disabled")
            entry_rec_email.config(state="readonly")
            frame_paso2.pack(fill="x")          # muestra el paso 2
            btn_confirmar.pack(fill="x", pady=(0, 8))
        else:
            error = respuesta.get("error", "No se pudo enviar el código")
            messagebox.showerror("Error", error, parent=ventana)

    def confirmar_cambio():
        codigo = entry_codigo.get().strip()
        nueva = entry_nueva.get().strip()
        email = entry_rec_email.get().strip()

        if not codigo or not nueva:
            messagebox.showwarning("Campos vacíos", "Llena el código y la nueva contraseña.", parent=ventana)
            return
        if len(nueva) < 6:
            messagebox.showwarning("Contraseña débil", "La contraseña debe tener al menos 6 caracteres.", parent=ventana)
            return

        respuesta = UsuarioService.cambiar_contraseña(email, codigo, nueva)

        if respuesta.get("Success"):
            messagebox.showinfo("¡Listo!", "Tu contraseña fue actualizada. Ya puedes iniciar sesión.", parent=ventana)
            ventana.destroy()
        else:
            error = respuesta.get("error", "Código incorrecto o expirado")
            messagebox.showerror("Error", error, parent=ventana)

    btn_enviar = tb.Button(frame, text="Enviar código", bootstyle="info", width=26, command=enviar_codigo)
    btn_enviar.pack(pady=(0, 8))

    # Este botón se agrega al frame pero se muestra solo en el paso 2
    btn_confirmar = tb.Button(frame, text="Cambiar contraseña", bootstyle="success", width=26, command=confirmar_cambio)


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
tb.Label(
    frame, 
    text="Correo electrónico", 
    font=("Helvetica", 10)).pack(anchor="w")
entry_email = tb.Entry(frame, width=32, font=("Helvetica", 11))
entry_email.pack(pady=(4, 16), ipady=6)

# Campo contraseña 
tb.Label(
    frame, 
    text="Contraseña", 
    font=("Helvetica", 10)).pack(anchor="w")
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

#Boton recuperacion de contrasena
tb.Button(
    frame,
    text="¿Olvidaste tu contraseña?",
    bootstyle="link",
    width=28,
    command=recuperar_contraseña
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

