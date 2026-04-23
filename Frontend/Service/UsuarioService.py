import requests

BASE_URL="Link de render"

def post(endpoint, data):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}",json=data)
        return response.json()
    except Exception as e:
        return {"Success": False, "error": str(e)}

def login(email, password):
    return post("/auth/login",{
        "email":email,
        "password": password
    })
def register(nombre,email,password,pregunta,respuesta):
    return post("/auth/register",{
        "nombre":nombre,
        "email":email,
        "password":password,
        "pregunta_recuperacion":pregunta,
        "respuesta_recuperacion":respuesta
    })