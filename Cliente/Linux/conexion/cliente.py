# coding:utf-8
import socket as sk
import json
import time
import random
from recoleccion.collector import Collector
from conexion.comando import Comando
from conexion.comando_configurar import ComandoConfigurar
from conexion.comando_informar import ComandoInformar
from conexion.comando_inicio import ComandoInicio
from conexion.comando_maquina_nueva import ComandoMaquinaNueva
from conexion.comando_maquina_registrada import ComandoMaquinaRegistrada
from conexion.comando_reportar import ComandoReportar
from conexion.comando_solicitar import ComandoSolicitar
from util.constantes import *

class Cliente:

    def __init__(self, ip_servidor, puerto):
        self._ip_servidor = ip_servidor
        self._puerto = puerto
        self._socket = None
        self._recolector = Collector()
        self._max_intentos_envio = 4

    def set_ip_servidor(self, ip_servidor):     
        self._ip_servidor = ip_servidor
    
    def set_puerto(self, puerto):
        """El puerto debe ser numérico"""
        self._puerto = puerto        
    
    def get_ip_servidor():
        return self._ip_servidor

    def get_puerto():
        return self._puerto

    def conectar(self):
        self._socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM, 0) #tcp
        server = (self._ip_servidor, self._puerto)
        try:        
            self._socket.connect(server)
            print("Se conectó con servidor => server:", self._ip_servidor)
        except sk.error as ge:
            self._socket = None
            print("Problemas al conectarse con el servidor:\nTipo => ", type(ge), " Mensaje => ", ge)
            raise KeyboardInterrupt

    def enviar_comando(self, cmd):
        print("Comando a enviar (max 2 intentos) =>" , cmd.comando)
        time.sleep(self.segundos_de_espera())
        if(not self.enviar(cmd.serialize())):
            print("Comando a enviar (último intento) =>" , cmd.comando)
            time.sleep(self.segundos_de_espera())
            self.enviar(cmd.serialize())

    def segundos_de_espera(self):
        rnd = random.random() * random.randint(1,15)
        print("Tiempo de espera para enviar:",rnd)
        return rnd

    def enviar(self, datos):
        mensaje_bytes = (datos + EOM).encode('ascii')
        print("Información =>", datos)
        tamanio_msj = int(len(mensaje_bytes))
        bytes_enviados = 0
        while bytes_enviados < tamanio_msj:
            mensaje_restante = mensaje_bytes[bytes_enviados:]
            bytes_enviados = bytes_enviados + self._socket.send(mensaje_bytes)
            if bytes_enviados == 0:
                print("Conexión con servidor rota")
                raise KeyboardInterrupt
        return (bytes_enviados == tamanio_msj)

    def recibir(self):
        max_datos = 1024
        datos = self._socket.recv(max_datos)   #en bytes
        if datos == b'':
            print("Se desconectó servidor")
            raise KeyboardInterrupt
        mensaje = datos.decode(encoding='ascii') #string
        return mensaje

    def recibir_comando(self):
        mensaje_recibido = self.recibir()
        cmd_recibido = None
        comando = json.loads(mensaje_recibido)
        if comando is not None:
            print("Comando recibido =>", comando['comando'])
            if (comando['comando'] == MAQUINA_REGISTRADA):
                cmd_recibido = ComandoMaquinaRegistrada()
                cmd_recibido = cmd_recibido.deserialize(mensaje_recibido)
            elif (comando['comando'] == CONFIGURAR):
                cmd_recibido = ComandoConfigurar()
                cmd_recibido = cmd_recibido.deserialize(mensaje_recibido)
            elif (comando['comando'] == SOLICITAR):
                cmd_recibido = ComandoSolicitar()
                cmd_recibido = cmd_recibido.deserialize(mensaje_recibido)
        return cmd_recibido

    def desconectar(self):
        if (self._socket is not None):
            self._socket.shutdown(sk.SHUT_RDWR)
            self._socket.close()

    def recolectar_componentes(self, informacion_solicitada):
        """Recolecta datos de los componenes que se encuentren en 
        informacion_solicitada. Puede ser procesador, memorias ram o discos duros.
        Retorna un array que contiene objetos de tipo ComandoInformar.ElementoInfomacion"""
        informacion_informar = []
        print("Información a recolectar => ", informacion_solicitada)
        maquina = self._recolector.get_maquina()
        for i in range(0, len(informacion_solicitada)):
            if informacion_solicitada[i] == PROCESADOR:
                procesador = maquina.getprocesador()
                elemento_procesador = ComandoInformar.ElementoProcesador()
                elemento_procesador.get_datos().actualizar_datos(procesador)
                informacion_informar.append(elemento_procesador)
            elif informacion_solicitada[i] == MEMORIAS_RAM:
                memorias_ram = maquina.getmemoriasram()
                elemento_memorias_ram = ComandoInformar.ElementoMemoriasRam()
                datos_memorias = []
                for i in range(0,len(memorias_ram)):
                    memoria_datos = ComandoInformar.DatosInformacionMemoriasRam()
                    memoria_datos.actualizar_datos(memorias_ram[i])
                    datos_memorias.append(memoria_datos)
                elemento_memorias_ram.set_datos(datos_memorias)
                informacion_informar.append(elemento_memorias_ram)
            elif informacion_solicitada[i] == DISCOS_DUROS:
                discos_duros = maquina.getdiscosduros()
                elemento_discos_duros = ComandoInformar.ElementoDiscosDuros()
                datos_discos = []
                for i in range(0,len(discos_duros)):
                    disco_datos = ComandoInformar.DatosInformacionDiscosDuros()
                    disco_datos.actualizar_datos(discos_duros[i])
                    datos_discos.append(disco_datos)
                elemento_discos_duros.set_datos(datos_discos)
                informacion_informar.append(elemento_discos_duros)
        return informacion_informar

    def generar_cmds_informar(self, informes):
        cmds_informar = []
        for informe in informes:
            if informe.get_tipo() == "inicio_sistema":
                info_solicitada = informe.get_informacion()
                cmd_informar = self.generar_cmd_informar(info_solicitada, id_informe = informe.get_id())
                cmds_informar.append(cmd_informar)
        return cmds_informar

    def generar_cmd_inicio(self, id_cliente):
        cmd_inicio = ComandoInicio()
        datos_cmd_inicio = ComandoInicio().Datos()
        datos_cmd_inicio.set_id(id_cliente)
        cmd_inicio.set_datos(datos_cmd_inicio)
        return cmd_inicio

    def generar_cmd_maquina_nueva(self):
        maquina_nueva = self._recolector.get_maquina_nueva()
        cmd_maquina_nueva = ComandoMaquinaNueva()
        cmd_maquina_nueva.datos.actualizar_datos(maquina_nueva)
        return cmd_maquina_nueva

    def generar_cmd_informar(self, info_solicitada, id_solicitud = None, id_informe = None):
        cmd_informar = ComandoInformar()
        if (id_solicitud is not None):
            print("id_solicitud =>" , id_solicitud)
            cmd_informar.datos.set_id_solicitud(id_solicitud)
        else:
            print("id_informe =>" , id_informe)
            cmd_informar.datos.set_id_informe(id_informe)
        info_a_reportar = self.recolectar_componentes(info_solicitada)
        cmd_informar.datos.set_informacion(info_a_reportar)
        return cmd_informar

    def es_comando_configurar(self, cmd):
        return (type(cmd) is ComandoConfigurar)

    def es_comando_solicitar(self, cmd):
        return (type(cmd) is ComandoSolicitar)
