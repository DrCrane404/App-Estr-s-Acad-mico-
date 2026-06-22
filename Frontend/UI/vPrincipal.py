# vPrincipal.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import date, timedelta
import calendar as cal_module
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
root.resizable(True, True)
root.place_window_center()

tareas = []

import base64
import json

def obtener_id_usuario():
    token = sesion.obtener()
    if not token:
        return None
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        datos = json.loads(base64.urlsafe_b64decode(payload))
        return datos.get("id")
    except Exception:
        return None
    

def cargar_tareas_api():
    global tareas
    token = sesion.obtener()
    if not token:
        return
    mi_id = obtener_id_usuario()
    respuesta = UsuarioService.obtener_mis_tareas(token)
    if isinstance(respuesta, list):
        tareas.clear()
        for t in respuesta:
            tareas.append({
                "task_id":    t.get("task_id"),
                "nombre":     t.get("title", ""),
                "descripcion": t.get("description", ""),
                "estres":     nivel_numerico_a_texto(t.get("stressLevel") or 0),
                "publica":    t.get("public", False),
                "codigo":     t.get("code") or "",
                "hecha":      t.get("completed", False),
                "tType":      t.get("tType", "PERSONAL"),
                "startDate":  t.get("startDate", ""),
                "finishDate": t.get("finishDate", ""),
                "esDueno":    t.get("user", {}).get("id") == mi_id
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

import random

MENSAJES_POSITIVOS = [
    "¡Hoy es un buen día para avanzar un poco más! 💪",
    "Recuerda: el descanso también es productividad. 😴",
    "Cada tarea que completas es un paso hacia tu meta. 🎯",
    "Eres capaz de más de lo que crees. ¡Sigue adelante! 🌟",
    "Tómate un respiro, lo estás haciendo muy bien. 🌿",
    "El estrés es temporal, tu esfuerzo es permanente. 🔥",
    "Un día a la vez, un paso a la vez. ¡Tú puedes! 🚀",
    "No olvides tomar agua y estirar un poco hoy. 💧",
    "Estás más cerca de lograrlo de lo que piensas. ✨",
    "El mejor momento para empezar fue ayer, el segundo mejor es ahora. 📚",
]

def mostrar_mensaje_positivo():
    mensaje = random.choice(MENSAJES_POSITIVOS)
    ventana = tb.Toplevel(root)
    ventana.title("Mensaje del día")
    ventana.geometry("380x180")
    ventana.resizable(False, False)
    ventana.place_window_center()

    frame = tb.Frame(ventana, padding=30)
    frame.pack(fill="both", expand=True)

    tb.Label(
        frame,
        text="💬 Mensaje del día",
        font=("Helvetica", 11, "bold"),
        bootstyle="info"
    ).pack(pady=(0, 12))

    tb.Label(
        frame,
        text=mensaje,
        font=("Helvetica", 12),
        wraplength=320,
        justify="center"
    ).pack(pady=(0, 16))

    tb.Button(
        frame,
        text="¡Gracias! 😊",
        bootstyle="success",
        width=16,
        command=ventana.destroy
    ).pack()

    ventana.after(8000, ventana.destroy)  # se cierra solo a los 8 segundos

def generar_codigo():
    return "EST-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=3))

# calendario
def calcular_horas_por_dia():
    """Regresa un diccionario {fecha: horas_totales} sumando horasDia de cada tarea activa por cada día entre su inicio y fin"""
    token = sesion.obtener()
    respuesta = UsuarioService.obtener_mis_tareas(token)
    
    horas_por_dia = {}
    if isinstance(respuesta, list):
        for t in respuesta:
            if t.get("completed"):
                continue
            horas_dia = t.get("horasDia", 0)
            inicio = date.fromisoformat(t["startDate"][:10])
            fin = date.fromisoformat(t["finishDate"][:10])
            
            actual = inicio
            while actual <= fin:
                horas_por_dia[actual] = horas_por_dia.get(actual, 0) + horas_dia
                actual += timedelta(days=1)
    
    return horas_por_dia


def verificar_alerta_horario(inicio_str, fin_str, horas_nuevas, excluir_task_id=None):
    """Verifica si una tarea hace que algún día supere las 16 horas"""
    try:
        inicio = date.fromisoformat(inicio_str[:10])
        fin = date.fromisoformat(fin_str[:10])
        horas_nuevas = float(horas_nuevas or 0)
    except (ValueError, TypeError):
        return None

    # Calcular horas existentes, excluyendo la tarea que se está editando
    horas_por_dia = {}
    for tarea in tareas:
        if tarea["hecha"]:
            continue
        if excluir_task_id and tarea.get("task_id") == excluir_task_id:
            continue
        try:
            t_inicio = date.fromisoformat(str(tarea.get("startDate", ""))[:10])
            t_fin = date.fromisoformat(str(tarea.get("finishDate", ""))[:10])
            t_horas = float(tarea.get("horas", 0) or 0)
        except (ValueError, TypeError):
            continue
        dia_actual = t_inicio
        while dia_actual <= t_fin:
            horas_por_dia[dia_actual] = horas_por_dia.get(dia_actual, 0) + t_horas
            dia_actual += timedelta(days=1)

    dias_en_peligro = []
    dia_actual = inicio
    while dia_actual <= fin:
        total = horas_por_dia.get(dia_actual, 0) + horas_nuevas
        if total > 16:
            dias_en_peligro.append((dia_actual, total))
        dia_actual += timedelta(days=1)

    return dias_en_peligro if dias_en_peligro else None

def calcular_estres_tareas():
    pesos = {"Bajo": 2, "Moderado": 4, "Alto": 7, "Muy alto": 10}
    tareas_activas = [t for t in tareas if not t["hecha"]]
    if not tareas_activas:
        return 0
    total = sum(pesos.get(t.get("estres", "Bajo"), 2) for t in tareas_activas)
    return min(round(total / len(tareas_activas), 1), 10)

def actualizar_barra_estres():
    token = sesion.obtener()
    if token:
        respuesta = UsuarioService.obtener_nivel_estres(token)
        nivel = respuesta.get("nivelFinal",0) if respuesta.get("existe") else 0
    else:
        nivel = 0

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

    # Sugerencia de ayuda si el estrés es alto 
    if nivel > 7.5:
        root.after(3000, sugerir_ayuda)  # aparece 3s después de cargar


def sugerir_ayuda():
    ventana = tb.Toplevel(root)
    ventana.title("⚠️ Nivel de estrés elevado")
    ventana.geometry("400x220")
    ventana.resizable(False, False)
    ventana.place_window_center()

    frame = tb.Frame(ventana, padding=30)
    frame.pack(fill="both", expand=True)

    tb.Label(
        frame,
        text="⚠️ Tu nivel de estrés es muy alto",
        font=("Helvetica", 13, "bold"),
        bootstyle="danger"
    ).pack(pady=(0, 8))

    tb.Label(
        frame,
        text="Te recomendamos visitar el apartado de Ayuda.\nEncontrarás técnicas y recursos para manejar el estrés.",
        font=("Helvetica", 11),
        wraplength=340,
        justify="center",
        bootstyle="secondary"
            ).pack(pady=(0, 20))

    frame_btn = tb.Frame(frame)
    frame_btn.pack()

    def ir_a_ayuda():
        ventana.destroy()
        import subprocess
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "vAyuda.py")])

    tb.Button(frame_btn, text="Ir a Ayuda", bootstyle="warning", width=14, command=ir_a_ayuda).pack(side="left", padx=(0, 8))
    tb.Button(frame_btn, text="Cerrar", bootstyle="secondary-outline", width=10, command=ventana.destroy).pack(side="left")

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
        # Al hacer clic fuera del menú se cierra
        root.bind("<Button-1>", cerrar_menu_si_clic_fuera)

