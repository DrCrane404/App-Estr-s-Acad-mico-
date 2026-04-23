import requests

BASE_URL="Link de render"

def post(endpoint, data):
    return requests.post(f"{BASE_URL}{endpoint}",json=data).json()
def login(email, password):
    return post("/auth/login",{
        "email":email,
        "password": password
    })
def register(nombre,email,password):
    return post("auth/register",{
        "nombre":nombre,
        "email":email,
        "password":password
    })