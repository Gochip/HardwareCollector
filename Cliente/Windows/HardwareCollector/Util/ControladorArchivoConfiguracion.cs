using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Web.Script.Serialization;
using System.IO;

namespace HardwareCollector.Util
{
    public class ControladorArchivoConfiguracion
    {
        public static string RutaArchivoConfiguracion = "C:\\config_hc.json";

        public static bool ExisteArchivo() {
            Console.WriteLine(RutaArchivoConfiguracion);
            return System.IO.File.Exists(RutaArchivoConfiguracion);
        }

        public static string LeerArchivoComoTexto() {
            string salida = "";
            salida = System.IO.File.ReadAllText(RutaArchivoConfiguracion);
            return salida;
            }

        public static void EscribirArchivo(ArchivoConfiguracion configuracion) {
            string json = new JavaScriptSerializer().Serialize(configuracion);
            System.IO.File.WriteAllText(RutaArchivoConfiguracion, json);
        }

        public static ArchivoConfiguracion LeerArchivo() {
           return new JavaScriptSerializer().Deserialize<ArchivoConfiguracion>(ControladorArchivoConfiguracion.LeerArchivoComoTexto());
        }

        public static bool PoseeIpValida(ArchivoConfiguracion archivo)
        {
            return (archivo != null && archivo.configuracion != null && archivo.configuracion.servidor != null && archivo.configuracion.servidor.ip != null && !archivo.configuracion.servidor.ip.Equals(""));
        }

        public static bool PoseePuertoValido(ArchivoConfiguracion archivo)
        {
            return (archivo.configuracion != null && archivo.configuracion.servidor != null  && archivo.configuracion.servidor.puerto != 0);
        }
    }
}