def cerrar_menu_si_clic_fuera(event):
    x, y = event.x_root, event.y_root
    mx = frame_menu.winfo_rootx()
    my = frame_menu.winfo_rooty()
    mw = frame_menu.winfo_width()
    mh = frame_menu.winfo_height()

    # También ignora clics en la barra superior donde está el botón ☰
    bx = frame_top.winfo_rootx()
    by = frame_top.winfo_rooty()
    bw = frame_top.winfo_width()
    bh = frame_top.winfo_height()

    dentro_menu = mx <= x <= mx + mw and my <= y <= my + mh
    dentro_barra = bx <= x <= bx + bw and by <= y <= by + bh

    if not dentro_menu and not dentro_barra:
        frame_menu.place_forget()
        menu_visible[0] = False
        root.unbind("<Button-1>")

def abrir_perfil():
    if menu_visible[0]:
        toggle_menu()
    import subprocess
    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "vPerfil.py")])

def abrir_configuracion():
    toggle_menu()
    import subprocess
    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "Menu.py")])

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

entry_busqueda = tb.Entry(frame_top, width=35, font=("Helvetica", 11))
entry_busqueda.place(x=70, y=13, height=30)

def buscar(texto):
    refrescar_tareas(filtro=texto.strip().lower())

#boton buscar
tb.Button(frame_top, text="🔍", bootstyle="secondary", command=lambda: buscar(entry_busqueda.get())).place(x=350, y=10)
entry_busqueda.bind("<Return>", lambda e: buscar(entry_busqueda.get()))

