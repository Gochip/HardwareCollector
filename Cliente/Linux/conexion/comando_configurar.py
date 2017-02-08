from conexion.comando import Comando
from util.archivoconfiguracion import *
import json

class ComandoConfigurar(Comando):
    
    datos = None
    
    def __init__(self):
        super().__init__("configurar")
        self.datos = None

    def set_datos(self, datos):
        self.datos = datos

    def get_datos(self):
        return self.datos

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
        configuracion.__dict__.update(comando['datos']['configuracion'])
        servidor = Servidor(**comando['datos']['configuracion']['servidor'])
        informes_conf = []
        try:
            informes = comando['datos']['configuracion']['informes']
            for i in range(0,len(informes)):
                informes_conf.append((Informe(**informes[i])))
        except KeyError:
            print("ERROR EN LA DESERIALIZACIÓN DE CONFIGURAR")
        configuracion.setinformes(informes_conf)
        configuracion.setservidor(servidor)
        archivo.setconfiguracion(configuracion)
        datos.set_configuracion(archivo)
        comando_respuesta.set_datos(datos)
        return comando_respuesta

