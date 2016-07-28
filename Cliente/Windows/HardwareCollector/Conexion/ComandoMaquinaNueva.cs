using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Web.Script.Serialization;

namespace HardwareCollector.Conexion
{
    class ComandoMaquinaNueva: Comando
    {
        public ComandoMaquinaNueva() : base("maquina_nueva") {

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
