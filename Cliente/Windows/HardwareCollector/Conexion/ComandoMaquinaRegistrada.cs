using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Web.Script.Serialization;

namespace HardwareCollector.Conexion
{
    public class ComandoMaquinaRegistrada: Comando
    {
        public Datos datos;
        public ComandoMaquinaRegistrada() : base("maquina_registrada") {

        }

        public class Datos {
            public string id;
        }

        public static ComandoMaquinaRegistrada Deserealizar(string json) {
            return new JavaScriptSerializer().Deserialize<ComandoMaquinaRegistrada>(json);
        }
    }
}
