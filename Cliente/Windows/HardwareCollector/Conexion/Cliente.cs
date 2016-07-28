using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading.Tasks;

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
                while (true) {
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

        public void enviarComando(Comando comando) {
            this.enviar(comando.Serialize());
        }

        public void enviar(string datos)
        {
            byte[] mensaje = Encoding.ASCII.GetBytes(datos + Comando.caracterFinComando);
            Console.WriteLine("Envie: " + datos);
            int bytesEnviados = socket.Send(mensaje);
        }

        public string recibir() {
            byte[] buffer = new byte[1024];
            int bytesRecibidos = socket.Receive(buffer);
            //bytesRecibidos es la cantidad de bytes recibidos
            string mensaje = Encoding.ASCII.GetString(buffer, 0, bytesRecibidos);
            return mensaje;
        }

        public Comando recibirComando() {
            string mensajeRecibido = recibir();
            return Comando.DeserializeComando(mensajeRecibido);
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