#boton calendario
tb.Button(frame_top, text="📅", bootstyle="info", width=3, command=lambda: abrir_calendario()).place(x=990, y=10)

#boton perfil
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

# PANEL DERECHO -- Tareas publicas
def ver_tarea_publica(tarea):
    ventana = tb.Toplevel(root)
    ventana.title("Tarea pública")
    ventana.geometry("420x460")
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

    colores = {"Bajo": "success", "Moderado": "info", "Alto": "warning", "Muy alto": "danger"}
    estilo = colores.get(tarea.get("estres", "Bajo"), "secondary")
    tb.Label(frame_info, text=f"⏱ Horas/día: {tarea.get('horas', '-')}", font=("Helvetica", 11)).pack(side="left", padx=(0, 20))
    tb.Label(frame_info, text=f"😰 Estrés: {tarea.get('estres', '-')}", font=("Helvetica", 11), bootstyle=estilo).pack(side="left")

    tb.Separator(frame).pack(fill="x", pady=8)

    # Pedir código para unirse — NO muestra el código de la tarea
    tb.Label(frame, text="Ingresa el código para unirte:", font=("Helvetica", 10)).pack(anchor="w")
    entry_codigo_unirse = tb.Entry(frame, width=20, font=("Helvetica", 11))
    entry_codigo_unirse.pack(anchor="w", pady=(4, 16), ipady=4)

    def unirse():
        codigo_ingresado = entry_codigo_unirse.get().strip().upper()
        if not codigo_ingresado:
            messagebox.showwarning("Vacío", "Ingresa el código de acceso.", parent=ventana)
            return
        token = sesion.obtener()
        respuesta = UsuarioService.unirse_tarea(codigo_ingresado, token)
        if respuesta.get("task_id"):
            messagebox.showinfo("¡Unido!", f"Te uniste a '{tarea['nombre']}' correctamente.")
            ventana.destroy()
            cargar_tareas_api()
            refrescar_tareas()
            actualizar_barra_estres()
        else:
            error = respuesta.get("message", "Código incorrecto o tarea no encontrada.")
            messagebox.showerror("Error", error, parent=ventana)

    frame_botones = tb.Frame(frame)
    frame_botones.pack(fill="x")
    tb.Button(frame_botones, text="Unirse", bootstyle="success", width=16, command=unirse).pack(side="left", padx=(0, 8))
    tb.Button(frame_botones, text="Cerrar", bootstyle="secondary", width=10, command=ventana.destroy).pack(side="left")
    
