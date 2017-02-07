class ArchivoConfiguracion:
    """{id: “id del cliente”,
        configuracion: {servidor: {ip: "", puerto: int}, informes: [{id: “id del informe, decidido por el cliente e informado al servidor”, informacion: [“procesador”, “memorias_ram”, “discos_duros”, “otro_componente…”], tipo: “programado|inicio_sistema|inicio_sesion|apagado”, hora: “hora del informe programado”}]}}"""
    
    def __init__(self, id, configuracion):
        self._id = id
        self._configuracion = configuracion

    def setid(self, id):
        self._id = id

    def setconfiguracion(self, configuracion):
        self._configuracion = configuracion
    
    def getid(self):
        return self._id

    def getconfiguracion(self):
        return self._configuracion


class Configuracion:

    def __init__(self):
        self._informes = []
        self._servidor = None

    def setinformes(self, informes):
        self._informes = informes

    def setservidor(self, servidor):
        self._servidor = servidor
    
    def getinformes(self):
        return self._informes

    def getservidor(self):
        return self._servidor
    
    def add_informe(self, informe):
        self._informes.append(informe)


class Servidor:

    def __init__(self, ip, puerto):
        self._ip = ip
        self._puerto = puerto

    def setip(self, ip):
        self._ip = ip
    
    def setpuerto(self, puerto):
        self._puerto = puerto

    def getip(self):
        return self._ip
    
    def getpuerto(self):
        return self._puerto


class Informe:

    def __init__(self, id, informacion, tipo, hora):
        self._id = id
        self._informacion = informacion
        self._tipo = tipo
        self._hora = hora

    def setid(self, id):
        self._id = id

    def setinformacion(self, informacion):
        self._informacion = informacion

    def settipo(self, tipo):
        self._tipo = tipo

    def sethora(self, hora):
        self._hora = hora

    def getid(self):
        return self._id

    def getinfomacion(self):
        return self._informacion

    def gettipo(self):
        return self._tipo

    def gethora(self):
        return self._hora
