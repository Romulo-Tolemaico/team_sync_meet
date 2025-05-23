# team_sync_meet
Resumen:
Esta funcionalidad permite la comunicación simultánea entre múltiples usuarios a través de WebSocket, logrando una conexión bidireccional persistente entre cliente y servidor. Se evita el uso de técnicas tradicionales como polling o long-polling para una mayor eficiencia y menor latencia. 

Objetivos:
- Permitir múltiples conexiones simultáneas.
- Transmitir mensajes en tiempo real a todos los usuarios conectados.
- Demostrar el uso práctico del protocolo WebSocket para comunicación persistente.

Alcance:
Incluye:
- Backend que gestiona conexiones WebSocket.
- Cliente web simple para enviar/recibir mensajes mediante consola
No incluye:
- Autenticación de usuarios.
- Persistencia de mensajes en base de datos.
Requisitos:
   Funcionales:
- Permitir que varios usuarios se conecten al servidor WebSocket.
- Difundir cada mensaje recibido a todos los usuarios conectados.
   No funcionales:
- Comunicación en tiempo real con latencia mínima.
- Código modular y mantenible.
Tecnologías:
- Python 3.9+
- Biblioteca websockets

Funcionalidades del sistema:
-Registro automático de usuarios
-Crear sala de chat
-Enviar y recibir mensajes
-Notificaciones de conexión/desconexión
-Salir de sala

instalacion y ejecucion:

1. Crear el entorno de trabajo
Elige una ubicación en tu disco y crea una nueva carpeta para el proyecto


Abre Visual Studio Code como administrador.


Desde Visual Studio Code, abre esa carpeta recién creada.

2. Crear el archivo de dependencias
Dentro de esa misma carpeta del proyecto, crea un archivo de texto.
****************************************************************************************
bidict==0.23.1
blinker==1.9.0
certifi==2025.4.26
charset-normalizer==3.4.2
click==8.2.0
colorama==0.4.6
dnspython==2.7.0
eventlet==0.39.1
Flask==3.1.0
Flask-SocketIO==5.3.4
greenlet==3.2.2
h11==0.16.0
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
python-engineio==4.3.4
python-socketio==5.7.2
requests==2.32.3
simple-websocket==1.1.0
urllib3==2.4.0
websocket-client==1.8.0
websockets==15.0.1
Werkzeug==3.1.3
wsproto==1.2.0
**************************************************************************************

Guarda el archivo con el nombre exacto: requirements.txt.


Este archivo permitirá instalar todas las dependencias necesarias más adelante.

3. Crear y activar un entorno virtual
En la terminal integrada de Visual Studio Code, ejecuta los siguientes comandos:
python -m venv venv
venv\Scripts\activate   


Esto crea una carpeta llamada venv que contiene un entorno virtual donde se instalarán las dependencias.

4. Instalar las dependencias
Con el entorno virtual activado, ejecuta en la terminal :
pip install -r requirements.txt

Esto instalará la biblioteca websockets y cualquier otra dependencia definida.

5. Crear el archivo principal del cliente
Fuera de la carpeta venv, es decir, en la raíz del proyecto, crea un archivo llamado: client.py 
en el ese archivo creado copia el siguiente codigo:

*****************************************************************************************
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



*****************************************************************************************


6. Ejecutar el cliente
Con todo listo, en la terminal (aún con el entorno virtual activado), ejecuta:
python cliente.py

7. Usar el sistema de chat
El programa te pedirá un nombre de usuario.


Luego, podrás escribir y enviar mensajes que se transmitirán en tiempo real a través de WebSocket.


Si hay otros usuarios conectados, podrás ver sus mensajes también.
