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
                //indorma estado al servidor
                Comando comandoInformar = new ComandoInformar();
                enviarComando(comandoInformar);
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
            this.enviar(comando.GetJson());
        }

        public void enviar(string datos)
        {
            byte[] mensaje = Encoding.ASCII.GetBytes(datos + Comando.caracterFinComando);
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
            Comando comando = null;
            string mensajeRecibido = recibir();
            comando = Comando.Construir(mensajeRecibido);
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

        public static void StartClient()
        {
            // Data buffer for incoming data.
            byte[] bytes = new byte[1024];

            // Connect to a remote device.
            try
            {
                // Establish the remote endpoint for the socket.
                // This example uses port 11000 on the local computer.
                IPHostEntry ipHostInfo = Dns.Resolve(Dns.GetHostName());
                IPAddress ipAddress = ipHostInfo.AddressList[0];
                IPEndPoint remoteEP = new IPEndPoint(ipAddress, 11000);

                // Create a TCP/IP  socket.
                Socket sender = new Socket(AddressFamily.InterNetwork,
                    SocketType.Stream, ProtocolType.Tcp);

                // Connect the socket to the remote endpoint. Catch any errors.
                try
                {
                    sender.Connect(remoteEP);

                    Console.WriteLine("Socket connected to {0}",
                        sender.RemoteEndPoint.ToString());

                    // Encode the data string into a byte array.
                    byte[] msg = Encoding.ASCII.GetBytes(new ComandoInformar().GetJson() + "<EOF>");

                    // Send the data through the socket.
                    int bytesSent = sender.Send(msg);

                    // Receive the response from the remote device.
                    int bytesRec = sender.Receive(bytes);
                    Console.WriteLine("Echoed test = {0}",
                        Encoding.ASCII.GetString(bytes, 0, bytesRec));

                    // Release the socket.
                    sender.Shutdown(SocketShutdown.Both);
                    sender.Close();

                }
                catch (ArgumentNullException ane)
                {
                    Console.WriteLine("ArgumentNullException : {0}", ane.ToString());
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
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
            }
        }
    }
}
