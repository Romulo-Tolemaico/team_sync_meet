import socketio
from datetime import datetime
import sys

class ClientDesign:
    """Diseño elegante para el cliente"""
    COLORS = {
        'system': '\033[94m',      # Azul para mensajes del sistema
        'user_joined': '\033[92m', # Verde para nuevos usuarios
        'user_left': '\033[91m',   # Rojo para salidas
        'message': '\033[95m',     # Morado para mensajes normales
        'input': '\033[93m',       # Amarillo para entrada
        'info': '\033[96m',        # Cyan para información
        'reset': '\033[0m'
    }

    @classmethod
    def print_message(cls, message_type, sender, content, timestamp=None):
        timestamp = timestamp or datetime.now().strftime('%H:%M:%S')
        color = cls.COLORS.get(message_type, cls.COLORS['message'])
        
        if message_type == 'system':
            print(f"\n{color}>>> {content} ({timestamp}){cls.COLORS['reset']}")
        elif message_type in ('user_joined', 'user_left'):
            icon = "↑↑" if message_type == 'user_joined' else "↓↓"
            print(f"\n{color}{icon} {content} ({timestamp}){cls.COLORS['reset']}")
        else:
            print(f"\n{color}[{timestamp}] {sender}: {content}{cls.COLORS['reset']}")

class ChatClient:
    def __init__(self):
        self.sio = socketio.Client()
        self.username = None
        self.setup_handlers()
        
    def setup_handlers(self):
        @self.sio.event
        def connect():
            ClientDesign.print_message('system', None, "Conectado al servidor")
            self.username = input(f"{ClientDesign.COLORS['input']}Ingresa tu nombre: {ClientDesign.COLORS['reset']}")
            self.sio.emit('set_username', {'username': self.username})
            
        @self.sio.on('chat_history')
        def handle_history(data):
            ClientDesign.print_message('system', None, f"Historial del chat ({len(data['history'])} mensajes)")
            for msg in data['history']:
                ClientDesign.print_message('message', msg['username'], msg['message'], msg['time'])
            
            ClientDesign.print_message('system', None, f"Usuarios activos: {', '.join(data['users'])}")
            self.print_prompt()
            
        @self.sio.on('new_message')
        def handle_new_message(data):
            ClientDesign.print_message('message', data['username'], data['message'], data['time'])
            self.print_prompt()
            
        @self.sio.on('system_message')
        def handle_system(data):
            if data['type'] == 'success':
                ClientDesign.print_message('user_joined', None, data['content'], data['time'])
            else:
                ClientDesign.print_message('user_left', None, data['content'], data['time'])
            self.print_prompt()
            
        @self.sio.on('update_users')
        def handle_users_update(users):
            ClientDesign.print_message('info', None, f"Usuarios conectados: {len(users)}")
            self.print_prompt()
            
    def print_prompt(self):
        print(f"{ClientDesign.COLORS['input']}[{self.username}]> {ClientDesign.COLORS['reset']}", end='', flush=True)
        
    def start(self):
        try:
            self.sio.connect(
                'https://team-sync-meet.onrender.com',
                transports=['websocket'],
                socketio_path='/socket.io'
            )
            
            while True:
                self.print_prompt()
                message = input().strip()
                
                if message.lower() == '/salir':
                    break
                    
                if message:
                    self.sio.emit('send_message', {'message': message})
                    
        except KeyboardInterrupt:
            pass
        except Exception as e:
            ClientDesign.print_message('system', None, f"Error: {str(e)}")
        finally:
            if self.sio.connected:
                self.sio.disconnect()
            ClientDesign.print_message('system', None, "Desconectado del chat")

if __name__ == '__main__':
    print("\n=== CLIENTE DE CHAT ELEGANTE ===")
    client = ChatClient()
    client.start()