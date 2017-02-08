
class MemoriaRam():
        
    def __init__(self):        
        self.banco = ""
        self.tecnologias = "" #EPROM, VRAM
        self.fabricante = ""        
        self.numero_serie = ""
        self.tamanio_bus_datos = ""
        self.velocidad = ""
        self.tamanio = ""

    def setid(self, id):
        self.id = id
    
    def setbanco(self, banco):
        self.banco = banco
        
    def setfabricante(self, fabricante):
        self.fabricante = fabricante
    
    def settamanio(self, tamanio):
        """Unidad de medida en Bytes"""
        self.tamanio = tamanio
        
    def setnumeroserie(self,numero_serie):
        self.numero_serie = numero_serie
    
    def settamaniobusdatos(self, tamanio_bus_datos):
        """En Bits"""
        self.tamanio_bus_datos = tamanio_bus_datos
        
    def setvelocidad(self, velocidad):
        """En MHz"""
        self.velocidad = velocidad
        
    def settecnologia(self, tecnologia):
        """EPROM, VRAM"""
        self.tecnologias = tecnologia
    
    def tostr(self):        
        memoria = 'Banco:'+ self.banco + '\n' +'Fabricante:'+self.fabricante+ '\n'+'Tamanio:'+ self.tamanio + '\n' + 'NumeroDeSerie:'+ self.numero_serie+'\n'+'TamanioBusDatos:'+ self.tamanio_bus_datos + '\n' + 'Velocidad:'+ self.velocidad+'\n'+'Tecnologia:'+ self.tecnologias
        return memoria    
