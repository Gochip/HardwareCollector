import json

class Comando:
    CARACTER_FIN_COMANDO = "\n"

    def __init__(self, comando):
        self.comando = comando

    def serialize(self):
        return json.dumps((self.__dict__))
    
    def deserialize(self, json):
        return None

    
