using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace HardwareCollector.Componente
{

    public class MemoriaRam
    {

        /*private String banco;//banklabel
        private String tecnologia; //memorytype?
        private String fabricante;//manufacturer
        private String numeroSerie;//serialnumber
        private String tamanioBusDatos; //datawidth
        private double velocidad;//nanosegundos//speed
                                 //ConfiguredClockSpeed;//MHz (0 si no esta configurado)
                                 //Description
                                 //DeviceLocator
                                 //InstallDate
                                 //MemoryType
                                 //Model
                                 //Name
                                 //Status
        private double capacidad;//bytes , capacity*/

        public String Banco { get; set; }
        public String Tecnologia { get; set; }
        public String Fabricante { get; set; }
        public String NumeroSerie { get; set; }
        public String TamanioBusDatos { get; set; }
        public double Velocidad { get; set; }
        public double Capacidad { get; set; }

        public override string ToString()
        {
            String salida = "Banco: " + Banco + "\n" +
                "Tecnologia: " + Tecnologia + "\n" +
                "Fabricante: " + Fabricante + "\n" +
                "TamanioBusDatos: " + TamanioBusDatos + "\n" +
                "Velocidad: " + Velocidad + "\n" +
                "Capacidad: " + Capacidad
                ;
            return salida;
        }

    }
}
