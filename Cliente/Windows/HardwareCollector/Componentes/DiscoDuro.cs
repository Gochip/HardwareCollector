
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace HardwareCollector.Componente
{
    public class DiscoDuro
    {

        //public String Fabricante { get; set; }//Manufacturer
        //public String Modelo { get; set; }//Model
        //public String NumeroSerie { get; set; }//SerialNumber
        //public String TipoInterfaz { get; set; }//InterfaceType (SCSI , PCI, IDE)
        //public String Firmware { get; set; }//FirmwareRevision?
        //public int CantidadParticiones { get; set; }//Partitions
        //public double Capacidad { get; set; }//kBytes
        //DefaultBlockSize (bytes)
        //InstallDate
        //MediaType: si es externo, fijo o removible..
        //Name

        public String Fabricante { get; set; }
        public String Modelo { get; set; }
        public String NumeroSerie { get; set; }
        public String TipoInterfaz { get; set; }//(SCSI , PCI, IDE)
        public String Firmware { get; set; }
        public int CantidadParticiones { get; set; }
        public double Capacidad { get; set; }//kBytes
        
        public override string ToString()
        {
            String salida = "Fabricante: " + Fabricante + "\n" +
                "Modelo: " + Modelo + "\n" +
                "NumeroSerie: " + NumeroSerie + "\n" +
                "TipoInterfaz: " + TipoInterfaz + "\n" +
                "Firmware: " + Firmware + "\n" +
                "CantidadParticiones: " + CantidadParticiones + "\n" +
                "Capacidad: " + Capacidad
                ;
            return salida;
        }

    }
}
