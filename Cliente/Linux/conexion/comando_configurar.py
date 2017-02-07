import comando.Comando as Comando
import json

class ComandoConfigurar(Comando):
    
    datos = None
    
    def __init__(self):
        super().__init__("configurar")

    class Datos:
        configuracion = None #archivo configuración

