from flask import Flask, request
from flask_socketio import SocketIO, emit
from datetime import datetime
import time, os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    transports=['websocket'],
    async_mode='eventlet',
    logger=True,
    engineio_logger=False
)

# Almacén de usuarios y mensajes
usuarios_activos = {}
historial_chat = []

class DisenoConsola:
    """Estilos para la consola del servidor"""
    ENCABEZADO = '\033[95m'
    AZUL = '\033[94m'
    VERDE = '\033[92m'
    AMARILLO = '\033[93m'
    ROJO = '\033[91m'
    NEGRITA = '\033[1m'
    SUBRAYADO = '\033[4m'
    FIN = '\033[0m'

    @classmethod
    def imprimir_encabezado(cls, mensaje):
        print(f"\n{cls.NEGRITA}{cls.AZUL}=== {mensaje} ==={cls.FIN}")

    @classmethod
    def imprimir_evento(cls, mensaje, tipo_evento="info"):
        colores = {
            "info": cls.AZUL,
            "exito": cls.VERDE,
            "advertencia": cls.AMARILLO,
            "error": cls.ROJO,
            "mensaje": cls.ENCABEZADO
        }
        marca_tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{colores.get(tipo_evento, cls.AZUL)}[{marca_tiempo}] {mensaje}{cls.FIN}")

@app.route('/')
def index():
    return "Servidor de Chat Activo"

@socketio.on('connect')
def manejar_conexion():
    DisenoConsola.imprimir_evento(f"Nueva conexión desde {request.remote_addr}", "info")
    emit('solicitar_nombre_usuario')

@socketio.on('set_username')
def manejar_nombre_usuario(data):
    id_cliente = request.sid
    nombre_usuario = data['username'].strip() or f"Usuario-{id_cliente[:4]}"
    usuarios_activos[id_cliente] = nombre_usuario
    DisenoConsola.imprimir_evento(f"Usuario registrado: {nombre_usuario}", "exito")
    emit('historial_chat', {'historial': historial_chat[-20:], 'usuarios': list(usuarios_activos.values())})
    emit('actualizar_usuarios', list(usuarios_activos.values()), broadcast=True)

@socketio.on('disconnect')
def manejar_desconexion():
    id_cliente = request.sid
    if id_cliente in usuarios_activos:
        nombre_usuario = usuarios_activos.pop(id_cliente)
        DisenoConsola.imprimir_evento(f"Usuario desconectado: {nombre_usuario}", "advertencia")
        emit('actualizar_usuarios', list(usuarios_activos.values()), broadcast=True)

@socketio.on('send_message')
def manejar_mensaje(data):
    id_cliente = request.sid
    if id_cliente in usuarios_activos:
        nombre_usuario = usuarios_activos[id_cliente]
        mensaje = data['message'].strip()
        if mensaje:
            datos_mensaje = {'username': nombre_usuario, 'message': mensaje, 'time': datetime.now().strftime('%H:%M:%S')}
            historial_chat.append(datos_mensaje)
            DisenoConsola.imprimir_evento(f"{nombre_usuario}: {mensaje}", "mensaje")
            emit('new_message', datos_mensaje, broadcast=True)

if __name__ == '__main__':
    DisenoConsola.imprimir_encabezado("SERVIDOR DE CHAT ELEGANTE")
    puerto = int(os.environ.get("PORT", 5000))
    modo_debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    socketio.run(app, host="0.0.0.0", port=puerto, debug=modo_debug)
