class ArchivoConfiguracion:
    """{id: “id del cliente”,
        configuracion: {servidor: {ip: "", puerto: int}, informes: [{id: “id del informe, decidido por el cliente e informado al servidor”, informacion: [“procesador”, “memorias_ram”, “discos_duros”, “otro_componente…”], tipo: “programado|inicio_sistema|inicio_sesion|apagado”, hora: “hora del informe programado”}]}}"""
    
    def __init__(self):
        self.id = ""
        self.configuracion = None

    def set_id(self, id):
        self.id = id

    def set_configuracion(self, configuracion):
        self.configuracion = configuracion
    
    def get_id(self):
        return self.id

    def get_configuracion(self):
        return self.configuracion
    
    def posee_id(self):
        return (len(self.id) > 0)

    def get_servidor_y_puerto(self):
        return (self.configuracion.get_servidor().get_servidor_y_puerto())

class Configuracion:

    def __init__(self):
        self.informes = []
        self.servidor = None

    def set_informes(self, informes):
        self.informes = informes

    def set_servidor(self, servidor):
        self.servidor = servidor
    
    def get_informes(self):
        return self.informes

    def get_servidor(self):
        return self.servidor
    
    def add_informe(self, informe):
        self.informes.append(informe)


class Servidor:

    def __init__(self, ip, puerto):
        self.ip = ip
        self.puerto = puerto

    def set_ip(self, ip):
        self.ip = ip
    
    def set_puerto(self, puerto):
        self.puerto = puerto

    def get_ip(self):
        return self.ip
    
    def get_puerto(self):
        return self.puerto

    def get_servidor_y_puerto(self):
        return (self.ip, self.puerto)


class Informe:

    def __init__(self, id, informacion, tipo=None, hora=None):
        self.id = id
        self.informacion = informacion
        self.tipo = tipo
        self.hora = hora

    def set_id(self, id):
        self.id = id

    def set_informacion(self, informacion):
        self.informacion = informacion

    def set_tipo(self, tipo):
        self.tipo = tipo

    def set_hora(self, hora):
        self.hora = hora

    def get_id(self):
        return self.id

    def get_informacion(self):
        return self.informacion

    def get_tipo(self):
        return self.tipo

    def get_hora(self):
        return self.hora
