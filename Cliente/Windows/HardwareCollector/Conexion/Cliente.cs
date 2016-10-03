using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading.Tasks;
using System.Text.RegularExpressions;
using System.Web.Script.Serialization;

namespace HardwareCollector.Conexion
{
    public class Cliente
    {

        public string ipServidor { get; set; }
        public int puertoServidor { get; set; }
        public Socket socket { get; set; }//tcp

        public void comenzar()
        {
            try
            {

                conectar();
                //socket iniciado
                Console.WriteLine("Conectado");
                while (true)
                {
                    string mensaje = recibir();
                    Console.WriteLine(mensaje);
                    if (mensaje == "fin")
                    {
                        break;
                    }
                }
                //indorma estado al servidor
                desconectar();
            }
            catch (SocketException se)
            {
                Console.WriteLine("SocketException : {0}", se.ToString());
            }
            catch (Exception e)
            {
                Console.WriteLine("Unexpected exception : {0}", e.ToString());
            }
        }

        public void conectar()
        {
            IPEndPoint puntoFinal = new IPEndPoint(IPAddress.Parse(ipServidor), puertoServidor);
            socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            socket.Connect(puntoFinal);
            //socket.ReceiveTimeout = 5000;//5 segundos espera como timeout antes de lanzar SocketException al tratar de leer datos recibidos
        }

        public void enviarComando(Comando comando)
        {
            this.enviar(comando.Serialize());
        }

        public void enviar(string datos)
        {
            
            //byte[] mensaje = Encoding.ASCII.GetBytes(datos + "\r\n");
            //Console.WriteLine("Envie: " + datos);
            //int bytesEnviados = socket.Send(mensaje);
            
            int tamanioMensaje = System.Text.Encoding.ASCII.GetByteCount(datos);
            byte[] bytesDatos = System.Text.Encoding.ASCII.GetBytes(datos);
            byte[] bytesTamanioMensaje = System.BitConverter.GetBytes(tamanioMensaje);
            socket.Send(bytesTamanioMensaje);
            socket.Send(bytesDatos);
            
        }

        public string recibir()
        {
            //byte[] buffer = new byte[1024];
            //int bytesRecibidos = socket.Receive(buffer);
            ////bytesRecibidos es la cantidad de bytes recibidos
            //string mensaje = Encoding.ASCII.GetString(buffer, 0, bytesRecibidos);
            //return mensaje;
            
            byte[] rcvLenBytes = new byte[4];
            socket.Receive(rcvLenBytes);
            int rcvLen = System.BitConverter.ToInt32(rcvLenBytes, 0);
            byte[] rcvBytes = new byte[rcvLen];
            socket.Receive(rcvBytes);
            String rcv = System.Text.Encoding.ASCII.GetString(rcvBytes);
            return rcv;
        }

        public Comando recibirComando()
        {
            string mensajeRecibido = recibir();
            Console.WriteLine("mensaje recibido: " + mensajeRecibido);
            string patron = "[\\\"|']?comando[\\\"|']?\\s*:\\s*[\\\"|'](.+)[\\\"|']";
            string nombreComando = "";
            Regex regexp = new Regex(patron, RegexOptions.IgnoreCase);
            Match m = regexp.Match(mensajeRecibido);
            int matchCount = 0;
            while (m.Success)
            {
                Group g = m.Groups[1];
                nombreComando = g.ToString();
                Console.WriteLine("Comando: " + g.ToString());
                m = m.NextMatch();
                matchCount++;
            }
            Comando comando = null;
            if (matchCount > 0)
            {
                if (nombreComando == "configurar")
                {
                    comando = (ComandoConfigurar)new JavaScriptSerializer().Deserialize<ComandoConfigurar>(mensajeRecibido);
                }
                else if (nombreComando == "informar")
                {
                    comando = (ComandoInformar)new JavaScriptSerializer().Deserialize<ComandoInformar>(mensajeRecibido);
                }
                else if (nombreComando == "inicio")
                {
                    comando = (ComandoInicio)new JavaScriptSerializer().Deserialize<ComandoInicio>(mensajeRecibido);
                }
                else if (nombreComando == "maquina_nueva")
                {
                    comando = (ComandoMaquinaNueva)new JavaScriptSerializer().Deserialize<ComandoMaquinaNueva>(mensajeRecibido);
                }
                else if (nombreComando == "maquina_registrada")
                {
                    comando = (ComandoMaquinaRegistrada)new JavaScriptSerializer().Deserialize<ComandoMaquinaRegistrada>(mensajeRecibido);
                }
                else if (nombreComando == "reportar")
                {
                    comando = (ComandoReportar)new JavaScriptSerializer().Deserialize<ComandoReportar>(mensajeRecibido);
                }
                else if (nombreComando == "solicitar")
                {
                    Console.WriteLine(mensajeRecibido);
                    comando = (ComandoSolicitar)new JavaScriptSerializer().Deserialize<ComandoSolicitar>(mensajeRecibido);
                }
            }
            else
            {
                return null;
            }
            return comando;
        }

        public void desconectar()
        {
            if (socket != null)
            {
                socket.Shutdown(SocketShutdown.Both);
                socket.Close();
            }
        }

    }
}
