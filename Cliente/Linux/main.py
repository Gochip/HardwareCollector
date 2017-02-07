#!/usr/bin/env python3
#encoding: UTF-8

if __name__ == "__main__":
    from pprint import pprint
    import recoleccion.collector as collector
    from util.controladorarchivoconfiguracion import ControladorArchivoConfiguracion
    from conexion.cliente import Cliente
    from conexion import *

    #recolector = collector.Collector()
    #maquina = recolector.get_maquina()
#    print(maquina.tostr())
    if (ControladorArchivoConfiguracion.existe_archivo()):
        archivo = ControladorArchivoConfiguracion.leer_archivo()        
        #creo el cliente, seteo ip servidor y puerto
        cliente = Cliente()
        cliente.set_ip_servidor(archivo.getconfiguracion().getservidor().getip())
        cliente.set_puerto(archivo.getconfiguracion().getservidor().getpuerto())
        #cliente inicia socket con servidor.
        cliente.conectar()
        #si archivo_configuracion.id. lenth == 0 -> enviar comando máquina nueva, recibir id, actualizar archivo
        if (archivo.configuracion.id.length == 0):
            cliente.enviar_comando(comando_maquina_nueva.ComandoMaquinaNueva())
            cmd_maquina_registrada = cliente.recibir_comando()
            id_maquina_registrada = cmd_maquina_registrada.Datos().id
            archivo= id_maquina_registrada
            ControladorArchivoConfiguracion.EscribirArchivo(archivo)
            cliente.enviar_comando(comando_inicio.Inicio())
        else:
            cliente.enviar_comando(comando_inicio.Inicio())
        cmd = cliente.recibirComando() #ya está en funcionamiento
        if (comando is comando_configurar.ComandoConfigurar):
            cmd_configurar = cmd
            archivo = cmd_configurar.Datos.configuracion #llama a clase dentro de clase
            ControladorArchivoConfiguracion.escribir_archivo(archivo)
        elif (comando is comando_solicitar.ComandoSolicitar()):
            cmd_solicitar = cmd
            cmd_informar = comando_informar.ComandoInformar()
            cmd_informar.datos.set_id_solicitud(cmd_solicitar.get_datos().get_id_solicitud())
            informacion_informar = [] # ComandoInformar.ElementoInfomacion
            informacion_solicitada = cmd_solicitar.get_datos().get_informacion()
            recolector = collector.Collector()
            maquina = recolector.get_maquina()
            for i in range(0,len(informacion_solicitada)):
                if informacion_procesada[i] == "procesador":
                    procesador = maquina.get_procesador()
                    informacion_informar.append(comando_informar.ComandoInformar.ElementoInformacion("procesador"))
                elif informacion_procesada[i] == "memorias_ram":
                    procesador = maquina.get_procesador()
                    informacion_informar.append(comando_informar.ComandoInformar.ElementoInformacion("memorias_ram"))
                elif informacion_procesada[i] == "discos_duros":
                    procesador = maquina.get_procesador()
                    informacion_informar.append(comando_informar.ComandoInformar.ElementoInformacion("discos_duros"))
            cmd_informar.datos.set_informacion(informacion_informar)
            cliente.enviarComando(cmd_informar)
    else:
        #si o si debe existir el archivo con la direccion del servidor, sino no puede contectarse...
        #termina
        print("No existe el archivo de configuracion, no es posible hallar el servidor")
