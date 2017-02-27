class ExcepcionSubprocess(Exception):
    pass

class ExcepcionFileIO(Exception):
    def __init__(self, url, mensaje = "No se pudó leer el archivo"):
        self._mensaje = mensaje
        self._url = url

class ExcepcionComando(Exception):
    def __init__(self, mensaje = "COMANDO NO INDENTIFICADO"):
        self._mensaje = mensaje

class Excepcion(Exception):
    def __init__(self, mensaje = None):
        self._mensaje = mensaje
        self._sugerencias = []

    def add_posible_solucion(self, sugerencia):
        self._sugerencias.add(sugerencia)

    def imprimir_posibles_soluciones(self):
        sugerencias = "Sugerencias\n"
        for i in range(0, sugerencias):
            sugerencias += (i + 1) + "- " + sugerencias[i] + "\n"
        return sugerencias
