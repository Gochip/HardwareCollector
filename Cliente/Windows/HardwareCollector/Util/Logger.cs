using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace HardwareCollector.Util
{
    public class Logger
    {
        private StreamWriter writer;
        private string pathfile;

        public Logger(string pathfile) {
            this.pathfile = pathfile;
        }

        public void openFile(FileMode mode)
        {
            FileStream file = File.Open(this.pathfile, mode);
            writer = new StreamWriter(file);
        }

        public void writeLine(string line)
        {
            writer.WriteLine(line);
        }

        public void close() {
            writer.Close();
        }
    }


}
