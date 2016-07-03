using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace HardwareCollector.Conexion
{


    public class Comando
    {
        public const string caracterFinComando = "<EOF>";
        public string comando { get; set; }

        public Comando(string nombre) {
            this.comando = nombre;
        }

        public Parametro parametros { get; set; }
        public abstract class Parametro
        {
            public bool todos { get; set; }
            public string[] componentes { set; get; }
        }

        public virtual string GetJson() {
            return "";
        }

        public static Comando Construir(string json)
        {
            return null;
        }

    }
}