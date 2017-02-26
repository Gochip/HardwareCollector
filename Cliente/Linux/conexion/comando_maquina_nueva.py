from conexion.comando import Comando
import json

class ComandoMaquinaNueva(Comando):
    
    def __init__(self):
        super().__init__("maquina_nueva")
        self.datos = self.Datos()

    def get_datos(self):
        return self.datos

    class Datos:
        def __init__(self):
            self.nombre_maquina = ""
            self.sistemaoperativo = None

        def actualizar_datos(self, maquina):
            self.nombre_maquina = maquina.getnombre()
            self.sistemaoperativo = ComandoMaquinaNueva.DatosSistemaOperativo()
            self.sistemaoperativo.actualizar_so(maquina.getsistemaoperativo().__dict__)

    class DatosSistemaOperativo:
        def __init__(self):
            self.nombre = ""
            self.version = ""

        def actualizar_so(self, dict_elemento):
            self.__dict__.update(dict_elemento)

    def serialize(self):
        datos_so = self.datos.sistemaoperativo.__dict__
        self.datos.sistemaoperativo = datos_so
        datos = self.datos.__dict__
        self.datos = datos
        print(self)
        return json.dumps(self.__dict__)
