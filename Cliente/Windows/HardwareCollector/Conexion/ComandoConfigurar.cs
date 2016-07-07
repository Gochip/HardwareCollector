using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using HardwareCollector.Util;

namespace HardwareCollector.Conexion
{
    public class ComandoConfigurar : Comando
    {

        public Datos datos;
        public ComandoConfigurar() : base("configurar")
        {

        }

        public class Datos
        {
            public ArchivoConfiguracion configuracion;
        }
    }
}
