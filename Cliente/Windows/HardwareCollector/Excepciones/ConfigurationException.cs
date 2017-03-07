using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace HardwareCollector.Excepciones
{
    public class ConfigurationException : Exception
    {
        public ConfigurationException()
        {
        }

        public ConfigurationException(string message) : base(message)
        {
        }


    }
}
