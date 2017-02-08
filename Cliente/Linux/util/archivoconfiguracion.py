class ArchivoConfiguracion:
    """{id: “id del cliente”,
        configuracion: {servidor: {ip: "", puerto: int}, informes: [{id: “id del informe, decidido por el cliente e informado al servidor”, informacion: [“procesador”, “memorias_ram”, “discos_duros”, “otro_componente…”], tipo: “programado|inicio_sistema|inicio_sesion|apagado”, hora: “hora del informe programado”}]}}"""
    
    def __init__(self):
        self.id = ""
        self.configuracion = None

    def setid(self, id):
        self.id = id

    def setconfiguracion(self, configuracion):
        self.configuracion = configuracion
    
    def getid(self):
        return self.id

    def getconfiguracion(self):
        return self.configuracion
    
    def posee_id(self):
        if len(self.id) > 0:
            return True
        return False

class Configuracion:

    def __init__(self):
        self.informes = []
        self.servidor = None

    def setinformes(self, informes):
        self.informes = informes

    def setservidor(self, servidor):
        self.servidor = servidor
    
    def getinformes(self):
        return self.informes

    def getservidor(self):
        return self.servidor
    
    def add_informe(self, informe):
        self.informes.append(informe)


class Servidor:

    def __init__(self, ip, puerto):
        self.ip = ip
        self.puerto = puerto

    def setip(self, ip):
        self.ip = ip
    
    def setpuerto(self, puerto):
        self.puerto = puerto

    def getip(self):
        return self.ip
    
    def getpuerto(self):
        return self.puerto


class Informe:

    def __init__(self, id, informacion, tipo, hora):
        self.id = id
        self.informacion = informacion
        self.tipo = tipo
        self.hora = hora

    def setid(self, id):
        self.id = id

    def setinformacion(self, informacion):
        self.informacion = informacion

    def settipo(self, tipo):
        self.tipo = tipo

    def sethora(self, hora):
        self.hora = hora

    def getid(self):
        return self.id

    def getinfomacion(self):
        return self.informacion

    def gettipo(self):
        return self.tipo

    def gethora(self):
        return self.hora
