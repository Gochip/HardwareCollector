using System;
using System.Management;
using System.Collections.Generic;
using System.Web.Script.Serialization;
using HardwareCollector.Recoleccion;
using HardwareCollector.Componente;
using HardwareCollector.Conexion;
using HardwareCollector.Util;
using HardwareCollector.Excepciones;
using System.Net.Sockets;
using System.IO;

namespace HardwareCollector.Principal
{
    public class Controlador
    {
        private Boolean logging;
        private Logger logger;
        private ArchivoConfiguracion config;
        private Cliente cliente;
        private Boolean detener;
        public enum ModoFuncionamiento { Activo, Pasivo };

        public Controlador()
        {
            this.logging = false;
            this.detener = false;
        }

        public Controlador(string logPath)
        {
            this.detener = false;
            this.logging = true;
            this.logger = new Logger(logPath);
        }

        public void Trabajar() {
            try
            {
                Comenzar();
                Conectar();
                FaseInicial();
                FaseFuncionamiento();
            }
            catch (Exception ex)
            {
                log(ex.Message);
            }
        }

        public void Comenzar()
        {
            if (ControladorArchivoConfiguracion.ExisteArchivo())
            {
                config = ControladorArchivoConfiguracion.LeerArchivo();
                if (ControladorArchivoConfiguracion.PoseeIpValida(config) && ControladorArchivoConfiguracion.PoseePuertoValido(config))
                {
                    cliente = new Cliente();
                    cliente.ipServidor = config.configuracion.servidor.ip;
                    cliente.puertoServidor = config.configuracion.servidor.puerto;
                }
                else
                {
                    throw new ConfigurationException("IP o puerto del servidor no válidos en el archivo de configuración");
                }
            }
            else
            {
                throw new ConfigurationException("No existe el archivo de configuración");
            }
            this.detener = false;
        }

        public void Conectar()
        {
            try
            {
                cliente.conectar();
            }
            catch (SocketException se)
            {
                //10061: servidor no encontrado
                if (se.ErrorCode.Equals(10061))
                {
                    throw new ConnectionException("Servidor apagado.");
                }
                else
                {
                    throw new ConnectionException("Error al tratar de conectarse: " + se.ToString());
                }
            }
        }

        public void Terminar()
        {
            if (this.logging)
            {
                this.logger.close();
            }
            if (this.cliente != null)
            {
                this.cliente.desconectar();
            }
        }

