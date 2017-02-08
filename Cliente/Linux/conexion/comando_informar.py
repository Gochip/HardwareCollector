from conexion.comando import Comando
from constantes import *
import json

class ComandoInformar(Comando):
    
    def __init__(self):
        super().__init__("informar")
        self.datos = ComandoInformar.Datos()

    def set_datos(self, datos):
        self.datos = datos

    def get_datos(self):
        return datos
    
    def serialize(self):
        datos = self.datos.__dict__
        self.datos = datos
        informacion = []
        for elemento_informacion in self.datos['informacion']:
            if elemento_informacion.componente == PROCESADOR:
                elemento = elemento_informacion.__dict__
                elemento['datos'] = elemento_informacion.datos.__dict__ 
                informacion.append(elemento)
            if elemento_informacion.componente == MEMORIAS_RAM or elemento_informacion.componente == DISCOS_DUROS:
                elementos = elemento_informacion.__dict__
                datos_memorias = []
                for i in range(0,len(elementos['datos'])):
                    datos_memorias.append(elementos['datos'][i].__dict__)
                elementos['datos'] = datos_memorias
                informacion.append(elementos)
        self.datos['informacion'] = informacion
        print(self.__dict__)
#        return json.dumps(self.__dict__)

    class Datos:
        def __init__(self):
            self.id_solicitud = ""
            self.id_informe = ""
            self.hash_configuracion = ""
            self.informacion = [] #ElementoInformacion
        
        def set_id_solicitud(self, id_solicitud):
            self.id_solicitud = id_solicitud

        def set_id_informe(self, id_informe):
            self.id_informe = id_informe
        
        def set_informacion(self, informacion):
            self.informacion = informacion

        def get_id_solicitud():
            return self.id_solicitud

        def get_id_informe():
            return self.id_informe

        def get_informacion():
            return self.informacion
    
    class ElementoInformacion:
        def __init__(self, componente):
            self.componente = componente

        def actualizar_elemento(dict_elemento):
            self.__dict__.update(dict_elemento)

    class DatosInformacion:
        pass

    class ElementoProcesador(ElementoInformacion):
        def __init__(self):
            super().__init__(PROCESADOR)
            self.datos = ComandoInformar.DatosInformacionProcesador()

        def set_datos(self, datos):
            self.datos = datos

        def get_datos(self):
            return self.datos

    class ElementoMemoriasRam(ElementoInformacion):
        def __init__(self):
            super().__init__(MEMORIAS_RAM)
            self.datos = [] #DatosInfomarcionMemorias

        def set_datos(self, datos):
            self.datos = datos

        def get_datos(self):
            return self.datos

    class ElementoDiscosDuros(ElementoInformacion):
        def __init__(self):
            super().__init__(DISCOS_DUROS)
            self.datos = [] #DatosInfomarcionDiscosDuros

        def set_datos(self, datos):
            self.datos = datos

        def get_datos(self):
            return self.datos

    class DatosInformacionProcesador(DatosInformacion):
        def __init__(self):
            self.nombre = ""
            self.descripcion = ""
            self.fabricante = ""
            self.arquitectura = ""
            self.cantidad_nucleos = 0
            self.cantidad_procesadores = 0
            self.velocidad = ""
            self.tamanio_cache = ""

        def actualizar_datos(self, procesador):
            self.__dict__.update(procesador.__dict__)
        
    class DatosInformacionMemoriasRam(DatosInformacion):
        def __init__(self):
            self.banco = ""
            self.tecnologias = ""
            self.fabricante = ""
            self.numero_serie = ""
            self.tamanio_bus_datos = ""
            self.velocidad = ""
            self.tamanio = ""

        def actualizar_datos(self, memoria):
            self.__dict__.update(memoria.__dict__)

    class DatosInformacionDiscosDuros(DatosInformacion):
        def __init__(self):
            self.fabricante = ""
            self.modelo = ""
            self.numero_serie = ""
            self.tipo_interfaz = ""
            self.firmware = ""
            self.cantidad_particiones = 0
            self.tamanio = ""

        def actualizar_datos(self, disco):
            self.__dict__.update(disco.__dict__)
