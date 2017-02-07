import comando.Comando as Comando
import json

class ComandoInformar(Comando):
    
    def __init__(self):
        super().__init__("informar")
    
    class Datos:
        def __init__(self):
            self._id_solicitud = ""
            self._informacion = [] #ElementoInformacion
        
        def set_id_solicitud(self, id_solicitud):
            self._id_solicitud = id_solicitud
        
        def set_informacion(self, informacion)
            self._informacion = informacion

        def get_id_solicitud():
            return self._id_solicitud

        def get_informacion():
            return self._informacion
    
    class ElementoInformacion:
        def __init__(self):
            self.clave = ""
            self.datos = [] #DatosInformacion

    class DatosInformacion:
        def __init__(self, clave, valor):
            self._clave = clave
            self._valor = valor
        
        def set_clave(self, clave):
            self._clave = clave

        def set_valor(self, valor):
            self._valor = valor

        def get_clave():
            return self._clave

        def get_valor():
            return self._valor

    class ElementoProcesador(ElementoInformacion):
        def __init__(self):
            super()._clave = "procesador"
            super()._datos.append(DatosInformacion("nombre",""))
            super()._datos.append(DatosInformacion("descripcion",""))
            super()._datos.append(DatosInformacion("fabricante",""))
            super()._datos.append(DatosInformacion("arquitectura",""))
            super()._datos.append(DatosInformacion("cantidad_nucleos","-1"))
            super()._datos.append(DatosInformacion("cantidad_procesador","-1"))
            super()._datos.append(DatosInformacion("velocidad","-1"))
            super()._datos.append(DatosInformacion("tamanio_cache","-1"))
        
