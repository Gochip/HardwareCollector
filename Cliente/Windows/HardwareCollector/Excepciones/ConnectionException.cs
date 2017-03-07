using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace HardwareCollector.Excepciones
{
    public class ConnectionException : Exception
    {
        public ConnectionException()
        {
        }

        public ConnectionException(string message) : base(message)
        {
        }

    }
}
