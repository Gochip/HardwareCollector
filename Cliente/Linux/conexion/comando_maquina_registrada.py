import comando.Comando as Comando
import json

class ComandoMaquinaRegistrada(Comando):
    
    def __init__(self):
        super().__init__("maquina_registrada")
    
    class Datos:
        def __init__(self):
            self._id_solicitar = ""

        def set_id_solicitar(self, solicitar):
            self._id_solicitar = solicitar

        def get_id_solicitar():
            return self._id_soliciar
    
    def deserealize(self, string_json):
        comando = json.loads(string_json)
        return ComandoMaquinaRegistrada(**comando)
        
