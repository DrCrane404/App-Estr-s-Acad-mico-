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
        response = requests.get(f"{BASE_URL}{endpoint}", headers={"Authorization": f"Bearer {token}"})
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

# Update llama a UsuarioService.get_by_email() y UsuarioService.update()
def get_by_email(email):
    return post("/auth/user", {"email": email})

def update(id, name, username, password):
    return post(f"/auth/update/{id}", {
        "name": name,
        "username": username,
        "password": password
    })

#----------------------TAREAS-----------------------------
def post_auth(endpoint, data, token):
    try:
        response = requests.post(
            f"{BASE_URL}{endpoint}",
            json=data,
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json()
    except Exception as e:
        return {"Success": False, "error": str(e)}

# Tareas
def crear_tarea(data: dict, token: str) -> dict:
    return post_auth("/task", data, token)

def obtener_mis_tareas(token: str) -> dict:
    return get_auth("/task/own", token)

def obtener_tarea(task_id: int, token: str) -> dict:
    return get_auth(f"/task/{task_id}", token)

def actualizar_tarea(task_id: int, data: dict, token: str) -> dict:
    return patch_auth(f"/task/{task_id}", data, token)

def completar_tarea(task_id: int, token: str) -> dict:
    return patch_auth(f"/task/complete/{task_id}", {}, token)

def eliminar_tarea(task_id: int, token: str) -> dict:
    return delete_auth(f"/task/{task_id}", token)

def obtener_tareas_publicas(token: str) -> dict:
    return get_auth("/task/public", token)

def unirse_tarea(code: str, token: str) -> dict:
    return post_auth("/task/join", {"code": code}, token)

#-----------------Cuestionario y nivel de estres -----------------------------
def guardar_cuestionario_inicial(puntuacion, categoria, puntaje_total, puntaje_maximo, token):
    return post_auth("/stress-level/inicial", {
        "puntuacion": puntuacion,
        "categoria": categoria,
        "puntajeTotal": puntaje_total,
        "puntajeMaximo": puntaje_maximo
    }, token)

def obtener_nivel_estres(token):
    return get_auth("/stress-level/nivel", token)