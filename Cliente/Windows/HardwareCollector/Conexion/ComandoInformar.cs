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
            datos = new Datos();
        }

        public class Datos
        {
            //opcional
            public string id_solicitud;
            public string id_informe;
            //es un array asociativo donde la clave es el nombre del componente y el valor un json de atributos y valores del componente
            public List<ElementoInformacion> informacion;
            public Datos()
            {
                informacion = new List<ElementoInformacion>();
            }
        }

        public abstract class ElementoInformacion {
            public string componente;
        }

        public abstract class DatosInformacion
        {
        }

        public class ElementoProcesador: ElementoInformacion
        {
            public ElementoProcesador() {
                componente = "procesador";
            }
            public DatosInformacion datos = new DatosInformacionProcesador();
        }

        public class ElementoMemoria : ElementoInformacion
        {
            public ElementoMemoria()
            {
                componente = "memorias_ram";
            }
            public List<DatosInformacionMemoriasRam> datos = new List<DatosInformacionMemoriasRam>();
        }

        public class ElementoDiscoDuro : ElementoInformacion
        {
            public ElementoDiscoDuro()
            {
                componente = "discos_duros";
            }
            public List<DatosInformacionDiscosDuros> datos = new List<DatosInformacionDiscosDuros>();
        }

        public class DatosInformacionProcesador : DatosInformacion {
            public string nombre;
            public string descripcion;
            public string fabricante;
            public string arquitectura;
            public int cantidad_nucleos;
            public int cantidad_procesadores;
            public string velocidad;
            public string tamanio_cache;
        }

        public class DatosInformacionDiscosDuros : DatosInformacion
        {
            public string fabricante;
            public string modelo;
            public string numero_serie;
            public string tipo_interfaz;
            public string firmware;
            public int cantidad_particiones;
            public string tamanio;
        }

        public class DatosInformacionMemoriasRam : DatosInformacion
        {
            public string banco;
            public string tecnologia;
            public string fabricante;
            public string numero_serie;
            public string tamanio_bus_datos;
            public string velocidad;
            public string tamanio;
        }
        
    }
}
