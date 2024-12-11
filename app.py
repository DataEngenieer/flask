from flask import Flask
from flask_socketio import SocketIO
import threading
import subprocess

app = Flask(__name__)
application = app
app.secret_key = '97110c78ae51a45af397b6534caef90ebb9b1dcb3380f008f90b23a5d1616bf1bc29098105da20fe'
#socketio = SocketIO(app)

"""
# Función para ejecutar el script de WebSocket
def run_websocket():
    subprocess.run(["python3", "websocket_token_1_tyt.py"])

# Iniciar el WebSocket al arrancar la app Flask
if __name__ == "__main__":
    thread = threading.Thread(target=run_websocket)
    thread.daemon = True
    thread.start()
    app.run(debug=True)
    
"""