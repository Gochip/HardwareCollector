#!/usr/bin/env python3
# coding:utf-8
import sys
from util.controlador_archivo_configuracion import ControladorArchivoConfiguracion
from util.constantes import *
from conexion.cliente import Cliente

try:
    cliente = None
    if (ControladorArchivoConfiguracion.existe_archivo()):
        archivo = ControladorArchivoConfiguracion.leer_archivo()
        ip_servidor = archivo.get_configuracion().get_servidor().get_ip()
        puerto_servidor = archivo.get_configuracion().get_servidor().get_puerto()
        cliente = Cliente(ip_servidor, puerto_servidor)
        cliente.conectar()
        if (not archivo.posee_id()):
            cliente.enviar_comando(cliente.generar_cmd_maquina_nueva())
            cmd_maquina_registrada = cliente.recibir_comando()
            id_maquina_registrada = cmd_maquina_registrada.get_datos().get_id()
            archivo.set_id(id_maquina_registrada)
            ControladorArchivoConfiguracion.escribir_archivo(archivo)
            cliente.enviar_comando(cliente.generar_cmd_inicio(archivo.get_id()))
        else:
            cliente.enviar_comando(cliente.generar_cmd_inicio(archivo.get_id()))
            archivo = ControladorArchivoConfiguracion.leer_archivo()
            informes = archivo.get_configuracion().get_informes()
            cmds_informar = cliente.generar_cmds_informar(informes)
            for cmd_informar in cmds_informar:
                cliente.enviar_comando(cmd_informar)
        while (True):
            cmd = cliente.recibir_comando()
            if (cliente.es_comando_configurar(cmd)):
                cmd_configurar = cmd
                informes = cmd_configurar.get_informes()
                archivo.get_configuracion().set_informes(informes)
                ControladorArchivoConfiguracion.escribir_archivo(archivo)                
                archivo = ControladorArchivoConfiguracion.leer_archivo()
                informes_archivo = archivo.get_configuracion().get_informes()
                cmds_informar = cliente.generar_cmds_informar(informes_archivo)
                for cmd_informar in cmds_informar:
                    cliente.enviar_comando(cmd_informar) #envío de informes
            elif (cliente.es_comando_solicitar(cmd)):                
                cmd_solicitar = cmd
                id_sol = cmd_solicitar.get_datos().get_id_solicitud()
                info_solicitada = cmd_solicitar.get_datos().get_informacion()
                cmd_informar = cliente.generar_cmd_informar(info_solicitada, id_solicitud = id_sol)
                cliente.enviar_comando(cmd_informar)
            elif(cmd is None):
                print("Comando recibido no identificado => ", cmd)
    else:
        #No se encuentra archivo, termina la ejecución
        print("config.json: No existe archivo de configuración")
        raise KeyboardInterrupt
except KeyboardInterrupt:
    sys.exit(0)
finally:
    if cliente is not None:
        cliente.desconectar()
    print("\nHARDWARE COLLECTOR FINALIZADO")
    sys.exit(0)
