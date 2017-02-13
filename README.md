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

Debe cambiar la constante DEFAULT_PORT definida en el archivo constants.py.
