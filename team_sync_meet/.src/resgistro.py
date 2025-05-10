import random
from colorama import init, Fore, Style

init(autoreset=True)

class Registro:
    def __init__(self):
        self.nombre = None

    def generarNombreAutomatico(self):
        return Fore.CYAN + f"Usuario_{random.randint(100, 999)}"

    def obtenerNombre(self):
        entrada = input(Fore.GREEN + "🟢 Ingresa tu nombre o pulsa ENTER para generar uno automático: ").strip()
        if not entrada:
            self.nombre = self.generarNombreAutomatico()
        else:
            self.nombre = entrada
        print(Fore.CYAN + f"\n👤 {self.nombre} ingresó al chat.")
        return self.nombre

if __name__ == "__main__":
    usuario = Registro()
    usuario.obtenerNombre()
