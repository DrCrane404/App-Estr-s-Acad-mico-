# Update.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Service'))
import UsuarioService

def buscar_usuario():
    token = entry_token.get().strip()
    if not token:
        messagebox.showwarning("Campo vacío", "Ingresa tu token de sesión.")
        return

    respuesta = UsuarioService.ver_perfil(token)

    if respuesta.get("name") or respuesta.get("username"):
        entry_name.delete(0, "end")
        entry_name.insert(0, respuesta.get("name", ""))

        entry_username.delete(0, "end")
        entry_username.insert(0, respuesta.get("username", ""))

        root.token = token
        messagebox.showinfo("Usuario encontrado", "Puedes modificar los datos.")
    else:
        messagebox.showerror("Error", "Token inválido o sesión expirada.")


def actualizar():
    name     = entry_name.get().strip()
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    confirm  = entry_confirm.get().strip()

    if not all([name, username]):
        messagebox.showwarning("Campos vacíos", "Nombre y usuario son obligatorios.")
        return

    if password and password != confirm:
        messagebox.showerror("Error", "Las contraseñas no coinciden.")
        return

    if password and len(password) < 6:
        messagebox.showwarning("Error", "La contraseña debe tener al menos 6 caracteres.")
        return

    token = getattr(root, "token", None)
    if not token:
        messagebox.showerror("Error", "Primero busca tu usuario con el token.")
        return

    datos = {"name": name, "username": username}
    if password:
        datos["password"] = password

    respuesta = UsuarioService.actualizar_perfil(datos, token)

    if respuesta.get("success") or respuesta.get("name"):
        messagebox.showinfo("Éxito", "Información actualizada correctamente.")
        root.destroy()
        import subprocess
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "Login.py")])
    else:
        error = respuesta.get("error", "No se pudo actualizar la información.")
        messagebox.showerror("Error al actualizar", error)


def abrir_register():
    root.destroy()
    import subprocess
    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "Register.py")])


# Ventana principal 
root = tb.Window(themename="superhero")
root.title("Modificar información")
root.geometry("460x580")
root.resizable(False, False)
root.place_window_center()
root.usuario_id = None

# Frame central 
frame = tb.Frame(root, padding=40)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Título 
tb.Label(
    frame,
    text="Modificar cuenta",
    font=("Helvetica", 22, "bold"),
    bootstyle="inverse-default"
).pack(pady=(0, 5))

tb.Label(
    frame,
    text="Busca tu cuenta y edita tu información",
    font=("Helvetica", 10),
    bootstyle="secondary"
).pack(pady=(0, 20))

# Buscar por token
tb.Label(frame, text="Token de sesión", font=("Helvetica", 10)).pack(anchor="w")
frame_buscar = tb.Frame(frame)
frame_buscar.pack(fill="x", pady=(4, 16))

entry_token = tb.Entry(frame_buscar, width=26, font=("Helvetica", 11))
entry_token.pack(side="left", ipady=6)

tb.Button(
    frame_buscar,
    text="Buscar",
    bootstyle="info",
    command=buscar_usuario
).pack(side="left", padx=(8, 0))

# Nombre completo
tb.Label(frame, text="Nuevo nombre completo", font=("Helvetica", 10)).pack(anchor="w")
entry_name = tb.Entry(frame, width=35, font=("Helvetica", 11))
entry_name.pack(pady=(4, 12), ipady=6)

# Username 
tb.Label(frame, text="Nuevo nombre de usuario", font=("Helvetica", 10)).pack(anchor="w")
entry_username = tb.Entry(frame, width=35, font=("Helvetica", 11))
entry_username.pack(pady=(4, 12), ipady=6)

# Nueva contraseña
tb.Label(frame, text="Nueva contraseña (opcional)", font=("Helvetica", 10)).pack(anchor="w")
entry_password = tb.Entry(frame, width=35, font=("Helvetica", 11), show="●")
entry_password.pack(pady=(4, 12), ipady=6)

# Confirmar contraseña
tb.Label(frame, text="Confirmar nueva contraseña", font=("Helvetica", 10)).pack(anchor="w")
entry_confirm = tb.Entry(frame, width=35, font=("Helvetica", 11), show="●")
entry_confirm.pack(pady=(4, 20), ipady=6)

# Botón actualizar 
tb.Button(
    frame,
    text="Guardar cambios",
    bootstyle="warning",
    width=30,
    command=actualizar
).pack(pady=(0, 12))

# Enlace a register 
lbl_volver = tb.Label(
    frame,
    text="← Volver al registro",
    bootstyle="info",
    cursor="hand2",
    font=("Helvetica", 9, "underline")
)
lbl_volver.pack()
lbl_volver.bind("<Button-1>", lambda e: abrir_register())

root.mainloop()