def abrir_calendario():
    ventana = tb.Toplevel(root)
    ventana.title("Calendario de carga de horas")
    ventana.geometry("640x580")
    ventana.resizable(False, False)
    ventana.place_window_center()
        
    frame = tb.Frame(ventana, padding=20)
    frame.pack(fill="both", expand=True)
        
    hoy = date.today()
    mes_actual = [hoy.month]
    anio_actual = [hoy.year]
        
    tb.Label(frame, text="📅 Calendario de horas asignadas", font=("Helvetica", 14, "bold"), bootstyle="info").pack(pady=(0, 8))
        
    lbl_mes = tb.Label(frame, text="", font=("Helvetica", 12, "bold"))
    lbl_mes.pack(pady=(0, 12))

    frame_dias = tb.Frame(frame)
    frame_dias.pack()

    frame_leyenda = tb.Frame(frame)
    frame_leyenda.pack(pady=(12, 0))

    tb.Label(frame_leyenda, text="🟩 Normal (≤16h)", font=("Helvetica", 9), bootstyle="success").pack(side="left", padx=8)
    tb.Label(frame_leyenda, text="🟥 Sueño en peligro (>16h)", font=("Helvetica", 9), bootstyle="danger").pack(side="left", padx=8)
    tb.Label(frame_leyenda, text="⬜ Sin tareas", font=("Helvetica", 9), bootstyle="secondary").pack(side="left", padx=8)

    def dibujar_mes():
        for widget in frame_dias.winfo_children():
            widget.destroy()
            
        lbl_mes.config(text=f"{cal_module.month_name[mes_actual[0]].capitalize()} {anio_actual[0]}")

        horas_por_dia = calcular_horas_por_dia()

        dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        for i, d in enumerate(dias_semana):
            tb.Label(
                frame_dias, 
                text=d, 
                font=("Helvetica", 10, "bold"), 
                width=6, 
                anchor="center"
                ).grid(row=0, column=i, padx=2, pady=2)

        cal_dias = cal_module.monthcalendar(anio_actual[0], mes_actual[0])

        for fila_idx, semana in enumerate(cal_dias, start=1):
            for col_idx, dia in enumerate(semana):
                if dia == 0:
                    continue

                fecha = date(anio_actual[0], mes_actual[0], dia)
                horas = horas_por_dia.get(fecha, 0)

                if horas > 16:
                    estilo = "danger"
                elif horas > 0:
                    estilo = "success"
                else:
                    estilo = "secondary-outline"

                texto = f"{dia}"
                if horas > 0:
                    texto += f"\n{horas:.1f}h"

                tb.Button(
                    frame_dias,
                    text=texto,
                    bootstyle=estilo,
                    width=6,
                    command=lambda f=fecha, h=horas: ver_detalle_dia(f, h)
                ).grid(row=fila_idx, column=col_idx, padx=2, pady=2)

    def ver_detalle_dia(fecha, horas):
        if horas > 16:
            messagebox.showwarning(
                "⚠️ Sueño en peligro",
                f"El {fecha.strftime('%d/%m/%Y')} tienes {horas:.1f} horas de tareas asignadas.\n\n"
                f"Esto supera las 16 horas recomendadas y deja menos de 8 horas para dormir."
            )
        elif horas > 0:
            messagebox.showinfo("Día con tareas", f"El {fecha.strftime('%d/%m/%Y')} tienes {horas:.1f} horas de tareas asignadas.")
        else:
            messagebox.showinfo("Sin tareas", f"El {fecha.strftime('%d/%m/%Y')} no tienes tareas asignadas.")

    def mes_anterior():
        if mes_actual[0] == 1:
            mes_actual[0] = 12
            anio_actual[0] -= 1
        else:
            mes_actual[0] -= 1
        dibujar_mes()

    def mes_siguiente():
        if mes_actual[0] == 12:
            mes_actual[0] = 1
            anio_actual[0] += 1
        else:
            mes_actual[0] += 1
        dibujar_mes()

    frame_nav = tb.Frame(frame)
    frame_nav.pack(pady=(8, 0))
    tb.Button(frame_nav, text="← Mes anterior", bootstyle="secondary-outline", command=mes_anterior).pack(side="left", padx=4)
    tb.Button(frame_nav, text="Mes siguiente →", bootstyle="secondary-outline", command=mes_siguiente).pack(side="left", padx=4)

    dibujar_mes()


