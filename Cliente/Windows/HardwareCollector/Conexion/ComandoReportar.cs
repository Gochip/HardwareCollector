using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Web.Script.Serialization;

namespace HardwareCollector.Conexion
{

    public class ComandoReportar : Comando
    {
        public class ParametroComandoReportar : Parametro
        {
            public int id_reporte { get; set; }
        }

        public override string GetJson()
        {
            Comando json = new Comando
            {
                comando = "reportar",
                parametros = new ParametroComandoReportar
                {
                    todos = true,
                    id_reporte = 1
                }
            };
            return new JavaScriptSerializer().Serialize(json);
        }
    }
}
