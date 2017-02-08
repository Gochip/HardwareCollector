from conexion.comando import Comando
import json

class ComandoSolicitar(Comando):    
    
    def __init__(self):
        super().__init__("solicitar")
        self.datos = None

    def set_datos(self, datos):
        self.datos = datos

    def get_datos(self):
        return self.datos

    class Datos:
        def __init__(self):
            self.id_solicitud = ""
            self.informacion = [] #array de string

        def set_id_solicitar(self, solicitud):
            self.id_solicitud = solicitud

        def get_id_solicitud(self):
            return self.id_solicitud
    
        def set_informacion(self, informacion):
            self.informacion = informacion

        def get_informacion(self):
            return self.informacion

    def deserialize(self, string_cmd):
        comando = json.loads(string_cmd)
        comando_respuesta = ComandoSolicitar()
        comando_respuesta.__dict__.update(comando)
        datos = ComandoSolicitar.Datos()
        datos.__dict__.update(comando['datos'])
        comando_respuesta.set_datos(datos)
        return comando_respuesta
