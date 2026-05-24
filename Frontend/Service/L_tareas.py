# L_tareas.py
import UsuarioService
from UI import sesion

# Lista de tareas en memoria
tareas = []

def L_tareas(accion, data=None, task_id=None):

    token = sesion.obtener()

    if accion == "listar":
        respuesta = UsuarioService.obtener_mis_tareas(token)
        if isinstance(respuesta, list):
            tareas.clear()
            tareas.extend(respuesta)
        return tareas

    elif accion == "crear":
        UsuarioService.crear_Tarea(
            data["title"], data["description"], data["stressLevel"],
            data["tType"], data["startDate"], data["finishDate"], token
        )
        return L_tareas("listar")  # recarga desde el backend

    elif accion == "actualizar":
        UsuarioService.actualizar_tarea(task_id, data, token)
        return L_tareas("listar")

    elif accion == "eliminar":
        UsuarioService.eliminar_tarea(task_id, token)
        return L_tareas("listar")

    elif accion == "completar":
        UsuarioService.completar_tarea(task_id, token)
        return L_tareas("listar")
