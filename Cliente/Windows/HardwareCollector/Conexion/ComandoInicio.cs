using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Web.Script.Serialization;

namespace HardwareCollector.Conexion
{
    public class ComandoInicio:Comando
    {
        public Datos datos;
        public ComandoInicio() : base("inicio") {
            datos = new Datos();
        }

        public class Datos
        {
            public string id;
            public Datos()
            {
                id = "-1";
            }
        }
    }
}
