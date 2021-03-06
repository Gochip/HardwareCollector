#!/usr/bin/env python3
#encoding: UTF-8
import json as json
import os.path as path
from .archivo_configuracion import *
from util.excepciones import *

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
        return archivo.read()

    @classmethod
    def escribir_archivo(self, archivo_configuracion):
        servidor_str = json.dumps(archivo_configuracion.get_configuracion().get_servidor().__dict__)
        informes = archivo_configuracion.get_configuracion().get_informes()
        informes_str = "[]"    
        if type(informes) is list:
            informes_str = "["
            for i in range(0, len(informes)):
                informes_str += json.dumps(informes[i].__dict__)
                if (i != (len(informes) - 1)):
                    informes += ","
            informes_str += "]"            
        str_archivo = '{"id":"' + str(archivo_configuracion.get_id()) + '",'
        str_archivo += '"configuracion":{"servidor":' + servidor_str + ',"informes":' + informes_str+ '}}'
        archivo = open(self.ruta_archivo_configuracion, "w")
        archivo.write(str_archivo)

    @classmethod
    def leer_archivo(self):
        msj = "config.json: Archivo corrupto o mal configurados"
        texto_archivo = self.leer_archivo_como_texto()
        try: 
            datos = json.loads(texto_archivo)
        except: 
            e = Excepcion(msj)
            raise e
        archivo_configuracion = ArchivoConfiguracion()
        try:
            servidor = Servidor(**datos['configuracion']['servidor'])
        except:
            e = Excepcion(msj)
            raise e            
        configuracion = Configuracion()
        configuracion.set_servidor(servidor)
        try:
            archivo_configuracion.set_id(datos['id'])
        except KeyError:
            pass
        try:
            informes = datos['configuracion']['informes']
            for informe in datos['configuracion']['informes']:
                informe_cliente = Informe(informe['id'], informe['informacion'], informe['tipo'], informe['hora'])
                configuracion.add_informe(informe_cliente)        
        except:
            pass
        archivo_configuracion.set_configuracion(configuracion)
        return archivo_configuracion
