import platform
from colorama import Fore, Style, init

# Iniciar colorama para colores en consola
init(autoreset=True)

# Importar winsound solo si es Windows
if platform.system() == "Windows":
    import winsound


class Sala:
    def __init__(self, nombre):
        self.nombre = nombre
        self.usuarios = []

    def agregar_usuario(self, usuario):
        self.usuarios.append(usuario)
        self.notificar(f"{usuario.nombre} se ha unido a la sala.")

    def quitar_usuario(self, usuario):
        if usuario in self.usuarios:
            self.usuarios.remove(usuario)
            self.notificar(f"{usuario.nombre} ha salido de la sala.")

    def enviar_mensaje(self, remitente, mensaje):
        texto = f"{Fore.CYAN}[{remitente.nombre}] {mensaje}{Style.RESET_ALL}"
        for usuario in self.usuarios:
            usuario.enviar(texto)
        self.reproducir_sonido()

    def notificar(self, mensaje):
        texto = f"{Fore.RED}[Sistema] {mensaje}{Style.RESET_ALL}"
        for usuario in self.usuarios:
            usuario.enviar(texto)
        self.reproducir_sonido()

    def reproducir_sonido(self):
        if platform.system() == "Windows":
            winsound.MessageBeep()


