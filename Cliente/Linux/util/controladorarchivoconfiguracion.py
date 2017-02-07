#!/usr/bin/env python3
#encoding: UTF-8
import json as json
import os.path as path
from .archivoconfiguracion import *

from pprint import pprint

class ControladorArchivoConfiguracion:

    ruta_archivo_configuracion = "/../config.json"

    @classmethod
    def existe_archivo(self):
        ruta = path.dirname(path.abspath(__file__))
        ruta += self.ruta_archivo_configuracion
        self.ruta_archivo_configuracion = ruta
        return path.exists(self.ruta_archivo_configuracion)

    @classmethod
    def leer_archivo_como_texto(self):
        archivo = open(self.ruta_archivo_configuracion, "r")
        return archivo.read()#.decode("UTF-8")

    @classmethod
    def escribir_archivo(self, archivo_configuracion):
        string_json = json.dumps(archivo_configuracion, sort_keys=True, indent=4)
        archivo = open(self.ruta_archivo_configuracion, "w")
        archivo.write(string_json)

    @classmethod
    def leer_archivo(self):
        texto_archivo = self.leer_archivo_como_texto()    
        datos = json.loads(texto_archivo)
        archivo_configuracion = None
        servidor = Servidor(datos['configuracion']['servidor']['ip'], datos['configuracion']['servidor']['puerto'])
        configuracion = Configuracion()
        configuracion.setservidor(servidor)
        for informe in datos['configuracion']['informes']:
            informe_cliente = Informe(informe['id'], informe['informacion'], informe['tipo'], informe['hora'])
            configuracion.add_informe(informe_cliente)
        archivo_configuracion = ArchivoConfiguracion(datos['id'], configuracion)
        return archivo_configuracion
