# vPrincipal.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import sys
import os
import random
import string

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Service'))
import sesion
import UsuarioService

# Ventana principal 
root = tb.Window(themename="superhero")
root.title("Panel Principal")
root.geometry("1100x650")
root.resizable(False, False)
root.place_window_center()

tareas = []
def cargar_tareas_api():
    global tareas
    token = sesion.obtener()
    if not token:
        return
    respuesta = UsuarioService.obtener_mis_tareas(token)
    if isinstance(respuesta, list):
        tareas.clear()
        for t in respuesta:
            tareas.append({
                "task_id":    t.get("task_id"),
                "nombre":     t.get("title", ""),
                "descripcion": t.get("description", ""),
                "estres":     nivel_numerico_a_texto(t.get("stressLevel", 0)),
                "publica":    t.get("public", False),
                "codigo":     t.get("code") or "",
                "hecha":      t.get("completed", False),
                "tType":      t.get("tType", "PERSONAL"),
                "startDate":  t.get("startDate", ""),
                "finishDate": t.get("finishDate", "")
            })

#Conversion para el calculo de estres
def nivel_texto_a_numerico(texto):
    return {"Bajo": 2, "Moderado": 5, "Alto": 7, "Muy alto": 10}.get(texto, 2)

def nivel_numerico_a_texto(n):
    if n <= 2: return "Bajo"
    elif n <= 5: return "Moderado"
    elif n <= 7: return "Alto"
    else: return "Muy alto"
# Utilidades 
def generar_codigo():
    return "EST-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=3))

def calcular_estres_tareas():
    pesos = {"Bajo": 2, "Moderado": 4, "Alto": 7, "Muy alto": 10}
    tareas_activas = [t for t in tareas if not t["hecha"]]
    if not tareas_activas:
        return 0
    total = sum(pesos.get(t.get("estres", "Bajo"), 2) for t in tareas_activas)
    return min(round(total / len(tareas_activas), 1), 10)

def actualizar_barra_estres():
    nivel = calcular_estres_tareas()
    barra_estres["value"] = nivel * 10
    if nivel <= 2.5:
        categoria, estilo = "Bajo", "success"
    elif nivel <= 5:
        categoria, estilo = "Moderado", "info"
    elif nivel <= 7.5:
        categoria, estilo = "Alto", "warning"
    else:
        categoria, estilo = "Muy Alto", "danger"
    lbl_nivel_estres.config(text=f"{categoria} — {nivel} / 10", bootstyle=estilo)
    barra_estres.config(bootstyle=f"{estilo}-striped")

# Menú lateral 
menu_visible = [False]
frame_menu = tb.Frame(root, width=200, bootstyle="dark")
frame_menu.place(x=0, y=0, width=200, height=650)
frame_menu.place_forget()

def toggle_menu():
    if menu_visible[0]:
        frame_menu.place_forget()
        menu_visible[0] = False
    else:
        frame_menu.place(x=0, y=0, width=200, height=650)
        frame_menu.lift()
        menu_visible[0] = True

def abrir_perfil():
    toggle_menu()
    import subprocess
    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "vPerfil.py")])

def abrir_configuracion():
    toggle_menu()
    messagebox.showinfo("Configuración", "Próximamente...")

def cerrar_sesion():
    if messagebox.askyesno("Cerrar sesión", "¿Estás seguro?"):
        sesion.cerrar()
        root.destroy()
        import subprocess
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "Login.py")])

tb.Label(frame_menu, text="☰ Menú", font=("Helvetica", 14, "bold"), bootstyle="inverse-dark").pack(pady=(20, 30), padx=16, anchor="w")
tb.Button(frame_menu, text="👤  Perfil", bootstyle="dark", width=18, command=abrir_perfil).pack(pady=6, padx=16)
tb.Button(frame_menu, text="⚙️  Configuración", bootstyle="dark", width=18, command=abrir_configuracion).pack(pady=6, padx=16)
tb.Separator(frame_menu).pack(fill="x", padx=16, pady=20)
tb.Button(frame_menu, text="🚪  Cerrar sesión", bootstyle="danger", width=18, command=cerrar_sesion).pack(pady=6, padx=16)

