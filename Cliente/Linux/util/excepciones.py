class ExcepcionSubprocess(Exception):
    pass

class ExcepcionFileIO(Exception):
    def __init__(self, url, mensaje = "No se pudó leer el archivo"):
        self._mensaje = mensaje
        self._url = url
