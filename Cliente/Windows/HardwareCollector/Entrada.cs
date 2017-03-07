using System;
using System.Management;
using System.Collections.Generic;
using System.Web.Script.Serialization;
using HardwareCollector.Recoleccion;
using HardwareCollector.Componente;
using HardwareCollector.Conexion;
using HardwareCollector.Principal;
using HardwareCollector.Util;
using System.Net.Sockets;
using System.IO;

namespace HardwareCollector
{
    class Entrada
    {

        private static Controlador controlador;

        //https://msdn.microsoft.com/en-us/library/aa390887(v=vs.85).aspx
        public static void Main()
        {
            controlador = new Controlador("d:\\logs.txt");
            controlador.Trabajar();
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