# Barra superior 
frame_top = tb.Frame(root, bootstyle="dark")
frame_top.place(x=0, y=0, width=1100, height=55)

tb.Button(frame_top, text="☰", bootstyle="success", width=3, command=toggle_menu).place(x=10, y=10)

entry_busqueda = tb.Entry(frame_top, width=40, font=("Helvetica", 11))
entry_busqueda.place(x=70, y=13, height=30)

def buscar(texto):
    refrescar_tareas(filtro=texto.strip().lower())

tb.Button(frame_top, text="🔍", bootstyle="secondary", command=lambda: buscar(entry_busqueda.get())).place(x=350, y=10)
entry_busqueda.bind("<Return>", lambda e: buscar(entry_busqueda.get()))

tb.Button(frame_top, text="👤", bootstyle="warning", width=3, command=abrir_perfil).place(x=1050, y=10)

# Área principal 
frame_contenido = tb.Frame(root)
frame_contenido.place(x=0, y=55, width=1100, height=595)


# Panel izquierdo 
frame_tareas = tb.Frame(frame_contenido)
frame_tareas.place(x=10, y=10, width=700, height=570)

tb.Label(frame_tareas, text="Mis tareas y actividades", font=("Helvetica", 13, "bold"), bootstyle="success").pack(anchor="w", pady=(0, 8))

canvas_tareas = tb.Canvas(frame_tareas, highlightthickness=0)
scroll_tareas = tb.Scrollbar(frame_tareas, orient="vertical", command=canvas_tareas.yview)
canvas_tareas.configure(yscrollcommand=scroll_tareas.set)
scroll_tareas.pack(side="right", fill="y")
canvas_tareas.pack(side="left", fill="both", expand=True)

frame_lista = tb.Frame(canvas_tareas)
canvas_tareas.create_window((0, 0), window=frame_lista, anchor="nw")

def actualizar_scroll(event=None):
    canvas_tareas.configure(scrollregion=canvas_tareas.bbox("all"))

frame_lista.bind("<Configure>", actualizar_scroll)

tb.Button(
    frame_tareas,
    text="+ Nueva tarea",
    bootstyle="success",
    width=20,
    command=lambda: agregar_tarea_ui()
).place(x=10, y=530)


# Panel derecho 
frame_derecho = tb.Frame(frame_contenido)
frame_derecho.place(x=720, y=10, width=370, height=570)

tb.Label(frame_derecho, text="Nivel de estrés", font=("Helvetica", 12, "bold"), bootstyle="warning").pack(anchor="w", pady=(0, 4))

barra_estres = tb.Progressbar(frame_derecho, bootstyle="success-striped", value=0, maximum=100)
barra_estres.pack(fill="x", pady=(0, 4))

lbl_nivel_estres = tb.Label(frame_derecho, text="Sin tareas — 0 / 10", font=("Helvetica", 11, "bold"), bootstyle="success")
lbl_nivel_estres.pack(anchor="e", pady=(0, 4))

tb.Label(frame_derecho, text="El nivel se calcula según el estrés\nde tus tareas activas.", font=("Helvetica", 9), bootstyle="secondary", justify="right").pack(anchor="e", pady=(0, 12))

tb.Separator(frame_derecho).pack(fill="x", pady=8)

tb.Label(frame_derecho, text="Tareas públicas", font=("Helvetica", 12, "bold"), bootstyle="info").pack(anchor="w", pady=(0, 8))

frame_buscar_pub = tb.Frame(frame_derecho)
frame_buscar_pub.pack(fill="x", pady=(0, 8))

entry_codigo = tb.Entry(frame_buscar_pub, width=14, font=("Helvetica", 11))
entry_codigo.pack(side="left", ipady=4)

