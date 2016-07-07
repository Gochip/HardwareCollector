using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Web.Script.Serialization;

namespace HardwareCollector.Conexion
{
    public class ComandoSolicitar: Comando
    {

        public Datos datos;
        public ComandoSolicitar() : base("solicitar") {

        }
        public class Datos
        {
            public string id_solicitud;
            public List<string> informacion;
        }
    }
}
