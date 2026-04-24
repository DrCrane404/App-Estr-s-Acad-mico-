import requests

BASE_URL="http://localhost:3000"

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
def register(name,username,email,password,r_question, r_aswer):
    return post("/auth/register",{
        "name":name,
        "username":username,
        "email":email,
        "password":password,
        "r_question":r_question,
        "r_answer":r_aswer
    })