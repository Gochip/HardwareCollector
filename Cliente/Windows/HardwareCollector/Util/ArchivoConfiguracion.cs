using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace HardwareCollector.Util
{
    public class ArchivoConfiguracion
    {

        //{
        //id: “id del cliente”,
        //configuracion: {
        //servidor: {
        //ip: "", 
        //puerto: int
        //}
        //informes: [
        //{
        //id: “id del informe, decidido por el cliente e informado al
        //servidor”,
        //informacion: [ “procesador”, “memorias_ram”,
        //“discos_duros”, “otro_componente…”],
        //tipo: “programado|inicio_sistema|inicio_sesion|apagado”,
        //hora: “hora del informe programado”
        //}
        //]
        //}
        //}

        public string id { get; set; }
        public Configuracion configuracion;

        public class Configuracion
        {
            public List<Informe> informes;
            public Servidor servidor;
        }

        public class Servidor {
            public string ip;
            public int puerto;
        }

        public class Informe
        {
            public int id;
            public List<string> informacion;
            public string tipo;
            public string hora;
        }

    }
}
