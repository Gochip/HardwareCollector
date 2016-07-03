using System;
using System.Management;
using System.Web.Script.Serialization;
using HardwareCollector.Recoleccion;
using HardwareCollector.Componente;
using HardwareCollector.Conexion;

namespace HardwareCollector
{
    class Principal
    {

        public static void Main()
        {
            //https://msdn.microsoft.com/en-us/library/aa390887(v=vs.85).aspx
            //Recolector recolector = new Recolector();
            //Maquina maquina = recolector.GetMaquina();
            //string cadena = new JavaScriptSerializer().Serialize(maquina);
            //Console.WriteLine(cadena);
            //maquina = new JavaScriptSerializer().Deserialize<Maquina>(cadena);
            //Console.WriteLine(maquina.Procesador.Arquitectura);

            ComandoInformar cmd = new ComandoInformar();
            Console.WriteLine(cmd.GetJson());

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
