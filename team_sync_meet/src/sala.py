import platform
from colorama import Fore, Style, init

# Iniciar colorama
init(autoreset=True)

# Sonido en Windows
if platform.system() == "Windows":
    import winsound


class SimpleUsuario:
    def __init__(self, nombre):
        self.nombre = nombre

    def enviar(self, mensaje):
        print(mensaje)


class Sala:
    def __init__(self, nombre):
        self.nombre = nombre
        self.usuarios = []

    def agregar_usuario(self, usuario):
        self.usuarios.append(usuario)
        self.notificar(f"{usuario.nombre} se ha unido a la sala.", destinatarios=[usuario])
        for u in self.usuarios:
            if u != usuario:
                u.enviar(f"{Fore.RED}[Sistema] {usuario.nombre} se ha unido a la sala.{Style.RESET_ALL}")
        self.reproducir_sonido()

    def quitar_usuario(self, nombre):
        for usuario in self.usuarios:
            if usuario.nombre == nombre:
                self.usuarios.remove(usuario)
                self.notificar(f"{usuario.nombre} ha salido de la sala.")
                return
        print(f"[Advertencia] No se encontró un usuario con el nombre '{nombre}'.")

    def mostrar_usuarios(self):
        if not self.usuarios:
            print("[Sala vacía]")
        else:
            print("[Usuarios en la sala]:")
            for usuario in self.usuarios:
                print(f"- {usuario.nombre}")

    def enviar_mensaje(self, remitente, mensaje):
        texto = f"{Fore.CYAN}[{remitente.nombre}] {mensaje}{Style.RESET_ALL}"
        for usuario in self.usuarios:
            usuario.enviar(texto)
        self.reproducir_sonido()

    def notificar(self, mensaje, destinatarios=None):
        texto = f"{Fore.RED}[Sistema] {mensaje}{Style.RESET_ALL}"
        if destinatarios is None:
            destinatarios = self.usuarios
        for usuario in destinatarios:
            usuario.enviar(texto)

    def reproducir_sonido(self):
        if platform.system() == "Windows":
            winsound.MessageBeep()

    def ejecutar(self):
        print(f"=== Sala '{self.nombre}' iniciada ===")
        print(f"[Usuarios iniciales]: {', '.join([u.nombre for u in self.usuarios])}")
        while True:
            comando = input("Comando ('salir [nombre]' o 'terminar'): ").strip()

            if comando.startswith("salir "):
                nombre = comando.split(" ", 1)[1]
                self.quitar_usuario(nombre)
            elif comando == "terminar":
                print("Finalizando la sala...")
                break
            else:
                print("[Error] Comando no reconocido.")
