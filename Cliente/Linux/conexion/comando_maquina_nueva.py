import comando.Comando as Comando
import json

class ComandoMaquinaNueva(Comando):
    
    def __init__(self):
        super().__init__("maquina_nueva")

    def serialize():
        return json.dump(vars(self))
    
    def deserialize(string_json)
        comando = json.loads(string_json)
        return ComandoMaquinaNueva(**comando) #mapea el array comadno a una instancia de objeto.