#Mostrar resultados de buscar las tareas publicas por nombre
def mostrar_resultados_publicos(resultados):
    ventana = tb.Toplevel(root)
    ventana.title("Resultados")
    ventana.geometry("420x400")
    ventana.resizable(False, False)
    ventana.place_window_center()

    frame = tb.Frame(ventana, padding=20)
    frame.pack(fill="both", expand=True)

    tb.Label(frame, text="Tareas encontradas", font=("Helvetica", 14, "bold"), bootstyle="info").pack(pady=(0, 16))

    for t in resultados:
        frame_t = tb.Frame(frame, bootstyle="dark", padding=10)
        frame_t.pack(fill="x", pady=6)
        tb.Label(frame_t, text=f"🌐 {t['nombre']}", font=("Helvetica", 12, "bold")).pack(anchor="w")
        tb.Label(frame_t, text=f"😰 Estrés: {t.get('estres', '-')}  ⏱ {t.get('horas', '-')}h/día", font=("Helvetica", 10), bootstyle="secondary").pack(anchor="w", pady=(2, 6))
        tb.Button(
            frame_t,
            text="Ver y unirse",
            bootstyle="info-outline",
            command=lambda t=t: [ventana.destroy(), ver_tarea_publica(t)]
        ).pack(anchor="e")

def buscar_tarea_publica():
    nombre = entry_codigo.get().strip().lower()
    if not nombre:
        messagebox.showwarning("Vacío", "Escribe el nombre de la tarea a buscar.")
        return
    
    token = sesion.obtener()
    respuesta = UsuarioService.buscar_tareas_publicas(nombre, token)
    print("RESPUESTA BUSQUEDA:", respuesta)

    if isinstance(respuesta, list) and respuesta:
        resultados = []
        for t in respuesta:
            resultados.append({
                "task_id": t.get("task_id"),
                "nombre": t.get("title", ""),
                "descripcion": t.get("description", ""),
                "horas": t.get("horasDia", 0),
                "estres": nivel_numerico_a_texto(t.get("stressLevel") or 0),
                "codigo": t.get("code") or ""
            })
        mostrar_resultados_publicos(resultados)
    else:
        messagebox.showerror("No encontrada", "No existe una tarea pública con ese nombre.")

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
        # Solo muestra el nombre, sin el código
        tb.Label(frame_pub, text=f"🌐 {t.get('nombre', 'Sin nombre')}", font=("Helvetica", 11), bootstyle="info").pack(side="left")
        tb.Button(
            frame_pub,
            text="Ver código",
            bootstyle="warning-outline",
            command=lambda t=t: messagebox.showinfo("Tu código", f"Código: {t['codigo']}\n\nCompártelo solo con quien quieras.")
        ).pack(side="right")


frame_buscar_pub = tb.Frame(frame_derecho)
frame_buscar_pub.pack(fill="x", pady=(0, 8))

entry_codigo = tb.Entry(frame_buscar_pub, width=14, font=("Helvetica", 11))
entry_codigo.pack(side="left", ipady=4)

tb.Button(frame_buscar_pub, text="Buscar", bootstyle="info", command=buscar_tarea_publica).pack(side="left", padx=(8, 0))

frame_lista_publica = tb.Frame(frame_derecho)
frame_lista_publica.pack(fill="both", expand=True)