def ver_tarea_publica(tarea):
    ventana = tb.Toplevel(root)
    ventana.title("Tarea pública")
    ventana.geometry("420x380")
    ventana.resizable(False, False)
    ventana.place_window_center()

    frame = tb.Frame(ventana, padding=30)
    frame.pack(fill="both", expand=True)

    tb.Label(frame, text="🌐 Tarea pública", font=("Helvetica", 14, "bold"), bootstyle="info").pack(anchor="w", pady=(0, 4))
    tb.Separator(frame).pack(fill="x", pady=8)

    tb.Label(frame, text="Nombre:", font=("Helvetica", 10), bootstyle="secondary").pack(anchor="w")
    tb.Label(frame, text=tarea["nombre"], font=("Helvetica", 13, "bold")).pack(anchor="w", pady=(2, 12))

    tb.Label(frame, text="Descripción:", font=("Helvetica", 10), bootstyle="secondary").pack(anchor="w")
    tb.Label(frame, text=tarea.get("descripcion") or "Sin descripción", font=("Helvetica", 11), wraplength=360, justify="left").pack(anchor="w", pady=(2, 12))

    frame_info = tb.Frame(frame)
    frame_info.pack(fill="x", pady=(0, 12))

    tb.Label(frame_info, text=f"⏱ Horas/día: {tarea.get('horas', '-')}", font=("Helvetica", 11)).pack(side="left", padx=(0, 20))

    colores = {"Bajo": "success", "Moderado": "info", "Alto": "warning", "Muy alto": "danger"}
    estilo = colores.get(tarea.get("estres", "Bajo"), "secondary")
    tb.Label(frame_info, text=f"😰 Estrés: {tarea.get('estres', '-')}", font=("Helvetica", 11), bootstyle=estilo).pack(side="left")

    tb.Separator(frame).pack(fill="x", pady=8)
    tb.Label(frame, text=f"Código: {tarea.get('codigo', '')}", font=("Helvetica", 10), bootstyle="warning").pack(anchor="w", pady=(0, 16))
    tb.Button(frame, text="Cerrar", bootstyle="secondary", width=16, command=ventana.destroy).pack()

def buscar_tarea_publica():
    codigo = entry_codigo.get().strip().upper()
    if not codigo:
        messagebox.showwarning("Vacío", "Escribe un código para buscar.")
        return
    token = sesion.obtener()
    respuesta = UsuarioService.unirse_tarea(codigo, token)
    if respuesta.get("task_id"):
        messagebox.showinfo("¡Unido!", f"Te uniste a la tarea: {respuesta.get('title')}")
        cargar_tareas_api()
        refrescar_tareas()
        refrescar_publicas()
        actualizar_barra_estres()
    else:
        messagebox.showerror("No encontrada", "No existe una tarea pública con ese código.")

tb.Button(frame_buscar_pub, text="Buscar", bootstyle="info", command=buscar_tarea_publica).pack(side="left", padx=(8, 0))

frame_lista_publica = tb.Frame(frame_derecho)
frame_lista_publica.pack(fill="both", expand=True)

def refrescar_publicas():
    for widget in frame_lista_publica.winfo_children():
        widget.destroy()
    publicas = [t for t in tareas if t.get("publica")]
    if not publicas:
        tb.Label(frame_lista_publica, text="No tienes tareas públicas.", font=("Helvetica", 10), bootstyle="secondary").pack(pady=10)
        return
    for t in publicas:
        frame_pub = tb.Frame(frame_lista_publica)
        frame_pub.pack(fill="x", pady=3)
        tb.Label(frame_pub, text=f"🌐 {t['nombre']}  [{t['codigo']}]", font=("Helvetica", 11), bootstyle="info").pack(side="left")
        tb.Button(frame_pub, text="Ver", bootstyle="info-outline", command=lambda t=t: ver_tarea_publica(t)).pack(side="right")


