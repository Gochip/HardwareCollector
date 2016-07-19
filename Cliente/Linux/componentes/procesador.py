class Procesador():    
    
    def __init__(self):        
        self.nombre = ""
        self.descripcion = ""
        self.tamanio_cache = "" #En KB
        self.arquitectura = ""
        self.cantidad_nucleos = 0
        self.cantidad_procesadores = 0
        self.fabricante = ""
        self.velocidad = "" # En MHz
    
    def setid(self, id):
        self.id = id
    
    def setarquitectura(self, arquitectura):
        self.arquitectura = arquitectura
    
    def setcantidadnucleos(self, cantidad_nucleos):
        self.cantidad_nucleos = cantidad_nucleos

    def setcantidadprocesadores(self, cantidad_procesadores):
        self.cantidad_procesadores = cantidad_procesadores
    
    def setfabricante(self, fabricante):
        self.fabricante = fabricante
    
    def setnombre(self, nombre):
        self.nombre = nombre

    def setdescripcion(self, descripcion):
        self.descripcion = descripcion
    
    def settamaniocache(self, cache):
        """Unidad de medida en KB"""
        self.tamanio_cache = cache
    
    def setvelocidad(self, velocidad):
        """Especifica la velocidad actual del procesador
        (no implica que sea la máxima velocidad). Unidad de medida en MHz"""
        self.velocidad = velocidad
        
    def tostr(self):
        #arquitectura, cantidad_nucleos, cantidad_procesadores, fabricante, nombre, descripcion, cache
        procesador = 'Nombre:'+ self.nombre + '\n' + 'Descripcion:'+ self.descripcion +'\n'+'TamanioCache:'+ self.tamanio_cache + '\n' + 'Arquitectura:'+ self.arquitectura+'\n'+'CantidadNucleos:'+ str(self.cantidad_nucleos) + '\n' + 'CantidadProcesadores:'+ str(self.cantidad_procesadores) +'\n'+'Fabricante:'+ self.fabricante + '\n'+'Velocidad:'+ self.velocidad
        return procesador
    
