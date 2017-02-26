import socket as sk
import ipaddress as ip
from conexion.comando import Comando
from conexion.comando_configurar import ComandoConfigurar
from conexion.comando_informar import ComandoInformar
from conexion.comando_inicio import ComandoInicio
from conexion.comando_maquina_nueva import ComandoMaquinaNueva
from conexion.comando_maquina_registrada import ComandoMaquinaRegistrada
from conexion.comando_reportar import ComandoReportar
from conexion.comando_solicitar import ComandoSolicitar
from util.constantes import *
from util.excepciones import *
import json

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
            if(mensaje == "fin"):
                break
        desconectar()

    def enviar_comando(self, cmd):
        self.enviar(cmd.serialize())

    def enviar(self, datos):
        mensaje_bytes = (datos+"\r\n").encode('ascii')
        print("DATOS ENVIADOS -> " + str(mensaje_bytes))
        bytes_enviados = self._socket.send(mensaje_bytes)

    def recibir(self):
        max_datos = 1024
        datos = self._socket.recv(max_datos)   #en bytes
#        datos = b'{"comando": "maquina_registrada", "datos": {"id":"321"}}'
#        datos = b'{"comando": "configurar", "datos": {"configuracion":{"servidor": {"ip": "127.0.0.1", "puerto": 30303}, "informes": [{"id": "prueba_cliente_linux", "informacion": ["procesador", "memorias_ram", "discos_duros"], "tipo": "programado", "hora": "2015-08-15 20:40:00"}]}}}'
#        datos = b'{"comando":"solicitar", "datos": {"id_solicitud":"121", "informacion":["procesador", "memorias_ram","discos_duros"]}}'
        mensaje = datos.decode(encoding='ascii') #string
        return mensaje

    def recibir_comando(self):
        mensaje_recibido = self.recibir()
        cmd_recibido = None
        try:
            comando = json.loads(mensaje_recibido)
            if comando is None:
                pass
            elif (comando['comando'] == MAQUINA_REGISTRADA):
                cmd_recibido = ComandoMaquinaRegistrada()
                cmd_recibido = cmd_recibido.deserialize(mensaje_recibido)
            elif (comando['comando'] == CONFIGURAR):
                cmd_recibido = ComandoConfigurar()
                cmd_recibido = cmd_recibido.deserialize(mensaje_recibido)
            elif (comando['comando'] == SOLICITAR):
                cmd_recibido = ComandoSolicitar()
                cmd_recibido = cmd_recibido.deserialize(mensaje_recibido)
        except KeyError:
            raise ExcepcionComando()
        return cmd_recibido

    def desconectar(self):
        if (self._socket != None):
            self._socket.shutdown(self._socket.SHUT_RDWR)
            self._socket.close()
    

