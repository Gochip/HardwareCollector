using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Management;
using HardwareCollector.Componente;

namespace HardwareCollector.Recoleccion
{
    public class Recolector
    {
        public Maquina GetMaquina()
        {
            Maquina maquina = new Maquina();
            maquina.Nombre = GetNombreMaquina();
            maquina.SistemaOperativo = GetSistemaOperativo();
            maquina.Procesador = GetProcesador();
            maquina.DiscosDuros = GetDiscosDuros();
            maquina.MemoriasRam = GetMemoriasRam();
            return maquina;
        }

        public SistemaOperativo GetSistemaOperativo() {
            SistemaOperativo sistemaOperativo = new SistemaOperativo();
            SelectQuery selectQuery = new SelectQuery("SELECT caption, version FROM Win32_OperatingSystem");
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(selectQuery);
            foreach (ManagementObject managementObject in searcher.Get())
            {
                sistemaOperativo.Nombre = ReadPropertyValueSafely(managementObject, "caption");
                sistemaOperativo.Version = ReadPropertyValueSafely(managementObject, "version");
            }
            return sistemaOperativo;
        }

        public string GetNombreMaquina()
        {
            string nombre = "";
            SelectQuery selectQuery = new SelectQuery("SELECT csname FROM Win32_OperatingSystem");
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(selectQuery);
            foreach (ManagementObject managementObject in searcher.Get())
            {
                nombre = ReadPropertyValueSafely(managementObject, "csname");
            }
            return nombre;
        }

        //https://msdn.microsoft.com/en-us/library/aa394373(v=vs.85).aspx
        public Procesador GetProcesador()
        {
            SelectQuery selectQuery = new SelectQuery("SELECT addresswidth, manufacturer, name, description, numberofcores, numberoflogicalprocessors, maxclockspeed, l2cachesize FROM Win32_Processor");
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(selectQuery);
            Procesador procesador = new Procesador();
            foreach (ManagementObject managementObject in searcher.Get())
            {
                procesador.Nombre = ReadPropertyValueSafely(managementObject, "name");
                procesador.Descripcion = ReadPropertyValueSafely(managementObject, "description");
                procesador.Fabricante = ReadPropertyValueSafely(managementObject, "manufacturer");
                procesador.Arquitectura = ReadPropertyValueSafely(managementObject, "addresswidth");
                int numberofcores = 0;
                if (Int32.TryParse(ReadPropertyValueSafely(managementObject, "numberofcores"), out numberofcores)) { }
                procesador.CantidadNucleos = numberofcores;
                int numberoflogicalprocessors = 0;
                if (Int32.TryParse(ReadPropertyValueSafely(managementObject, "numberoflogicalprocessors"), out numberofcores)) { }
                procesador.CantidadProcesadores = numberoflogicalprocessors;
                double maxclockspeed = 0;
                if (Double.TryParse(ReadPropertyValueSafely(managementObject, "maxclockspeed"), out maxclockspeed)) { }
                procesador.Velocidad = maxclockspeed;
                double l2cachesize = 0;
                if (Double.TryParse(ReadPropertyValueSafely(managementObject, "l2cachesize"), out l2cachesize)) { }
                procesador.Cache = l2cachesize;
            }
            return procesador;
        }

        //https://msdn.microsoft.com/en-us/library/aa394132(v=vs.85).aspx
        public List<DiscoDuro> GetDiscosDuros()
        {
            SelectQuery selectQuery = new SelectQuery("SELECT manufacturer, model, size, serialnumber, firmwarerevision, interfacetype, partitions FROM Win32_DiskDrive");//diskdrive
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(selectQuery);
            List<DiscoDuro> discos = new List<DiscoDuro>();
            foreach (ManagementObject managementObject in searcher.Get())
            {
                DiscoDuro discoDuro = new DiscoDuro();
                discoDuro.Fabricante = ReadPropertyValueSafely(managementObject, "manufacturer");
                discoDuro.Modelo = ReadPropertyValueSafely(managementObject, "model");
                discoDuro.NumeroSerie = ReadPropertyValueSafely(managementObject, "serialnumber");
                discoDuro.TipoInterfaz = ReadPropertyValueSafely(managementObject, "interfacetype");
                discoDuro.Firmware = ReadPropertyValueSafely(managementObject, "firmwarerevision");
                int partitions = 0;
                if (Int32.TryParse(ReadPropertyValueSafely(managementObject, "partitions"), out partitions)) { }
                discoDuro.CantidadParticiones = partitions;
                double size = 0;
                if (Double.TryParse(ReadPropertyValueSafely(managementObject, "size"), out size)) { }
                discoDuro.Capacidad = size;
                discos.Add(discoDuro);
            }
            return discos;
        }

        //https://msdn.microsoft.com/en-us/library/aa394347(v=vs.85).aspx
        public List<MemoriaRam> GetMemoriasRam()
        {
            SelectQuery selectQuery = new SelectQuery("SELECT banklabel, memorytype, manufacturer, serialnumber, datawidth, speed, capacity FROM Win32_PhysicalMemory");//diskdrive
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(selectQuery);
            List<MemoriaRam> memorias = new List<MemoriaRam>();
            foreach (ManagementObject managementObject in searcher.Get())
            {
                MemoriaRam memoria = new MemoriaRam();
                memoria.Banco = ReadPropertyValueSafely(managementObject, "banklabel");
                memoria.Tecnologia = ReadPropertyValueSafely(managementObject, "memorytype");
                memoria.Fabricante = ReadPropertyValueSafely(managementObject, "manufacturer");
                memoria.NumeroSerie = ReadPropertyValueSafely(managementObject, "serialnumber");
                memoria.TamanioBusDatos = ReadPropertyValueSafely(managementObject, "datawidth");
                //configuredclockspeed fue cambiado a speed porque versiones anteriores de windows 10 no lo soportan: 
                double speed = 0;
                if (Double.TryParse(ReadPropertyValueSafely(managementObject, "speed"), out speed)) { }
                memoria.Velocidad = speed;
                double capacity = 0;
                if (Double.TryParse(ReadPropertyValueSafely(managementObject, "capacity"), out capacity)) { }
                memoria.Capacidad = capacity;
                memorias.Add(memoria);
            }
            return memorias;
        }

        private string ReadPropertyValueSafely(ManagementObject managementObject, string propertyName) {
            string resultado = "";
            if (managementObject.GetPropertyValue(propertyName) != null)
            {
                resultado = managementObject.GetPropertyValue(propertyName).ToString();
            }
            return resultado;
        }

    }
}
