# vPerfil.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Service'))
import UsuarioService
import sesion

root = tb.Window(themename="superhero")
root.title("Mi Perfil")
root.geometry("500x800")
root.resizable(False, False)
root.place_window_center()

frame = tb.Frame(root, padding=30)
frame.pack(fill="both", expand=True)

tb.Label(frame, text="Mi Perfil", font=("Helvetica", 20, "bold"), bootstyle="inverse-default").pack(pady=(0, 20))

# Campos 
tb.Label(frame, text="Nombre completo", font=("Helvetica", 10)).pack(anchor="w")
entry_nombre = tb.Entry(frame, width=40, font=("Helvetica", 11))
entry_nombre.pack(pady=(4, 12), ipady=5)

tb.Label(frame, text="Nombre de usuario", font=("Helvetica", 10)).pack(anchor="w")
entry_username = tb.Entry(frame, width=40, font=("Helvetica", 11))
entry_username.pack(pady=(4, 12), ipady=5)

tb.Label(frame, text="Correo electrónico", font=("Helvetica", 10)).pack(anchor="w")
entry_email = tb.Entry(frame, width=40, font=("Helvetica", 11))
entry_email.pack(pady=(4, 12), ipady=5)

tb.Separator(frame).pack(fill="x", pady=12)

tb.Label(frame, text="Nueva contraseña (opcional)", font=("Helvetica", 10)).pack(anchor="w")
entry_password = tb.Entry(frame, width=40, font=("Helvetica", 11), show="●")
entry_password.pack(pady=(4, 12), ipady=5)

tb.Label(frame, text="Confirmar nueva contraseña", font=("Helvetica", 10)).pack(anchor="w")
entry_confirm = tb.Entry(frame, width=40, font=("Helvetica", 11), show="●")
entry_confirm.pack(pady=(4, 20), ipady=5)

# Cargar perfil 
def cargar_perfil():
    token = sesion.obtener()
    if not token:
        return
    respuesta = UsuarioService.ver_perfil(token)
    if respuesta.get("name"):
        entry_nombre.insert(0, respuesta.get("name", ""))
        entry_username.insert(0, respuesta.get("username", ""))
        entry_email.insert(0, respuesta.get("email", ""))

# Guardar cambios 
def guardar_cambios():
    nombre   = entry_nombre.get().strip()
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    confirm  = entry_confirm.get().strip()

    if not all([nombre, username]):
        messagebox.showwarning("Campos vacíos", "Nombre y usuario son obligatorios.")
        return
    if password and password != confirm:
        messagebox.showerror("Error", "Las contraseñas no coinciden.")
        return
    if password and len(password) < 6:
        messagebox.showwarning("Error", "La contraseña debe tener al menos 6 caracteres.")
        return

    token = sesion.obtener()
    if not token:
        messagebox.showerror("Error", "No hay sesión activa.")
        return

    datos = {"name": nombre, "username": username}
    if password:
        datos["password"] = password

    respuesta = UsuarioService.actualizar_perfil(datos, token)
    if respuesta.get("success") or respuesta.get("name"):
        messagebox.showinfo("Éxito", "Perfil actualizado correctamente.")
    else:
        error = respuesta.get("error", "No se pudo actualizar el perfil.")
        messagebox.showerror("Error", error)

tb.Button(frame, text="Guardar cambios", bootstyle="success", width=30, command=guardar_cambios).pack(pady=(0, 8))

def volver():
    root.destroy()

lbl_volver = tb.Label(frame, text="← Volver", bootstyle="info", cursor="hand2", font=("Helvetica", 9, "underline"))
lbl_volver.pack()
lbl_volver.bind("<Button-1>", lambda e: volver())

cargar_perfil()
root.mainloop()