# Formulario agregar/editar 
def agregar_tarea_ui(tarea_existente=None, indice=None):
    es_edicion = tarea_existente is not None

    ventana = tb.Toplevel(root)
    ventana.title("Editar tarea" if es_edicion else "Nueva tarea")
    ventana.geometry("400x600")
    ventana.resizable(False, False)
    ventana.place_window_center()
    ventana.grab_set()

    frame = tb.Frame(ventana, padding=20)
    frame.pack(fill="both", expand=True)

    tb.Label(frame, text="Editar tarea" if es_edicion else "Nueva tarea", font=("Helvetica", 15, "bold")).pack(pady=(0, 16))

    tb.Label(frame, text="Nombre de la tarea", font=("Helvetica", 11)).pack(anchor="w")
    entry_nombre = tb.Entry(frame, width=38, font=("Helvetica", 12))
    entry_nombre.pack(pady=(4, 10), ipady=5)
    if es_edicion:
        entry_nombre.insert(0, tarea_existente["nombre"])

    tb.Label(frame, text="Descripción", font=("Helvetica", 11)).pack(anchor="w")
    entry_desc = tb.Text(frame, width=38, height=3, font=("Helvetica", 11))
    entry_desc.pack(pady=(4, 10))
    if es_edicion and tarea_existente.get("descripcion"):
        entry_desc.insert("1.0", tarea_existente["descripcion"])

    tb.Label(frame, text="Horas asignadas por día", font=("Helvetica", 11)).pack(anchor="w")
    entry_horas = tb.Spinbox(frame, from_=0.5, to=12, increment=0.5, width=10, font=("Helvetica", 11))
    entry_horas.pack(anchor="w", pady=(4, 10), ipady=4)
    if es_edicion and tarea_existente.get("horas"):
        entry_horas.delete(0, "end")
        entry_horas.insert(0, tarea_existente["horas"])

    tb.Label(frame, text="Nivel de estrés que genera", font=("Helvetica", 11)).pack(anchor="w")
    frame_niveles = tb.Frame(frame)
    frame_niveles.pack(fill="x", pady=(4, 10))

    niveles = ["Bajo", "Moderado", "Alto", "Muy alto"]
    colores  = ["success", "info", "warning", "danger"]
    nivel_sel = tb.StringVar(value=tarea_existente.get("estres", "Bajo") if es_edicion else "Bajo")

    tb.Label(frame, text="Tipo de actividad", font=("Helvetica", 11)).pack(anchor="w")
    frame_tipos = tb.Frame(frame)
    frame_tipos.pack(fill="x", pady=(4, 10))

    tipo_sel = tb.StringVar(value=tarea_existente.get("tType", "ACADEMIA") if es_edicion else "ACADEMIA")
    tb.Radiobutton(frame_tipos, text="Académica", variable=tipo_sel, value="ACADEMIA", bootstyle="info").pack(side="left", padx=6)
    tb.Radiobutton(frame_tipos, text="Recreativa", variable=tipo_sel, value="RECREATIVA", bootstyle="success").pack(side="left", padx=6)

    for nivel, color in zip(niveles, colores):
        tb.Radiobutton(frame_niveles, text=nivel, variable=nivel_sel, value=nivel, bootstyle=color).pack(side="left", padx=6)

    tb.Separator(frame).pack(fill="x", pady=10)

    es_publica = tb.BooleanVar(value=tarea_existente.get("publica", False) if es_edicion else False)
    lbl_codigo = tb.Label(frame, text="", font=("Helvetica", 10), bootstyle="warning")
    codigo_actual = [tarea_existente.get("codigo") if es_edicion else None]

    def toggle_publica():
        if es_publica.get():
            if not codigo_actual[0]:
                codigo_actual[0] = generar_codigo()
            lbl_codigo.config(text=f"Código: {codigo_actual[0]}  🌐 Compártelo")
            lbl_codigo.pack(anchor="w", pady=(4, 0))
        else:
            lbl_codigo.pack_forget()

    tb.Checkbutton(frame, text="Hacer tarea pública", variable=es_publica, bootstyle="info", command=toggle_publica).pack(anchor="w")

    if es_edicion and tarea_existente.get("publica"):
        toggle_publica()

    def guardar():
        nombre  = entry_nombre.get().strip()
        desc    = entry_desc.get("1.0", "end").strip()
        horas   = entry_horas.get().strip()
        nivel   = nivel_sel.get()
        publica = es_publica.get()
        codigo  = codigo_actual[0] if publica else None

        if not nombre:
            messagebox.showwarning("Campo vacío", "Escribe el nombre de la tarea.", parent=ventana)
            return

        token = sesion.obtener()
        from datetime import date
        hoy = str(date.today())

        if es_edicion:
            respuesta = UsuarioService.actualizar_tarea(tarea_existente["task_id"], {
                "title": nombre,
                "description": desc,
                "stressLevel": nivel_texto_a_numerico(nivel),
                "public": publica,
                "code": codigo
            }, token)
            if respuesta.get("task_id") or respuesta.get("title"):
                messagebox.showinfo("Éxito", "Tarea actualizada.", parent=ventana)
            else:
                messagebox.showerror("Error", respuesta.get("message", "No se pudo actualizar."), parent=ventana)
                return
        else:
            respuesta = UsuarioService.crear_tarea({
                "title": nombre,
                "description": desc or "Sin descripción",
                "stressLevel": nivel_texto_a_numerico(nivel),
                "tType": tipo_sel.get(),
                "startDate": hoy,
                "finishDate": hoy,
                "public": publica,
                "code": codigo
            }, token)
            if respuesta.get("task_id"):
                if publica and codigo:
                    messagebox.showinfo("Tarea pública", f"Código de acceso: {codigo}\n\nCompártelo con quien quieras.", parent=ventana)
            else:
                messagebox.showerror("Error", respuesta.get("message", "No se pudo crear la tarea."), parent=ventana)
                return

        ventana.destroy()
        cargar_tareas_api()
        refrescar_tareas()
        refrescar_publicas()
        actualizar_barra_estres()
    tb.Button(frame, text="Guardar cambios" if es_edicion else "Guardar tarea", bootstyle="success", width=22, command=guardar).pack(pady=(14, 10), side="bottom")

