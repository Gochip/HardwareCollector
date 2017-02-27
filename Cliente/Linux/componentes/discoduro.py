
class DiscoDuro():
    
    def __init__(self):                            
        self.fabricante = ""
        self.modelo = ""
        self.numero_serie = ""        
        self.tipo_interfaz = ""
        self.firmware = ""
        self.cantidad_particiones = 0
        self.tamanio = ""
    
    def setid(self, id):
        self.id = id
        
    def setfabricante(self, fabricante):
        self.fabricante = fabricante

    def setmodelo(self, modelo):
        self.modelo = modelo
        
    def setnumeroserie(self, numero_serie):
        self.numero_serie = numero_serie
        
    def settamanio(self, tamanio):
        """En Bytes"""
        self.tamanio = tamanio
    
    def settipointerfaz(self, tipo_interfaz):
        """SCSI, PC, IDE"""
        self.tipo_interfaz = tipo_interfaz
        
    def setfirmware(self, firmware):
        self.firmware = firmware
        
    def setcantidadparticiones(self, cantidad_particiones):
        self.cantidad_particiones = cantidad_particiones        
    
    def tostr(self):        
        disco = 'Modelo:'+ self.modelo + '\n' +'Fabricante:'+self.fabricante+ '\n'+'NúmeroSerie:'+ self.numero_serie + '\n' + 'Capacidad:'+ str(self.tamanio)+'\n'+'TipoInterfaz:'+ self.tipo_interfaz + '\n' + 'Firmware:'+ self.firmware+'\n'+'CantidadParticiones:'+ str(self.cantidad_particiones)
        return disco
