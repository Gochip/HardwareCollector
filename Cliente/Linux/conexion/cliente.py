# coding:utf-8
import socket as sk
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
        self._puerto = None
        self._socket = None

    def set_ip_servidor(self, ip_servidor):
        if self.es_direccion_ip_valida(ip_servidor):
            self._ip_servidor = ip_servidor
        else:
            e = Excepcion("IP Servidor no válida")
            e.add_posible_solucion("Revisar IP Servidor en archivo config.json")
            raise e
    
    def set_puerto(self, puerto):
        try:
            self._puerto = int(puerto)
        except:
            e = Excepcion("Puerto no válido")
            e.add_posible_solucion("Revisar puerto en archivo config.json")
            raise e
    
    def get_ip_servidor():
        return self._ip_servidor

    def get_puerto():
        return self._puerto

    def conectar(self):
        self._socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM, 0) #tcp
        server = (self._ip_servidor, self._puerto)
        try:
            self._socket.connect(server)
        except:
            e = Excepcion("Conexión rechazada:")
            e.add_posible_solucion("Servidor corretto?")
            e.add_posible_solucion("Puerto correcto?")
            e.add_posible_solucion("Servidor levantado?")
            raise e

    def enviar_comando(self, cmd):
        self.enviar(cmd.serialize())

    def enviar(self, datos):
        mensaje_bytes = (datos + EOM).encode('ascii')
        print("DATOS ENVIADOS -> " + str(mensaje_bytes))
        tamanio_msj = int(len(mensaje_bytes))
        bytes_enviados = 0
        while bytes_enviados < tamanio_msj:
            try:
                mensaje_restante = mensaje_bytes[bytes_enviados:]
                bytes_enviados = self._socket.send(mensaje_bytes)
            except InterruptedError:
                pass #llamada al sistema interrumpida
            if bytes_enviados == 0:
                e = Excepcion("Conexión con Servidor rota")
                e = e.add_posible_solucion("Reiniciar el programa")
                raise e

    def recibir(self):
        max_datos = 1024
        datos = self._socket.recv(max_datos)   #en bytes
        print(datos)
        if datos == b'':
            raise RuntimeError
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
        if (self._socket is not None):
            self._socket.shutdown(sk.SHUT_RDWR)
            self._socket.close() 
    
    def es_direccion_ip_valida(self, valor):
        """Verifica que la dirección pasada como valor no contenga solo números,
            ni espacios. De lo contrario devuelve False."""
        for caracter in valor:
            if caracter.isspace():
                return False
        return not valor.isdigit();
