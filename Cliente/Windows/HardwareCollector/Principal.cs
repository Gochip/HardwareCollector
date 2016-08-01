using System;
using System.Management;
using System.Collections.Generic;
using System.Web.Script.Serialization;
using HardwareCollector.Recoleccion;
using HardwareCollector.Componente;
using HardwareCollector.Conexion;
using HardwareCollector.Util;
using System.Net.Sockets;
using System.IO;

namespace HardwareCollector
{
    class Principal
    {

        //https://msdn.microsoft.com/en-us/library/aa390887(v=vs.85).aspx
        public static void Main()
        {
            try
            {
                if (ControladorArchivoConfiguracion.ExisteArchivo())
                {
                    ArchivoConfiguracion archivo = ControladorArchivoConfiguracion.LeerArchivo();
                    //si es el archivo no tiene la direccion del servidor, termina...
                    if (ControladorArchivoConfiguracion.PoseeIpValida(archivo) && ControladorArchivoConfiguracion.PoseePuertoValido(archivo))
                    {
                        Cliente cliente = new Cliente();
                        cliente.ipServidor = archivo.configuracion.servidor.ip;
                        cliente.puertoServidor = archivo.configuracion.servidor.puerto;
                        cliente.conectar();
                        //si no encuentra su id, le solicita al servidor
                        if (!archivo.PoseeId())
                        {
                            cliente.enviarComando(new ComandoMaquinaNueva());
                            ComandoMaquinaRegistrada comandoMaquinaRegistrada = ((ComandoMaquinaRegistrada)cliente.recibirComando());
                            string id = comandoMaquinaRegistrada.datos.id;
                            archivo.id = id;
                            ControladorArchivoConfiguracion.EscribirArchivo(archivo);
                            cliente.enviarComando(new ComandoInicio());
                            //necesito configuracion
                            //espero el mensaje del servidor
                            //ComandoConfigurar comando = ((ComandoConfigurar)cliente.recibirComando());
                        }
                        else
                        {
                            //aviso que me conecte y puedo empezar a trabajar
                            cliente.enviarComando(new ComandoInicio());
                        }
                        //...
                        //estoy en funcionamiento
                        Comando comando = cliente.recibirComando();
                        if (comando is ComandoConfigurar)
                        {
                            //piso la configuracion actual del cliente, podria solo pisar la parte de informes (y no la id cliente y datos del servidor)
                            ComandoConfigurar comandoConfigurar = (ComandoConfigurar)comando;
                            archivo = comandoConfigurar.datos.configuracion;
                            ControladorArchivoConfiguracion.EscribirArchivo(archivo);
                        }
                        else if (comando is ComandoSolicitar)
                        {
                            ComandoSolicitar comandoSolicitar = (ComandoSolicitar)comando;
                            ComandoInformar comandoInformar = new ComandoInformar();
                            comandoInformar.datos.id_solicitud = comandoSolicitar.datos.id_solicitud;
                            List<ComandoInformar.ElementoInformacion> informacionInformar = new List<ComandoInformar.ElementoInformacion>();
                            List<string> informacionSolicitada = comandoSolicitar.datos.informacion;
                            Recolector recolector = new Recolector();
                            //por defecto pido toda la maquina, es ineficiente
                            Maquina maquina = recolector.GetMaquina();
                            for (int i = 0; i < informacionSolicitada.Count; i++)
                            {
                                if (informacionSolicitada[i] == "procesador")
                                {
                                    Procesador procesador = maquina.Procesador;
                                    ComandoInformar.ElementoProcesador elementoProcesador = new ComandoInformar.ElementoProcesador();
                                    
                                    informacionInformar.Add(elementoProcesador);
                                }
                                else if (informacionSolicitada[i] == "memorias_ram")
                                {

                                }
                                else if (informacionSolicitada[i] == "discos_duros")
                                {

                                }
                            }
                            comandoInformar.datos.informacion = informacionInformar;
                            cliente.enviarComando(comandoInformar);
                        }
                    }
                    else {
                        Console.WriteLine("El archivo de configuración existe pero no posee ip y/o puerto válido.");
                    }
                }
                else
                {
                    //si o si debe existir el archivo con la direccion del servidor, sino no puede contectarse...
                    Console.WriteLine("No existe el archivo de configuración, no es posible hallar el servidor.");
                }
            }
            catch (SocketException se)
            {
                //10061:  servidor no encontrado
                if (se.ErrorCode.Equals(10061))
                {
                    Console.WriteLine("Servidor apagado.");
                }
                else
                {
                    Console.WriteLine("Error en el socket: {0}", se.ToString());
                }
            }
            catch (Exception e)
            {
                Console.WriteLine("Error: {0}", e.ToString());
            }
            Console.ReadLine();
        }

        private static void ConsultarDatosClaseWMI(String NombreClase)
        {
            SelectQuery selectQuery = new SelectQuery("SELECT * FROM " + NombreClase);
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(selectQuery);
            foreach (ManagementObject managementObject in searcher.Get())
            {
                foreach (PropertyData propiedad in managementObject.Properties)
                {
                    Console.WriteLine(propiedad.Name + ": " + managementObject[propiedad.Name]);
                }
            }
        }
    }

}

