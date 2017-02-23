using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Web.Script.Serialization;

namespace HardwareCollector.Conexion
{
    public class ComandoMaquinaNueva: Comando
    {
        public Datos datos;
        public ComandoMaquinaNueva() : base("maquina_nueva") {
            datos = new Datos();
        }

        public class Datos
        {
            public string nombre_maquina;
            public SistemaOperativo sistema_operativo;
            public Datos()
            {
                nombre_maquina = "";
                sistema_operativo = new SistemaOperativo();
            }
        }

        public class SistemaOperativo {
            public string nombre;
            public string version;
            public SistemaOperativo() {
                nombre = "";
                version = "";
            }
        }

        public override string Serialize()
        {
            return new JavaScriptSerializer().Serialize(this);
        }

        public override Comando Deserialize(string json)
        {
            //return (ComandoMaquinaNueva)new JavaScriptSerializer().Deserialize(json, this.GetType());
            return (Comando)new JavaScriptSerializer().Deserialize(json, this.GetType());
        }
        
    }
}
