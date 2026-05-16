import requests

BASE_URL="http://localhost:3000"

#EndPoints
def post(endpoint, data):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}",json=data)
        return response.json()
    except Exception as e:
        return {"Success": False, "error": str(e)}
    
def get_auth(endpoint, token):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers={"Authorization": f"Bearer{token}"})
        return response.json()
    except Exception as e:
        return{
            "Success":False, 
            "error": str(e)
        }
def patch_auth(endpoint, data, token):
    try:
        response = requests.patch(
            f"{BASE_URL}{endpoint}",
            json=data,
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json()
    except Exception as e:
        return {"Success": False, "error": str(e)}

def delete_auth(endpoint, token):
    try:
        response = requests.delete(
            f"{BASE_URL}{endpoint}",
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json()
    except Exception as e:
        return {"Success": False, "error": str(e)}
    
#Modulo de Usuarios
def login(email, password):
    return post("/auth/login",{
        "email":email,
        "password": password
    })

def register(name,username,email,password):
    return post("/auth/register",{
        "name":name,
        "username":username,
        "email":email,
        "password":password,
    })

def ver_perfil(token: str) -> dict:
    return get_auth("/auth/profile", token)

def actualizar_perfil(datos: dict, token: str) -> dict:
    # datos puede incluir: name, username, email, password
    return patch_auth("/auth/profile", datos, token)

def eliminar_cuenta(token: str) -> dict:
    return delete_auth("/auth/profile", token)

# Recuperacion de contraseña
def solicitar_codigo_recuperacion(email: str) -> dict:
    #Llama al backend para que genere y envíe el código al correo.
    return post("/auth/forgot-password", {
        "email": email
    })

def cambiar_contraseña(email:str, codigo: str, nueva_contraseña: str) -> dict:
    """Valida el código y actualiza la contraseña en el backend."""
    return post("/auth/reset-password", {
        "email":email,
        "code":codigo,
        "newPassword": nueva_contraseña
    })

#Modulo de tareas
def crear_Tarea(title, description, stressLevel, tType, startDate, finishDate, token: str):
    try:
        response = requests.post(
            f"{BASE_URL}/task",
            json={
                "title": title,
                "description": description,
                "tType": tType,
                "stressLevel": stressLevel,
                "startDate": startDate,
                "finishDate": finishDate,
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json()
    except Exception as e:
        return {"Success": False, "error": str(e)}

def obtener_todas_tareas(token: str) -> dict:
    return get_auth("/task", token)

def obtener_mis_tareas(token: str) -> dict:
    return get_auth("/task/own", token)

def obtener_tareas_usuario(user_id: int, token: str) -> dict:
    return get_auth(f"/task/user/{user_id}", token)

def obtener_tarea(task_id: int, token: str) -> dict:
    return get_auth(f"/task/{task_id}", token)

def actualizar_tarea(task_id: int, datos: dict, token: str) -> dict:
    return patch_auth(f"/task/{task_id}", datos, token)

def completar_tarea(task_id: int, token: str) -> dict:
    return patch_auth(f"/task/complete/{task_id}", {}, token)

def eliminar_tarea(task_id: int, token: str) -> dict:
    return delete_auth(f"/task/{task_id}", token)