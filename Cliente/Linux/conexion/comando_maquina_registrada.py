from conexion.comando import Comando
import json

class ComandoMaquinaRegistrada(Comando):
    
    def __init__(self):
        super().__init__("maquina_registrada")
        self.datos = self.Datos()

    def set_datos(self, datos):
        self.datos = datos
    
    def get_datos(self):
        return self.datos
    
    class Datos:
        def __init__(self):
            self.id = ""

        def set_id(self, solicitud):
            self.id = solicitud

        def get_id(self):
            return self.id
    
    def deserialize(self, string_json):
        comando = json.loads(string_json)
        comando_respuesta = ComandoMaquinaRegistrada()
        comando_respuesta.__dict__.update(comando)
        datos = ComandoMaquinaRegistrada.Datos()
        datos.__dict__.update(comando['datos'])
        comando_respuesta.set_datos(datos)
        return comando_respuesta
        