# Refrescar tareas 
def refrescar_tareas(filtro=""):
    for widget in frame_lista.winfo_children():
        widget.destroy()

    tareas_mostrar = [t for t in tareas if filtro in t["nombre"].lower()] if filtro else tareas

    if not tareas_mostrar:
        msg = f"Sin resultados para '{filtro}'" if filtro else "No tienes tareas.\nPresiona '+ Nueva tarea'."
        tb.Label(frame_lista, text=msg, bootstyle="secondary", font=("Helvetica", 11), justify="center").pack(pady=40)
        actualizar_scroll()
        return

    for i, tarea in enumerate(tareas):
        if filtro and filtro not in tarea["nombre"].lower():
            continue

        es_resultado = bool(filtro and filtro in tarea["nombre"].lower())
        frame_t = tb.Frame(frame_lista, bootstyle="warning" if es_resultado else "dark")
        frame_t.pack(fill="x", padx=4, pady=6, ipady=10)

        var = tb.BooleanVar(value=tarea["hecha"])

        def marcar(i=i, var=var):
            token = sesion.obtener()
            UsuarioService.completar_tarea(tareas[i]["task_id"], token)
            tareas[i]["hecha"] = var.get()
            actualizar_barra_estres()
            refrescar_tareas(filtro)

        tb.Checkbutton(frame_t, variable=var, bootstyle="success", command=marcar).pack(side="left", padx=8)

        estilo = "secondary" if tarea["hecha"] else "default"
        texto = f"✓ {tarea['nombre']}" if tarea["hecha"] else tarea["nombre"]
        if tarea.get("horas"):
            texto += f"  ⏱{tarea['horas']}h"
        if tarea.get("estres"):
            texto += f"  😰{tarea['estres']}"
        if tarea.get("publica"):
            texto += f"  🌐[{tarea['codigo']}]"
        else:
            texto += "  🔒"

        tb.Label(frame_t, text=texto, font=("Helvetica", 14), bootstyle=estilo).pack(side="left", pady=8)

        tb.Button(frame_t, text="✏️", bootstyle="info-link", command=lambda i=i: agregar_tarea_ui(tareas[i], i)).pack(side="right", padx=4)
        tb.Button(frame_t, text="🗑", bootstyle="danger-link", command=lambda i=i: eliminar_tarea(i)).pack(side="right", padx=4)

    actualizar_scroll()

def eliminar_tarea(i):
    if messagebox.askyesno("Eliminar", f"¿Eliminar '{tareas[i]['nombre']}'?"):
        token = sesion.obtener()
        print("TASK ID:", tareas[i].get("task_id"))
        respuesta = UsuarioService.eliminar_tarea(tareas[i]["task_id"], token)
        print("RESPUESTA:", respuesta)
        cargar_tareas_api()
        refrescar_tareas()
        refrescar_publicas()
        actualizar_barra_estres()

#INICIAR
cargar_tareas_api()
refrescar_tareas()
refrescar_publicas()
actualizar_barra_estres()
root.mainloop()