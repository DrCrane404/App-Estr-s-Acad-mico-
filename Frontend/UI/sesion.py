token = None
usuario = None

def guardar (token_recibido):
    global token, usuario
    token = token_recibido

def cerrar():
    global token, usuario
    token = None
    usuario = None

def borrar():
    global token, usuario
    token = None
    usuario = None

def obtener():
    global token
    return token