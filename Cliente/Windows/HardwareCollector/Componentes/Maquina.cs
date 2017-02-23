using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace HardwareCollector.Componente
{
    public class Maquina
    {
        public string Nombre { get; set; }
        public SistemaOperativo SistemaOperativo { get; set; }
        public Procesador Procesador { get; set; }
        public List<DiscoDuro> DiscosDuros { get; set; }
        public List<MemoriaRam> MemoriasRam { get; set; }
    }
}