        public void FaseInicial()
        {
            if (!config.PoseeId())
            {
                Recolector recolector = new Recolector();
                ComandoMaquinaNueva comandoMaquinaNueva = new ComandoMaquinaNueva();
                comandoMaquinaNueva.datos.nombre_maquina = recolector.GetNombreMaquina();
                SistemaOperativo sistemaOperativo = recolector.GetSistemaOperativo();
                comandoMaquinaNueva.datos.sistema_operativo.nombre = sistemaOperativo.Nombre;
                comandoMaquinaNueva.datos.sistema_operativo.version = sistemaOperativo.Version;
                cliente.enviarComando(comandoMaquinaNueva);
                log("ENVIO COMANDO MAQUINA NUEVA - SOLICITANDO ID");

                ComandoMaquinaRegistrada comandoMaquinaRegistrada = ((ComandoMaquinaRegistrada)cliente.recibirComando());
                string id = comandoMaquinaRegistrada.datos.id;
                config.id = id;
                log("COMANDO MAQUINA REGISTRADA RECIBIDO, ID MAQUINA: " + id);
                ControladorArchivoConfiguracion.EscribirArchivo(config);
                config = ControladorArchivoConfiguracion.LeerArchivo();
                ComandoInicio comandoInicio = new ComandoInicio();
                comandoInicio.datos.id = config.id;
                log("ENVIO COMANDO INICIO SOLICTANDO CONFIGURACION");
                cliente.enviarComando(comandoInicio);

                //necesito configuracion
                //espero el mensaje del servidor
                ComandoConfigurar comandoConfigurar = ((ComandoConfigurar)cliente.recibirComando());
                config.configuracion.informes = ((ArchivoConfiguracion)comandoConfigurar.datos.configuracion).configuracion.informes;
                ControladorArchivoConfiguracion.EscribirArchivo(config);
                log("RECIBO COMANDO CONFIGURAR, CONFIGURACION RECIBIDA");
            }
            else
            {
                //aviso que me conecte y puedo empezar a trabajar
                log("ENVIO COMANDO INICIO SOLICTANDO CONFIGURACION");
                ComandoInicio comandoInicio = new ComandoInicio();
                comandoInicio.datos.id = config.id;
                cliente.enviarComando(comandoInicio);

                log("RECIBO COMANDO CONFIGURAR, CONFIGURACION RECIBIDA");
                //piso la configuracion actual del cliente, podria solo pisar la parte de informes (y no la id cliente y datos del servidor)
                ComandoConfigurar comandoConfigurar = (ComandoConfigurar)cliente.recibirComando();
                config.configuracion.informes = ((ArchivoConfiguracion)comandoConfigurar.datos.configuracion).configuracion.informes;
                ControladorArchivoConfiguracion.EscribirArchivo(config);
            }
            
            //ahora debo verificar si tengo un informe programando al inicio (del sistema o mas bien del servicio...)
            log("VERIFICO EXISTENCIA DE INFORME AL INICIO DEL SISTEMA (INICIO DEL SERVICIO)");
            for (int i = 0; i < config.configuracion.informes.Count; i++)
            {
                ArchivoConfiguracion.Informe informe = config.configuracion.informes[i];
                if (informe.tipo == "inicio_sistema")
                {
                    log("ID INFORME: " + informe.id);
                    string info = "";
                    for(int a = 0;a< informe.informacion.Count; a++)
                    {
                        info += informe.informacion[a] + ",";
                    }
                    log("INFORMACION DE INFORME: "+ info);
                    ComandoInformar comandoInformar = ArmarComandoInformar(ModoFuncionamiento.Pasivo, informe.id, informe.informacion);
                    log("ENVIO COMANDO INFORMAR");
                    cliente.enviarComando(comandoInformar);
                }
            }
        }

        public void FaseFuncionamiento()
        {
            log("EN FUNCIONAMIENTO");
            while (!this.detener)
            {
                Comando comando = cliente.recibirComando();
                if (comando is ComandoConfigurar)
                {
                    log("RECIBO COMANDO CONFIGURAR, CONFIGURACION RECIBIDA");
                    //piso la configuracion actual del cliente, podria solo pisar la parte de informes (y no la id cliente y datos del servidor)
                    ComandoConfigurar comandoConfigurar = (ComandoConfigurar)comando;
                    config.configuracion.informes = ((ArchivoConfiguracion)comandoConfigurar.datos.configuracion).configuracion.informes;
                    ControladorArchivoConfiguracion.EscribirArchivo(config);
                }
                else if (comando is ComandoSolicitar)
                {
                    log("RECIBO COMANDO SOLICITAR");
                    ComandoSolicitar comandoSolicitar = (ComandoSolicitar)comando;
                    log("ID SOLICITUD: " + comandoSolicitar.datos.id_solicitud.ToString());
                    log("INFORMACION SOLICITADA: " + comandoSolicitar.datos.informacion.ToString());
                    ComandoInformar comandoInformar = ArmarComandoInformar(ModoFuncionamiento.Activo, comandoSolicitar.datos.id_solicitud, comandoSolicitar.datos.informacion);
                    log("ENVIO COMANDO INFORMAR");
                    cliente.enviarComando(comandoInformar);
                }
            }
        }

