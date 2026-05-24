# sesion.py
import tempfile, os

_ruta = os.path.join(tempfile.gettempdir(), "estres_sesion.txt")

def guardar(token_recibido):
    with open(_ruta, "w") as f:
        f.write(token_recibido)

def obtener():
    try:
        with open(_ruta, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def cerrar():
    if os.path.exists(_ruta):
        os.remove(_ruta)