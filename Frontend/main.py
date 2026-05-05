import subprocess
import sys
import os
if __name__ == "__main__":
    ruta_login = os.path.join(os.path.dirname(__file__), "UI", "Login.py")
    subprocess.Popen([sys.executable, ruta_login])