using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Web.Script.Serialization;

namespace HardwareCollector.Conexion
{

    public abstract class Comando
    {
        public const string caracterFinComando = "<EOF>";
        public string comando { get; set; }

        public Comando(string nombre)
        {
            this.comando = nombre;
        }

        public virtual string Serialize()
        {
            return new JavaScriptSerializer().Serialize(this);
        }

        public virtual Comando Deserialize(string json) {
            return null;
        }
        

    }
}