import platform
from colorama import Fore, Style, init

# Iniciar colorama
init(autoreset=True)

# Sonido en Windows
if platform.system() == "Windows":
    import winsound

class Notificaciones:
    @staticmethod
    def enviar_mensaje(texto, destinatarios):
        for usuario in destinatarios:
            usuario.enviar(texto)

    @staticmethod
    def notificar(mensaje, destinatarios=None):
        texto = f"{Fore.RED}[Sistema] {mensaje}{Style.RESET_ALL}"
        if destinatarios is not None:
            Notificaciones.enviar_mensaje(texto, destinatarios)

    @staticmethod
    def reproducir_sonido():
        if platform.system() == "Windows":
            winsound.MessageBeep()