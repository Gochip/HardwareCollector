using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Web.Script.Serialization;
using HardwareCollector.Componente;

namespace HardwareCollector.Conexion
{

    public class ComandoInformar:Comando
    {

        public Datos datos;
        public ComandoInformar() : base("informar") {

        }

        public class Datos
        {
            //opcional
            public string id_solicitud;
            //es un array asociativo donde la clave es el nombre del componente y el valor un json de atributos y valores del componente
            public List<ElementoInformacion> informacion;
        }

        public class ElementoInformacion {
            //nombre del componente
            public string clave;
            //json cuyas propiedades son los nombres de los atributos del componente y valor es el valor de tal atributo
            public List<DatosInformacion> datos;
        }

        public class DatosInformacion {
            //es el nombre del atributo del componente
            public string clave;
            //es el valor para ese atributo del componente
            public object valor;
        }

        public class ElementoProcesador: ElementoInformacion
        {
            public ElementoProcesador() {
                clave = "procesador";
                datos.Add(new DatosInformacion() { clave = "nombre", valor = "" });
                datos.Add(new DatosInformacion() { clave = "descripcion", valor = "" });
                datos.Add(new DatosInformacion() { clave = "fabricante", valor = "" });
                datos.Add(new DatosInformacion() { clave = "arquitectura", valor = "" });
                datos.Add(new DatosInformacion() { clave = "cantidad_nucleos", valor = -1 });
                datos.Add(new DatosInformacion() { clave = "cantidad_procesador", valor = -1 });
                datos.Add(new DatosInformacion() { clave = "velocidad", valor = -1 });
                datos.Add(new DatosInformacion() { clave = "tamanio_cache", valor = -1 });
            }
        }

        /*
        public ComandoInformar(Maquina maquina, int informe, int reporte):base("informar") {
            this.datos = new DatoComandoInformar()
            {
                procesador = Maquina.Procesador,
                discos_duros = Maquina.DiscosDuros.ToArray(),
                memorias_ram = Maquina.MemoriasRam.ToArray(),
            };
        }

        public Maquina Maquina { set; get; }

        public class ParametroComandoInformar: Parametro
        {
            public int id_informe { get; set; }
            public bool respuesta { get; set; }
            public int id_reporte { get; set; }
        }

        public DatoComandoInformar datos { get; set; }
        public class DatoComandoInformar {
            public Procesador procesador { get; set; }
            public DiscoDuro[] discos_duros{ get; set; }
            public MemoriaRam[] memorias_ram { get; set; }
        }

        public override string GetJson() {
            Comando json = new Comando
            {
                comando = "informar",
                parametros = new ParametroComandoInformar {
                        todos = true,
                        id_informe = 1
                }
            };
            return new JavaScriptSerializer().Serialize(null);
        }
    */
    }
}
