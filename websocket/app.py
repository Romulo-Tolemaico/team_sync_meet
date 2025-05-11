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
    async_mode='gevent',
    logger=True,
    engineio_logger=False,
    ping_timeout=30,  # Aumenta el tiempo de espera
    ping_interval=10  # Verifica la conexión con más frecuencia
)

# Almacén de usuarios y mensajes
active_users = {}
chat_history = []

class ConsoleDesign:
    """Estilos para la consola del servidor"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @classmethod
    def print_header(cls, message):
        print(f"\n{cls.BOLD}{cls.BLUE}=== {message} ==={cls.END}")

    @classmethod
    def print_event(cls, message, event_type="info"):
        colors = {
            "info": cls.BLUE,
            "success": cls.GREEN,
            "warning": cls.YELLOW,
            "error": cls.RED,
            "message": cls.HEADER
        }
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{colors[event_type]}[{timestamp}] {message}{cls.END}")

def broadcast_system_message(message, event_type="info"):
    """Envía mensajes del sistema a todos los clientes"""
    emit('system_message', {
        'content': message,
        'type': event_type,
        'time': datetime.now().strftime('%H:%M:%S')
    }, broadcast=True)

@socketio.on('connect')
def handle_connect():
    ConsoleDesign.print_event(f"Nueva conexión desde {request.remote_addr}", "info")
    emit('request_username')

@socketio.on('set_username')
def handle_set_username(data):
    client_id = request.sid
    username = data['username'].strip() or f"Usuario-{client_id[:4]}"
    
    active_users[client_id] = username
    ConsoleDesign.print_event(f"Usuario registrado: {username}", "success")
    broadcast_system_message(f"✨ {username} se ha unido al chat", "success")
    
    emit('chat_history', {
        'history': chat_history[-20:],  
        'users': list(active_users.values())
    })
    
    emit('update_users', list(active_users.values()), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    if client_id in active_users:
        username = active_users.pop(client_id)
        ConsoleDesign.print_event(f"Usuario desconectado: {username}", "warning")
        broadcast_system_message(f"👋 {username} ha abandonado el chat", "warning")
        emit('update_users', list(active_users.values()), broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    client_id = request.sid
    if client_id in active_users:
        username = active_users[client_id]
        message = data['message'].strip()
        
        if message:
            message_data = {
                'username': username,
                'message': message,
                'time': datetime.now().strftime('%H:%M:%S')
            }
            chat_history.append(message_data)
            ConsoleDesign.print_event(f"{username}: {message}", "message")
            emit('new_message', message_data, broadcast=True)

if __name__ == '__main__':
    ConsoleDesign.print_header("SERVIDOR DE CHAT ELEGANTE")
    print(f"{ConsoleDesign.GREEN}• Modo: WebSocket puro")
    print(f"• Sala única con historial de mensajes")
    print(f"• Notificaciones elegantes de conexión/desconexión")
    print(f"• Registro detallado en consola{ConsoleDesign.END}\n")
    
    # Detectar si estamos en Render o Local
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    
    socketio.run(app, host="0.0.0.0", port=port, debug=debug_mode)