# Formulario agregar/editar 
def agregar_tarea_ui(tarea_existente=None, indice=None):
    es_edicion = tarea_existente is not None

    ventana = tb.Toplevel(root)
    ventana.title("Editar tarea" if es_edicion else "Nueva tarea")
    ventana.geometry("400x800")
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

    # Fechas 
    frame_fechas = tb.Frame(frame)
    frame_fechas.pack(fill="x", pady=(0, 10))
        
    frame_fecha_inicio = tb.Frame(frame_fechas)
    frame_fecha_inicio.pack(side="left", padx=(0, 10))
    tb.Label(frame_fecha_inicio, text="Fecha de inicio", font=("Helvetica", 11)).pack(anchor="w")
    entry_fecha_inicio = tb.DateEntry(frame_fecha_inicio, width=12, dateformat="%Y-%m-%d")
    entry_fecha_inicio.pack(pady=(4, 0))
        
    frame_fecha_fin = tb.Frame(frame_fechas)
    frame_fecha_fin.pack(side="left")
    tb.Label(frame_fecha_fin, text="Fecha de fin", font=("Helvetica", 11)).pack(anchor="w")
    entry_fecha_fin = tb.DateEntry(frame_fecha_fin, width=12, dateformat="%Y-%m-%d")
    entry_fecha_fin.pack(pady=(4, 0))
        
    if es_edicion:
        if tarea_existente.get("startDate"):
            entry_fecha_inicio.entry.delete(0, "end")
            entry_fecha_inicio.entry.insert(0, str(tarea_existente["startDate"])[:10])
        if tarea_existente.get("finishDate"):
            entry_fecha_fin.entry.delete(0, "end")
            entry_fecha_fin.entry.insert(0, str(tarea_existente["finishDate"])[:10])

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
        fecha_inicio = entry_fecha_inicio.entry.get().strip()
        fecha_fin = entry_fecha_fin.entry.get().strip()
        
        if not nombre:
            messagebox.showwarning("Campo vacío", "Escribe el nombre de la tarea.", parent=ventana)
            return

        if not fecha_inicio or not fecha_fin:
            messagebox.showwarning("Campo vacío", "Selecciona las fechas de inicio y fin.", parent=ventana)
            return

        if date.fromisoformat(fecha_inicio) > date.fromisoformat(fecha_fin):
            messagebox.showwarning("Fechas inválidas", "La fecha de fin debe ser igual o posterior a la de inicio.", parent=ventana)
            return

        token = sesion.obtener()
        hoy = str(date.today())

        if es_edicion:
            es_dueno = tarea_existente.get("esDueno", True)

            if es_dueno:
                respuesta = UsuarioService.actualizar_tarea(tarea_existente["task_id"], {
                    "title": nombre,
                    "description": desc,
                    "stressLevel": nivel_texto_a_numerico(nivel),
                    "public": publica,
                    "code": codigo
                }, token)
            else:
                # Miembro: solo puede modificar su propio nivel de estrés
                respuesta = UsuarioService.actualizar_tarea(tarea_existente["task_id"], {
                    "stressLevel": nivel_texto_a_numerico(nivel)
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
                "startDate": fecha_inicio,
                "finishDate": fecha_fin,
                "horasDia": float(horas),
                "public": publica,
                "code": codigo
            }, token)
            if respuesta.get("task_id"):
                if publica and codigo:
                    messagebox.showinfo("Tarea pública", f"Código de acceso: {codigo}\n\nCompártelo con quien quieras.", parent=ventana)
            else:
                messagebox.showerror("Error", respuesta.get("message", "No se pudo crear la tarea."), parent=ventana)
                return

        # Verificar alerta de horario
        task_id_actual = tarea_existente.get("task_id") if es_edicion else None
        dias_peligro = verificar_alerta_horario(fecha_inicio, fecha_fin, horas, excluir_task_id=task_id_actual)

        if dias_peligro:
            dias_texto = "\n".join([f"  • {d.strftime('%d/%m/%Y')}: {h:.1f}h totales" for d, h in dias_peligro])
            messagebox.showwarning(
                "⚠️ Horario en peligro",
                f"Con esta tarea, los siguientes días superan las 16 horas:\n\n{dias_texto}\n\n"
                f"Esto deja menos de 8 horas para dormir. Considera ajustar horas o fechas.",
                parent=ventana
            )

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
root.after(1500, mostrar_mensaje_positivo)
root.mainloop()