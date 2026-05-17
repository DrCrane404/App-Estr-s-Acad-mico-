# L_tareas.py

# Lista de tareas en memoria
tareas = []

def L_tareas(accion, data=None, task_id=None):
    """
    Maneja la raylist de tareas en memoria.
    - accion: "crear", "listar", "actualizar", "eliminar"
    - data: información de la tarea (ejemplo: {"title": "Estudiar", "deadline": "2026-05-20"})
    - task_id: índice de la tarea (para actualizar o eliminar)
    """
    try:
        if accion == "crear":
            tareas.append(data)
            return {"Success": True, "tareas": tareas}
        elif accion == "listar":
            return {"Success": True, "tareas": tareas}
        elif accion == "actualizar":
            if task_id is not None and 0 <= task_id < len(tareas):
                tareas[task_id] = data
                return {"Success": True, "tareas": tareas}
            else:
                return {"Success": False, "error": "ID inválido"}
        elif accion == "eliminar":
            if task_id is not None and 0 <= task_id < len(tareas):
                tareas.pop(task_id)
                return {"Success": True, "tareas": tareas}
            else:
                return {"Success": False, "error": "ID inválido"}
        else:
            return {"Success": False, "error": "Acción no válida"}
    except Exception as e:
        return {"Success": False, "error": str(e)}
