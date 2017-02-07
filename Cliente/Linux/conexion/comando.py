import json

class Comando:
    CARACTER_FIN_COMANDO = "<EOF>"

    def __init__(self, comando):
        self._comando = comando

    def serialize():
        return json.dump(vars(self))
    
    def deserialize(json):
        return None

    
