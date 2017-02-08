from conexion.comando import Comando
import json

class ComandoMaquinaNueva(Comando):
    
    def __init__(self):
        super().__init__("maquina_nueva")