        private ComandoInformar ArmarComandoInformar(ModoFuncionamiento modoFuncinamiento, int idInformeOSolicitud, List<string> informacionSolicitada) {
            log("En armado informar");
            ComandoInformar comandoInformar = new ComandoInformar();
            if (modoFuncinamiento == ModoFuncionamiento.Activo)
            {
                comandoInformar.datos.id_solicitud = idInformeOSolicitud;
                log("Modo activo");
            }
            else if (modoFuncinamiento == ModoFuncionamiento.Pasivo) {
                comandoInformar.datos.id_informe = idInformeOSolicitud;
                log("Modo pasivo");
            }
            log("idInformeOSolicitud: " + idInformeOSolicitud);
            List<ComandoInformar.ElementoInformacion> informacionInformar = new List<ComandoInformar.ElementoInformacion>();
            log("Cree informacionInformar");
            Recolector recolector = new Recolector();
            log("Cree Recolector");
            //por defecto pido toda la maquina, es ineficiente
            //Maquina maquina = recolector.GetMaquina();
            Maquina maquina = new Maquina();

            maquina.Procesador = recolector.GetProcesador();
            log("obtengo procesador");
            maquina.DiscosDuros = recolector.GetDiscosDuros();
            log("obtengo discos");
            maquina.MemoriasRam = recolector.GetMemoriasRam();
            log("obtengo GetMemoriasRam");
            for (int i = 0; i < informacionSolicitada.Count; i++)
            {
                if (informacionSolicitada[i] == "procesador")
                {
                    log("Busco procesador");
                    Procesador procesador = maquina.Procesador;
                    ComandoInformar.ElementoProcesador elementoProcesador = new ComandoInformar.ElementoProcesador();
                    ((ComandoInformar.DatosInformacionProcesador)elementoProcesador.datos).nombre = procesador.Nombre;
                    ((ComandoInformar.DatosInformacionProcesador)elementoProcesador.datos).descripcion = procesador.Descripcion;
                    ((ComandoInformar.DatosInformacionProcesador)elementoProcesador.datos).fabricante = procesador.Fabricante;
                    ((ComandoInformar.DatosInformacionProcesador)elementoProcesador.datos).arquitectura = procesador.Arquitectura;
                    ((ComandoInformar.DatosInformacionProcesador)elementoProcesador.datos).cantidad_nucleos = procesador.CantidadNucleos;
                    ((ComandoInformar.DatosInformacionProcesador)elementoProcesador.datos).velocidad = procesador.Velocidad.ToString();
                    ((ComandoInformar.DatosInformacionProcesador)elementoProcesador.datos).tamanio_cache = procesador.Cache.ToString();
                    informacionInformar.Add(elementoProcesador);
                    log("Agrego procesador");
                }
                else if (informacionSolicitada[i] == "memorias_ram")
                {
                    List<MemoriaRam> memorias = maquina.MemoriasRam;
                    ComandoInformar.ElementoMemoria elementoMemoria = new ComandoInformar.ElementoMemoria();
                    log("Busco rams");
                    foreach (MemoriaRam memoria in memorias)
                    {
                        log("Busco ram");
                        ComandoInformar.DatosInformacionMemoriasRam dato = new ComandoInformar.DatosInformacionMemoriasRam();
                        dato.banco = memoria.Banco;
                        dato.tecnologia = memoria.Tecnologia;
                        dato.fabricante = memoria.Fabricante;
                        dato.numero_serie = memoria.NumeroSerie;
                        dato.tamanio_bus_datos = memoria.TamanioBusDatos;
                        dato.velocidad = memoria.Velocidad.ToString();
                        dato.tamanio = memoria.Capacidad.ToString();
                        elementoMemoria.datos.Add(dato);
                        log("Agrego ram");
                    }
                    informacionInformar.Add(elementoMemoria);
                }
                else if (informacionSolicitada[i] == "discos_duros")
                {
                    log("Busco discos");
                    List<DiscoDuro> discos = maquina.DiscosDuros;
                    ComandoInformar.ElementoDiscoDuro elemento = new ComandoInformar.ElementoDiscoDuro();
                    foreach (DiscoDuro disco in discos)
                    {
                        log("Busco disco");
                        ComandoInformar.DatosInformacionDiscosDuros dato = new ComandoInformar.DatosInformacionDiscosDuros();
                        dato.fabricante = disco.Fabricante;
                        dato.modelo = disco.Modelo;
                        dato.numero_serie = disco.NumeroSerie;
                        dato.tipo_interfaz = disco.TipoInterfaz;
                        dato.firmware = disco.Firmware;
                        dato.cantidad_particiones = disco.CantidadParticiones;
                        dato.tamanio = disco.Capacidad.ToString();
                        elemento.datos.Add(dato);
                        log("Agrego disco");
                    }
                    informacionInformar.Add(elemento);
                }
            }
            comandoInformar.datos.informacion = informacionInformar;
            return comandoInformar;
        }

        public void log(string mensaje)
        {
            if (this.logging)
            {
                this.logger.openFile(FileMode.Append);
                this.logger.writeLine(mensaje);
                this.logger.close();
            }
        }

        public void Detener()
        {
            this.detener = true;
        }
    }
}
