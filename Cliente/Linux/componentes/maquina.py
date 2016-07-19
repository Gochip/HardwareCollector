class Maquina():    
    
    def __init__(self):
        self.ipv4 = ""        
        self.ipv6 = ""
        self.mac = ""
        self.nombre = ""
        self.fabricante = ""
        self.sistema_operativo = ""
        self.memorias_ram = []       
        self.discos_duro = []       
        
    def setid(self, id):
        self.id = id
    
    def setipv4(self, ipv4):
        self.ipv4 = ipv4
    
    def setipv6(self, ipv6):
        self.ipv4 = ipv6
    
    def setmac(self, mac):
        self.ipv4 = mac

    def setnombre(self, nombre):
        self.nombre = nombre
    
    def setfabricante(self, fabricante):
        self.fabricante = fabricante

    def setplaca_madre(self, placa_madre):
        self.placa_madre = placa_madre

    def setbios(self, bios):
        self.bios = bios
    
    def setsistemaoperativo(self, sistema_operativo):
        self.sistema_operativo = sistema_operativo
    
    def setdiscosduro(self, discos_duro):
        self.discos_duro = discos_duro
    
    def setmemoriasram(self, memorias_ram):
        self.memorias_ram = memorias_ram
    
    def setprocesador(self, procesador):
        self.procesador = procesador
    
    def tostr(self):
        maquina = 'Nombre:' + self.nombre + '\n' + 'Fabricante:' + self.fabricante + '\n' + 'SistemaOperativo:' + self.sistema_operativo + '\n\n' + 'DiscosDuro:' + self.listardiscosduro() + '\n\n' + 'Procesador:' + self.procesador.tostr() + '\n\n' + 'MemoriasRam:' + self.listarmemoriasram()
        return maquina
    
    def listarmemoriasram(self):
        strmemorias = ""
        for memoria in self.memorias_ram:
            strmemorias = strmemorias + '\n' + memoria.tostr()
        return strmemorias
    
    def listardiscosduro(self):
        strdiscos = ""
        for disco in self.discos_duro:
            strdiscos = strdiscos + '\n' + disco.tostr()
        return strdiscos