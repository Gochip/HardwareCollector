using System;
using System.Collections.Generic;
using System.Text;
using Microsoft.Deployment.WindowsInstaller;
using System.IO;

namespace HardwareCollectorCustomAction
{
    public class CustomActions
    {
        [CustomAction]
        public static ActionResult CustomActionCrearArchivoConfig(Session session)
        {
            session.Log("Begin CustomActionCrearArchivoConfig");
            try
            {
                FileStream file = File.Open("C:\\config_hc.json", FileMode.Create);
                StreamWriter fileWriter = new StreamWriter(file);
                fileWriter.WriteLine("{'configuracion':{'informes':null,'servidor':{'ip':'172.16.8.13','puerto':30330}}}");
                fileWriter.Close();
            }
            catch (Exception ex)
            {
                session.Log("ERROR in custom action CustomActionCrearArchivoConfig {0}", ex.ToString());
                return ActionResult.Failure;
            }
            return ActionResult.Success;
        }

        [CustomAction]
        public static ActionResult CustomActionBorrarArchivoConfig(Session session)
        {
            session.Log("Begin CustomActionBorrarArchivoConfig");
            try
            {
                File.Delete("C:\\config_hc.json");
            }
            catch (Exception ex)
            {
                session.Log("ERROR in custom action CustomActionBorrarArchivoConfig {0}", ex.ToString());
                return ActionResult.Failure;
            }
            return ActionResult.Success;
        }
    }
}
