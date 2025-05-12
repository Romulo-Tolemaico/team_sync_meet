from flask import Flask, request
from flask_socketio import SocketIO, emit
from datetime import datetime
import time, os

aplicacion = Flask(__name__)
aplicacion.config['CLAVE_SECRETA'] = 'tu_clave_secreta_aqui'

socketio = SocketIO(
    aplicacion,
    origenes_permitidos_cors="*",
    transportes=['websocket'],
    modo_asincrono='eventlet',
    registrador=True,
    registrador_engineio=False
)

# Almacenamiento de usuarios y mensajes
usuarios_activos = {}
historial_chat = []

class DisenioConsola:
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
            "success": cls.VERDE,
            "warning": cls.AMARILLO,
            "error": cls.ROJO,
            "message": cls.ENCABEZADO
        }
        marca_tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{colores[tipo_evento]}[{marca_tiempo}] {mensaje}{cls.FIN}")

def difundir_mensaje_sistema(mensaje, tipo_evento="info"):
    """Envía mensajes del sistema a todos los clientes"""
    emit('mensaje_sistema', {
        'contenido': mensaje,
        'tipo': tipo_evento,
        'hora': datetime.now().strftime('%H:%M:%S')
    }, broadcast=True)

@socketio.on('conectar')
def manejar_conexion():
    DisenioConsola.imprimir_evento(f"Nueva conexión desde {request.remote_addr}", "info")
    emit('solicitar_usuario')

@socketio.on('establecer_usuario')
def manejar_establecer_usuario(datos):
    id_cliente = request.sid
    usuario = datos['usuario'].strip() or f"Usuario-{id_cliente[:4]}"
    
    usuarios_activos[id_cliente] = usuario
    DisenioConsola.imprimir_evento(f"Usuario registrado: {usuario}", "success")
    difundir_mensaje_sistema(f"✨ {usuario} se ha unido al chat", "success")
    
    emit('historial_chat', {
        'historial': historial_chat[-20:],  
        'usuarios': list(usuarios_activos.values())
    })
    
    emit('actualizar_usuarios', list(usuarios_activos.values()), broadcast=True)

@socketio.on('desconectar')
def manejar_desconexion():
    id_cliente = request.sid
    if id_cliente in usuarios_activos:
        usuario = usuarios_activos.pop(id_cliente)
        DisenioConsola.imprimir_evento(f"Usuario desconectado: {usuario}", "warning")
        difundir_mensaje_sistema(f"👋 {usuario} ha abandonado el chat", "warning")
        emit('actualizar_usuarios', list(usuarios_activos.values()), broadcast=True)

@socketio.on('enviar_mensaje')
def manejar_mensaje(datos):
    id_cliente = request.sid
    if id_cliente in usuarios_activos:
        usuario = usuarios_activos[id_cliente]
        mensaje = datos['mensaje'].strip()
        
        if mensaje:
            datos_mensaje = {
                'usuario': usuario,
                'mensaje': mensaje,
                'hora': datetime.now().strftime('%H:%M:%S')
            }
            historial_chat.append(datos_mensaje)
            DisenioConsola.imprimir_evento(f"{usuario}: {mensaje}", "message")
            emit('nuevo_mensaje', datos_mensaje, broadcast=True)

if __name__ == '__main__':
    DisenioConsola.imprimir_encabezado("SERVIDOR DE CHAT ELEGANTE")
    print(f"{DisenioConsola.VERDE}• Modo: WebSocket puro")
    print(f"• Sala única con historial de mensajes")
    print(f"• Notificaciones elegantes de conexión/desconexión")
    print(f"• Registro detallado en consola{DisenioConsola.FIN}\n")
    
    # Detectar si estamos en Render o Local
    puerto = int(os.environ.get("PUERTO", 5000))
    modo_depuracion = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    
    socketio.run(aplicacion, host="0.0.0.0", port=puerto, debug=modo_depuracion)