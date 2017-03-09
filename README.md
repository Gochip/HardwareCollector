# HardwareCollector

El HardwareCollector permite la recolección de datos de computadoras de un laboratorio informático. Está compuesto por un programa cliente y un servidor.

Se une con el proyecto ISAAI para mantener un histórico de los cambios en el hardware y software.

https://github.com/dsbarrionuevo/isaai

## Servidor de  Hardware Collector ##

Desarrollado en Python2.7 y se encuentra en el directorio Servidor/Python.

Para ejecutarlo (Linux Ubuntu):

1. Instalar mysql server con el comando apt-get install mysql-server.
2. Instalación del driver de mysql para Python (se necesita tener instalado pip):
  2.1. echo "https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-2.2.2.tar.gz" >> requirements.txt.
  2.2. sudo -H pip install -r ./requirements.txt.
  2.3. Para verificar que está instalado ejecutar pip list y en la lista debe aparecer: mysql-connector-python.
3. Ejecutar el script bd.sql que se encuntra en el directorio Servidor/bd.
3. Ejecutar python server.py en el directorio Servidor/Python. Esto levanta un servicio en el puerto 30330.

### Cambiar el puerto de escucha ###

Debe cambiar la constante DEFAULT_PORT definida en el archivo constants.py. Considerar que esto requiere que se actualice el puerto usado por los clientes.

## Cliente Windows ##

Desarrollado en Visual Studio Community 2015 Version 14.0.25123.00 Update 2 y Microsoft .NET Framework Version 4.6.01586.

La solución consta de 4 proyectos:
* HardwareCollector: Modelo de datos y controlador principal del cliente.
* HardwareCollectorService: Servicio que inicia el controlador principal en un hilo aparte. Depende del anterior.
* HardwareCollectorCustomAction: Crea el archivo config_hc.json en el disco "C:" al instalarse y lo elimina al desintalarse. Es independiente.
* HardwareCollectorInstaller: Crea el instalador del programa y del servicio. Depende de los 3 proyectos anteriores.

### Requerimientos ###

* Windows 7 o posterior (WMI no viene incluido en Windows XP ni Vista)
* .NET Framework instalado (versión 4.0 en adelante)

### Cómo instalarlo ###

Por ahora, los parámetros de configuración de cada máquina cliente se pueden modificar en el método "CustomActionCrearArchivoConfig" de la clase HardwareCollectorCustomAction.CustomActions. Es necesario modificar la IP y puerto usados por el servidor. En el futuro éstos deben ser seteados durante la instalación. La clase HardwareCollector.Util.ControladorArchivoConfiguracion posee hardcodeada la ubicación del archivo de configuración donde buscará la información para que el cliente funcione.

Al ejecutar el instalador se crea el programa HardwareCollector.exe y HardwareCollectorService.exe en "Program Files\Labsis\HardwareCollectorService". El primero es solo para ejecutar la consola pero no tiene utilidad. El segundo representa el servicio que se instala e inicia al finalizar el instalador.

Además, al instalar el servicio se crea el archivo "config_hc.json" en "C:\\" con la IP y puerto del servidor, por lo que es necesario ejecutar el instalador con persmisos de escritura en ese disco.

El servicio se llama "HardwareCollectorService" y puede ser consultador con el programa services.msc. Posee la siguiente configuración: cuenta de usuario "LocalSystem" (tiene los privilegios más alto de sistema) y se programó para iniciar "Automatic", es decir se pone en funcionamiento con el inicio del sistema. 

Caulquier error durante la instalación o desinstalación puede ser consultada ingresando en "Visor de envetos>Registro de Windows>Aplicación".




