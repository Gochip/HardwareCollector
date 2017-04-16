from conexion.comando import Comando
from util.archivo_configuracion import *
import json

class ComandoConfigurar(Comando):
    
    #datos = None
    
    def __init__(self):
        super().__init__("configurar")
        self.datos = None

    def set_datos(self, datos):
        self.datos = datos

    def get_datos(self):
        return self.datos

    def get_informes(self):
        return self.datos.configuracion.get_configuracion().get_informes()

    class Datos:
        def __init__(self):
            self.configuracion = None #archivo configuración

        def set_configuracion(self, configuracion):
            self.configuracion = configuracion

        def get_configuracion(self):
            return self.configuracion


    def deserialize(self, string_json):
        comando = json.loads(string_json)
        comando_respuesta = ComandoConfigurar()
        comando_respuesta.__dict__.update(comando)
        datos = ComandoConfigurar.Datos()
        datos.__dict__.update(comando['datos'])
        archivo = ArchivoConfiguracion()
        configuracion = Configuracion()
        configuracion.__dict__.update(comando['datos']['configuracion']['configuracion'])
        informes_conf = []
        try:
            informes = comando['datos']['configuracion']['configuracion']['informes']
            for i in range(0, len(informes)):
                informes_conf.append((Informe(**informes[i])))
        except KeyError:
            pass
        configuracion.set_informes(informes_conf)
        archivo.set_configuracion(configuracion)
        datos.set_configuracion(archivo)
        comando_respuesta.set_datos(datos)
        return comando_respuesta

