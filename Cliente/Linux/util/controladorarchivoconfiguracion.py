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
        servidor_str = json.dumps(archivo_configuracion.getconfiguracion().getservidor().__dict__)
        informes = archivo_configuracion.getconfiguracion().getinformes()
        if type(informes) is list:
            informes_str = "["
            for i in range(0,len(informes)):
                informes_str += json.dumps(informes[i].__dict__)
                if (i != (len(informes)-1)):
                    informes += ","
            informes_str += "]"
        else:
            informes_str = "[]"    
        str_archivo = '{"id":"'+archivo_configuracion.getid()+'",'
        str_archivo += '"configuracion":{"servidor":'+servidor_str+',"informes":'+informes_str+'}}'
        print(str_archivo)
        archivo = open(self.ruta_archivo_configuracion, "w")
        archivo.write(str_archivo)

    @classmethod
    def leer_archivo(self):
        texto_archivo = self.leer_archivo_como_texto()  
        datos = json.loads(texto_archivo)
        archivo_configuracion = ArchivoConfiguracion()
        servidor = Servidor(**datos['configuracion']['servidor'])
        configuracion = Configuracion()
        configuracion.setservidor(servidor)
        try:
            archivo_configuracion.setid(datos['id'])
            informes = datos['configuracion']['informes']
            for informe in datos['configuracion']['informes']:
                informe_cliente = Informe(informe['id'], informe['informacion'], informe['tipo'], informe['hora'])
                configuracion.add_informe(informe_cliente)        
        except KeyError:
            print("ARCHIVO CORRUPTO")
        except TypeError:
            print("ARCHIVO SIN CONFIGURACIÓN COMPLETA")
        archivo_configuracion.setconfiguracion(configuracion)            
        return archivo_configuracion
