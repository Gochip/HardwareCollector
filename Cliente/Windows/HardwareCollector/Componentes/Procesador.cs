using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace HardwareCollector.Componente
{
    public class Procesador
    {
        /*public String Nombre { get; set; }//>>Name<<//Caption//DeviceID//Name//ProcessorId//ProcessorType
        public String Descripcion { get; set; }//Description
        public String Fabricante { get; set; }//Manufacturer
        public String Arquitectura { get; set; }//AddressWidth
        public int CantidadNucleos { get; set; }//NumberOfCores
        public int CantidadProcesadores { get; set; }//NumberOfLogicalProcessors
        numeroSerie//SerialNumber
                   //Status
                   //Version
        velocidad; //MaxClockSpeed (MHz)
        public double Cache { get; set; }//L2CacheSize(KB)*/

        public string Nombre { get; set; }
        public string Descripcion { get; set; }
        public string Fabricante { get; set; }
        public string Arquitectura { get; set; }
        public int CantidadNucleos { get; set; }
        public int CantidadProcesadores { get; set; }
        public double Velocidad { get; set; }
        public double Cache { get; set; }

        public override string ToString()
        {
            String salida = "Nombre: " + Nombre + "\n" +
                "Descripcion: " + Descripcion + "\n" +
                "Fabricante: " + Fabricante + "\n" +
                "Arquitectura: " + Arquitectura + "\n" +
                "CantidadNucleos: " + CantidadNucleos + "\n" +
                "CantidadProcesadores: " + CantidadProcesadores + "\n" +
                "Velocidad: " + Velocidad + "\n" +
                "Cache: " + CantidadNucleos
                ;
            return salida;
        }
    }
}
