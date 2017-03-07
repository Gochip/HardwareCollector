using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Linq;
using System.ServiceProcess;
using System.Text;
using System.Threading.Tasks;
using System;
using System.Management;
using System.Web.Script.Serialization;
using HardwareCollector.Recoleccion;
using HardwareCollector.Componente;
using HardwareCollector.Conexion;
using HardwareCollector.Util;
using HardwareCollector.Principal;
using HardwareCollector.Excepciones;
using System.Net.Sockets;
using System.IO;
using System.Threading;

namespace HardwareCollectorService
{
    public partial class HardwareCollectorService : ServiceBase
    {
        private Controlador controlador;
        private Thread thread;

        public HardwareCollectorService()
        {
            InitializeComponent();
        }

        protected override void OnStart(string[] args)
        {
            controlador = new Controlador();
            try
            {
                thread = new Thread(new ThreadStart(controlador.Trabajar));
                thread.Start();
            }
            catch (Exception ex) {
                controlador.log(ex.Message);
            }
        }

        
        protected override void OnStop()
        {
            //limpiar recursos: thread, socket.
            controlador.Detener();
            controlador.Terminar();
        }

        /*
        protected override void OnContinue()
        {
            controlador = new Controlador("d:\\hc_logs.txt");
            try
            {
                controlador.Comenzar();
                controlador.Conectar();
                controlador.FaseInicial();
                thread = new Thread(new ThreadStart(controlador.FaseFuncionamiento));
                thread.Start();
            }
            catch (Exception ex)
            {
                controlador.log(ex.Message + ", " + ex.StackTrace);
            }
        }

        protected override void OnPause()
        {
            //pausar thread
            controlador.Detener();
            controlador.Terminar();
        }
        */

    }
}
