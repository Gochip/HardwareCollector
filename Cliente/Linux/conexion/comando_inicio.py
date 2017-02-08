from conexion.comando import Comando
import json

class ComandoInicio(Comando):
    
    def __init__(self):
        super().__init__("inicio")
        self.datos = None

    def set_datos(self, datos):
        self.datos = datos
    
    def get_datos():
        return self.datos
    
    class Datos:
        def __init__(self):
            self.id = ""

        def set_id(self, solicitud):
            self.id = solicitud

        def get_id(self):
            return self.id

    def serialize(self):
        datos = self.datos.__dict__
        self.datos = datos
        return json.dumps(self.__dict__)
