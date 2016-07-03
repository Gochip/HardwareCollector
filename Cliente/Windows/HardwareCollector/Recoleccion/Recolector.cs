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
            maquina.Procesador = GetProcesador();
            maquina.DiscosDuros = GetDiscosDuros();
            maquina.MemoriasRam = GetMemoriasRam();
            return maquina;
        }

        //https://msdn.microsoft.com/en-us/library/aa394373(v=vs.85).aspx
        public Procesador GetProcesador()
        {
            SelectQuery selectQuery = new SelectQuery("SELECT addresswidth, manufacturer, name, description, numberofcores, numberoflogicalprocessors, maxclockspeed, l2cachesize FROM Win32_Processor");
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(selectQuery);
            Procesador procesador = new Procesador();
            foreach (ManagementObject managementObject in searcher.Get())
            {
                procesador.Nombre = managementObject.GetPropertyValue("name").ToString();
                procesador.Descripcion = managementObject.GetPropertyValue("description").ToString();
                procesador.Fabricante = managementObject.GetPropertyValue("manufacturer").ToString();
                procesador.Arquitectura = managementObject.GetPropertyValue("addresswidth").ToString();
                procesador.CantidadNucleos = Int32.Parse(managementObject.GetPropertyValue("numberofcores").ToString());
                procesador.CantidadProcesadores = Int32.Parse(managementObject.GetPropertyValue("numberoflogicalprocessors").ToString());
                procesador.Velocidad = Double.Parse(managementObject.GetPropertyValue("maxclockspeed").ToString());
                procesador.Cache = Double.Parse(managementObject.GetPropertyValue("l2cachesize").ToString());
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
                discoDuro.Fabricante = managementObject.GetPropertyValue("manufacturer").ToString();
                discoDuro.Modelo = managementObject.GetPropertyValue("model").ToString();
                discoDuro.NumeroSerie = managementObject.GetPropertyValue("serialnumber").ToString();
                discoDuro.TipoInterfaz = managementObject.GetPropertyValue("interfacetype").ToString();
                discoDuro.Firmware = managementObject.GetPropertyValue("firmwarerevision").ToString();
                discoDuro.CantidadParticiones = int.Parse(managementObject.GetPropertyValue("partitions").ToString());
                discoDuro.Capacidad = Double.Parse(managementObject.GetPropertyValue("size").ToString());
                discos.Add(discoDuro);
            }
            return discos;
        }

        //https://msdn.microsoft.com/en-us/library/aa394347(v=vs.85).aspx
        public List<MemoriaRam> GetMemoriasRam()
        {
            SelectQuery selectQuery = new SelectQuery("SELECT banklabel, memorytype, manufacturer, serialnumber, datawidth, configuredclockspeed, capacity FROM Win32_PhysicalMemory");//diskdrive
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(selectQuery);
            List<MemoriaRam> memorias = new List<MemoriaRam>();
            foreach (ManagementObject managementObject in searcher.Get())
            {
                MemoriaRam memoria = new MemoriaRam();
                memoria.Banco = managementObject.GetPropertyValue("banklabel").ToString();
                memoria.Tecnologia = managementObject.GetPropertyValue("memorytype").ToString();
                memoria.Fabricante = managementObject.GetPropertyValue("manufacturer").ToString();
                memoria.NumeroSerie = managementObject.GetPropertyValue("serialnumber").ToString();
                memoria.TamanioBusDatos = managementObject.GetPropertyValue("datawidth").ToString();
                //configuredclockspeed puede dar 0 cuando no esta configurado
                memoria.Velocidad = Double.Parse(managementObject.GetPropertyValue("configuredclockspeed").ToString());
                memoria.Capacidad = Double.Parse(managementObject.GetPropertyValue("capacity").ToString());
                memorias.Add(memoria);
            }
            return memorias;
        }
    }
}
