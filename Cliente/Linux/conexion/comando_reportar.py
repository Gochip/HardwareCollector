from conexion.comando import Comando
import json

class ComandoReportar(Comando):
    
    def __init__(self):
        super().__init__("reportar")
        self._datos = None
    
    class Datos:
        def __init__(self):
            self._id_solicitud = ""

        def set_id_solicitar(self, solicitud):
            self._id_solicitud = solicitud

        def get_id_solicitud(self):
            return self._id_solicitud
    
    def deserealize(string_json):
        comando = json.loads(string_json)
        return ComandoMaquinaRegistrada(**comando)
