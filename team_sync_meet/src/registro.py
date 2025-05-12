import socketio
import random

class ChatClient:
    def __init__(self):
        self.sio = socketio.Client()
        self.username = None
        self.setup_handlers()

    def generar_nombre_automatico(self):
        return f"Usuario_{random.randint(100, 999)}"

    def solicitar_nombre_usuario(self):
        nombre = input(f"{ClientDesign.COLORS['input']}Ingresa tu nombre (ENTER para uno automático): {ClientDesign.COLORS['reset']}").strip()
        return nombre if nombre else self.generar_nombre_automatico()

    def setup_handlers(self):
        @self.sio.event
        def connect():
            ClientDesign.print_message('system', None, "Conectado al servidor")
            self.username = self.solicitar_nombre_usuario()
            ClientDesign.print_message('system', None, f"👤 {self.username} ingreso al chat")
            self.sio.emit('set_username', {'username': self.username})