import socket as sk
import ipaddress as ip
from conexion.comando import Comando

class Cliente:

    def __init__(self):
        self._ip_servidor = None
        self._puerto = 0
        self._socket = None

    def set_ip_servidor(self, ip_servidor):
        self._ip_servidor = ip.ip_address(ip_servidor)
    
    def set_puerto(self, puerto):
        self._puerto = puerto
    
    def get_ip_servidor():
        return self._ip_servidor

    def get_puerto():
        return self._puerto

    def conectar(self):
        self._socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM, 0) #tcp
        server = (str(self._ip_servidor), int(self._puerto))
        self._socket.connect(server)

    def comenzar(self):
        #revisar excepciones
        self.conectar()
        print("conectado")
        while True:
            mensaje = self.recibir()
            print(mensaje)
            if(mensaje == "fin"):
                break
        desconectar()

    def enviar_comando(self, cmd):
        self.enviar(cmd.serialize())

    def enviar(self, datos):
        mensaje_bytes = datos + comando.Comando.CARACTER_FIN_COMANDO.encode('utf-8')
        print("DATOS ENVIADOS -> " + mensajes)
        bytes_enviados = self._socket.send(mensajes_bytes)

    def recibir(self):
        max_datos = 1024
        datos = self._socket.recv(max_datos)   #en bytes
        mensaje = datos.decode(encoding='UTF-8') #string
        return mensaje

    def recibir_comando(self):
        mensaje_recibido = self.recibir()
        return None

    def desconectar(self):
        if (self._socket != None):
            self._socket.shutdown(self._socket.SHUT_RDWR)
            self._socket.close()
    

