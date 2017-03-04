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
        public static ActionResult CustomActionCrearArchiveConfig(Session session)
        {
            session.Log("Begin CustomActionCrearArchiveConfig");
            try
            {
                StreamWriter file = new StreamWriter("c:\\config_hc.json");
                file.WriteLine("{'configuracion':{'informes':null,'servidor':{'ip':'192.168.27.101','puerto':30330}}}");
                file.Close();
            }
            catch (Exception ex)
            {
                session.Log("ERROR in custom action CustomActionCrearArchiveConfig {0}", ex.ToString());
                return ActionResult.Failure;
            }
            return ActionResult.Success;
        }
    }
}
