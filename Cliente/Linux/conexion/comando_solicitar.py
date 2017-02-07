import comando.Comando as Comando
import json

class ComandoSolicitar(Comando):
    
    datos = None
    
    def __init__(self):
        super().__init__("solicitar")

    class Datos:
        id_solicitud = ""
        informacion = [] #array de string
