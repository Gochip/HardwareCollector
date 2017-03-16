# encoding: utf-8

"""

Escucho por el puerto: 31415

Comandos disponibles:

obtener_hash (id_desafio) : hash
guardar_respuesta (id_desafio, hash, id_grupo) : booleano


"""

import socket
import os
import os.path
import mysql.connector
import json
import time
import random
from constants import *
from subprocess import PIPE, Popen


class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket):
        self.socket = socket
        self.closed = False
        self.output = ""
        self.input = ""
        self.user = "root"
        self.password = "toor"
        self.db = "hc_bd"
        self.id_maquina = None
        self.solicitudes = []

    def get_fileno(self):
        """
        Retorna el file descriptor del socket.
        """
        return self.socket.fileno()

    def is_closed(self):
        return self.closed

    def handle_input(self):
        """
        Maneja la entrada para este cliente.
        Guarda los datos en un búfer de entrada.

        Retorna True si se pudo recibir algo, False en caso contrario.
        """
        data = self.socket.recv(4096)
        if len(data) > 0:
            self.input += data
            # Si recibimos un EOL actuamos
            while EOL in self.input:
                (command, self.input) = self.input.split(EOL, 1)
                if '\n' in command:
                    self.add_command_status(BAD_EOL)
                    break
                print ("Command:", command[:50])
                command_status = self.execute(command)
                print ("Command status:", command_status)
            return True
        else:
            return False

    def handle_output(self):
        """
        Maneja la salida para este cliente.
        Envía los datos guardados en un búfer de salida.

        Retorna True si se pudo enviar algo, False en caso que el búfer de
        salida está vacío.
        """
        return self.send()

    def events(self):
        """
        Devuelve los eventos (POLLIN, POLLOUT) que le interesan
        a la conexión en este momento
        """
        return True

    def add_command_status(self, status):
        """
        Agrega el estado del comando al búfer de salida.
        """
        self.output += str(status) + EOL

    def send(self):
        """
        Envía el contenido en el búfer de salida.
        """
        if self.output != "":
            sent = self.socket.send(self.output)
            if sent == 0:
                return False
            self.output = self.output[sent:]
            return True
        else:
            return False

    def execute(self, command):
        """
        Valida y ejecuta un comando.
        Llena el búfer de salida con la respuesta.
        Retorna el código de estado.
        """
        command_status = COMANDO_INVALIDO
        if True:
        #try:
            json_comando = json.loads(command)
            resultado = None
            comando = json_comando["comando"]
            print ("nombre de comando: " + comando)
            if comando == MAQUINA_NUEVA:
                datos = json_comando["datos"]
                if datos is not None:
                    resultado = {}
                    nombre_maquina = datos["nombre_maquina"]
                    nombre_sistema_operativo = datos["sistema_operativo"]["nombre"]
                    version_sistema_operativo = datos["sistema_operativo"]["version"]
                    id_maquina = self.maquina_nueva(nombre_maquina, nombre_sistema_operativo, version_sistema_operativo)
                    resultado["comando"] = MAQUINA_REGISTRADA
                    resultado["datos"] = {"id": id_maquina}
                    self.id_maquina = id_maquina
                    print("MAQUINA REGISTRADA")
                    command_status = OK
                else:
                    command_status = ERROR
            elif comando == INICIO:
                datos = json_comando["datos"]
                if datos is not None:
                    id_maquina = datos["id"]
                    resultado = {}
                    respuesta = self.inicio(id_maquina)
                    resultado["comando"] = CONFIGURAR
                    resultado["datos"] = {"configuracion": respuesta}
                    print("MAQUINA INICIADA")
                    
                    # Ejemplo de solicitud de datos tras recibir un comando inicio
                    '''
                    self.id_maquina = datos["id"]
                    resultado = {}
                    resultado = self.solicitar(["procesador","discos_duros", "memorias_ram"])
                    print("SOLICITAR")
                    '''
                    command_status = OK
                else:
                    command_status = ERROR
            elif comando == INFORMAR:
                datos = json_comando["datos"]
                print(datos)
                if datos is not None:
                    try:
                        id_solicitud = datos["id_solicitud"]
                    except:
                        id_solicitud = None

                    try:
                        id_informe = datos["id_informe"]
                    except:
                        id_informe = None

                    modo = ""
                    if id_solicitud is not None:
                        modo = "activo"

                    if id_informe is not None:
                        modo = "pasivo"
                    print("modo: " + modo)
                    print(id_informe)
                    try:
                        informacion = datos["informacion"]
                        self.informar(modo, id_solicitud, id_informe, informacion)
                        command_status = OK
                    except KeyError:
                        command_status = ERROR
        #except:
        #    print("Formato incorrecto de datos")
        self.output += json.dumps(resultado)
        return command_status

        # COMPLETAR
        
        # Validar comando.
        """command_parts = command.split()
        if len(command_parts) == 0:
            self.add_command_status(COMANDO_INVALIDO)
            return INVALID_COMMAND
        else:
            (command, arguments) = (command_parts[0], command_parts[1:])
        if not self.validate_command(command):
            self.add_command_status(COMANDO_INVALIDO)
            return COMANDO_INVALIDO

        command_status = COMANDO_INVALIDO
        buf = ""
        print command
        if command == OBTENER_HASH:
            if len(arguments) != 1:
                command_status = COMANDO_INVALIDO
            else:
                id_desafio = arguments[0]
                buf += self.get_hash(id_desafio) + EOL
                command_status = OK
        elif command == GUARDAR_RESPUESTA:
            if len(arguments) != 3:
                command_status = COMANDO_INVALIDO
            else:
                id_desafio = arguments[0]
                hash = arguments[1]
                id_grupo = arguments[2]
                buf += self.save_response(id_desafio, hash, id_grupo) + EOL
                command_status = OK
        elif command == SALIR:
            if len(arguments) > 0:
                command_status = COMANDO_INVALIDO
            else:
                self.closed = True
                command_status = OK

        self.add_command_status(command_status)
        self.output += buf

        return command_status"""

    def close(self):
        self.socket.close()

    # PRIVADOS

    def get_tipo_informe(self, nombre_informe):
        cnx = mysql.connector.connect(user=self.user, password=self.password, database=self.db)
        cursor = cnx.cursor()
        consulta = ("SELECT id FROM tipos_informes WHERE nombre=%s")

        cursor.execute(consulta, (nombre_informe, ))
        id_tipo_informe = None
        for (id_tipo) in cursor:
            id_tipo_informe = id_tipo[0]
        return id_tipo_informe

    def get_ids_componentes(self):
        cnx = mysql.connector.connect(user=self.user, password=self.password, database=self.db)
        cursor = cnx.cursor()
        consulta = ("SELECT id FROM componentes")

        cursor.execute(consulta)
        ids = []
        for (id_componente) in cursor:
            ids.append(id_componente[0])
        return ids

    def get_componentes_informe(self, id_informe):
        """
            Retorna la configuración de un informe
        """
        cnx = mysql.connector.connect(user=self.user, password=self.password, database=self.db)
        cursor = cnx.cursor()
        consulta = """SELECT c.nombre
                    FROM componentes_x_informe AS cxi
                    INNER JOIN componentes AS c ON (c.id = cxi.id_componente)
                    WHERE cxi.id_informe=%s"""

        componentes = []
        cursor.execute(consulta, (id_informe, ))
        for (nombre) in cursor:
            componentes.append(nombre[0])
        return componentes

    def get_tipos_informes(self, id_informe):
        """
            Retorna una tupla con el tipo de informe
        """
        """cnx = mysql.connector.connect(user=self.user, password=self.password, database=self.db)
        cursor = cnx.cursor()
        consulta = "SELECT id FROM informes AS i INNER JOIN tipos_informes WHERE id_maquina=%d"
        cursor.execute(consulta, id_maquina)
        informes = []
        for (id_informe) in cursor:
            informes.append(id_informe)
        return informes"""
        pass

    def get_informes(self, id_maquina):
        """
            Retorna todos los id de informes para una máquina dada
        """
        cnx = mysql.connector.connect(user=self.user, password=self.password, database=self.db)
        cursor = cnx.cursor()
        consulta = """SELECT ixm.id_informe FROM maquinas AS m
                    INNER JOIN informes_x_maquina AS ixm ON (m.id = ixm.id_maquina)
                    WHERE m.id=%s"""
        cursor.execute(consulta, (id_maquina, ))
        informes = []
        for (id_informe) in cursor:
            informes.append(id_informe[0])
        return informes

    def get_id_caracteristica_x_componente(self, id_componente, nombre_caracteristica):
        cnx = mysql.connector.connect(user=self.user, password=self.password, database=self.db)
        cursor = cnx.cursor()
        consulta = """
                    SELECT cxc.id FROM caracteristicas_x_componentes AS cxc
                    WHERE cxc.id_componente=%s AND cxc.nombre=%s
                   """
        cursor.execute(consulta, (id_componente, nombre_caracteristica))
        id_caracteristica = None
        for (caract) in cursor:
            id_caracteristica = caract[0]
        return id_caracteristica

    def get_id_componente(self, nombre_componente):
        cnx = mysql.connector.connect(user=self.user, password=self.password, database=self.db)
        cursor = cnx.cursor()
        consulta = """
                    SELECT c.id FROM componentes AS c
                    WHERE c.nombre=%s
                   """
        cursor.execute(consulta, (nombre_componente, ))
        id_componente = None
        for (comp) in cursor:
            id_componente = comp[0]
        return id_componente

    def actualizar_fecha_sincronizacion(self, id_maquina):
        cnx = mysql.connector.connect(user=self.user, password=self.password, database=self.db)
        cursor = cnx.cursor()
        actualizacion = """
                        UPDATE maquinas SET fecha_sincronizacion=NOW() WHERE id=%s
                       """
        cursor.execute(actualizacion, (id_maquina,))
        cnx.commit()

    # COMANDOS DE SALIDA

    def solicitar(self, informacion_a_solicitar):
        solicitud = Solicitud()
        solicitud.informacion = informacion_a_solicitar
        self.solicitudes.append(solicitud)

        comando = {}
        comando["comando"] = SOLICITAR
        comando["datos"] = {}
        comando["datos"]["id_solicitud"] = solicitud.get_id()
        comando["datos"]["informacion"] = informacion_a_solicitar
        return comando

    # COMANDOS DE ENTRADA

    def maquina_nueva(self, nombre_maquina, nombre_sistema_operativo, version_sistema_operativo):
        """
            Método que ejecuta el comando MAQUINA_NUEVA.
            Retorna el ID de máquina creada.
        """
        cnx = mysql.connector.connect(user=self.user, password=self.password, database=self.db)
        cursor = cnx.cursor()

        insercion = ("INSERT INTO maquinas "
                    "(nombre_maquina, nombre_sistema_operativo, version_sistema_operativo, fecha_alta, fecha_sincronizacion) VALUES "
                    "(%s, %s, %s, NOW(), NOW())")
        cursor.execute(insercion, (nombre_maquina, nombre_sistema_operativo, version_sistema_operativo))
        id_maquina_insertado = cursor.lastrowid

        id_tipo_informe_inicio_sistema = self.get_tipo_informe('inicio_sistema')

        insercion1 = ("INSERT INTO informes_x_maquina "
                     "(id_maquina, id_tipo_informe) "
                     "VALUES (%s, %s)")
        cursor.execute(insercion1, (id_maquina_insertado, id_tipo_informe_inicio_sistema))
        id_informe_insertado = cursor.lastrowid

        # Agregar for componentes
        ids_componentes = self.get_ids_componentes()
        for id_componente in ids_componentes:
            insercion = ("INSERT INTO componentes_x_informe "
                         "(id_maquina, id_informe, id_componente) "
                         "VALUES (%s, %s, %s)")
            cursor.execute(insercion, (id_maquina_insertado, id_informe_insertado, id_componente))

        cnx.commit()
        cursor.close()
        cnx.close()        
        return id_maquina_insertado

    def inicio(self, id_maquina):
        """
            Método que ejecuta el comando INICIO.
        """
        resultado = {}
        if self.id_maquina is not None:
            id_maquina = self.id_maquina
        if self.id_maquina is None:
            self.id_maquina = id_maquina

        if id_maquina is not None:
            resultado["id"] = id_maquina
            configuracion = {}
            informes = self.get_informes(id_maquina)
            configuracion["informes"] = []
            for id_informe in informes:
                componentes = self.get_componentes_informe(id_informe)
                informe = {}
                informe["id"] = id_informe
                informe["informacion"] = componentes
                informe["tipo"] = 'inicio_sistema'
                #if tipo == "programado":
                #    informe["hora"] = "12:00"
                configuracion["informes"].append(informe)
            resultado["configuracion"] = configuracion
        return resultado

    def informar(self, modo, id_solicitud = None, id_informe = None, informacion = []):
        # Siempre debo actualizar la columna "fecha_sincronizacion" de la tabla maquinas.
        # Falta considerar los id de informe y solicitud...
        # Modo pasivo: verificar que el id de informe sea el adecuado
        # respecto a la información recibida.
        if ((modo == "activo" and id_solicitud is not None) or True):
            # Modo activo: verificar que el id de solicitud esté en el bufer de solicitudes.
            print ("ID SOLICITUD: ")
            print (id_solicitud)
            print ("ID INFORME: ")
            print (id_informe)
            print ("INFORMACIÓN: ")
            print (informacion)
            cnx = mysql.connector.connect(user=self.user, password=self.password, database=self.db)
            cursor = cnx.cursor()
            for info in informacion:
                componente = info["componente"]
                id_componente = self.get_id_componente(componente)

                borrado_componentes_x_maquinas = ("DELETE FROM componentes_x_maquinas WHERE id_maquina=%s AND id_componente=%s")
                cursor.execute(borrado_componentes_x_maquinas, (self.id_maquina, id_componente))

                borrado_caracteristicas_x_componentes_x_maquinas = ("DELETE FROM caracteristicas_x_componentes_x_maquinas WHERE id_maquina=%s AND id_componente=%s")
                cursor.execute(borrado_caracteristicas_x_componentes_x_maquinas, (self.id_maquina, id_componente))

                if componente == "procesador":
                    # Elimino todos los procesador de una maquina.
                    datos = info["datos"]
                    
                    # 1) Verifico si existe el componente en la tabla "componentes_x_maquinas" dados 
                    # el id_componente y el self.id_maquina
                    # 1.1) Si existe no inserto nada en "componentes_x_maquinas" pero 
                    # actualizo "caracteristicas_x_componentes_x_maquinas" con los valores recibidos del procesador y 
                    # con (id_componente, id_maquina, id_caracteristica, 1, valor), uso 1 como posicion.

                    # 1.2) Si no existe, inserto en "componentes_x_maquinas" y tambien en "caracteristicas_x_componentes_x_maquinas"
                    # con los valores recibidos y con (id_componente, id_maquina, id_caracteristica, 1, valor), uso 1 como posicion.

                    insercion = ("INSERT INTO componentes_x_maquinas "
                         "(id_componente, id_maquina, posicion) "
                         "VALUES (%s, %s, %s)")
                    # Columna posicion se usa para distinguir entre muchos componentes de la misma maquina del mismo tipo (como ser memorias ram)
                    cursor.execute(insercion, (id_componente, self.id_maquina, 1))
                    cnx.commit()
                    for clave, valor in datos.items():
                        nombre_caracteristica = clave
                        valor_caracteristica = valor
                        id_caracteristica = self.get_id_caracteristica_x_componente(id_componente, nombre_caracteristica)

                        insercion = ("INSERT INTO caracteristicas_x_componentes_x_maquinas "
                                "(id_componente, id_maquina, id_caracteristica, posicion, valor) "
                                "VALUES (%s, %s, %s, %s, %s)")
                        cursor.execute(insercion, (id_componente, self.id_maquina, id_caracteristica, 1, valor_caracteristica))
                        cnx.commit()
                    self.actualizar_fecha_sincronizacion(self.id_maquina)
                elif componente == "discos_duros" or componente == "memorias_ram":
                    # Pseudocodigo:
                    # El procedimiento es igual al caso del procesador, solo que debo considerar que en
                    # datos es un arreglo indexado de arreglos asociativos, como ser
                    # datos = [{clave:valor},{clave:valor}]
                    datos = info["datos"]
                    posicion = 1
                    for dato in datos:
                        insercion = ("INSERT INTO componentes_x_maquinas "
                             "(id_componente, id_maquina, posicion) "
                             "VALUES (%s, %s, %s)")
                        cursor.execute(insercion, (id_componente, self.id_maquina, posicion))
                        cnx.commit()
                        for clave, valor in dato.items():
                            nombre_caracteristica = clave
                            valor_caracteristica = valor
                            id_caracteristica = self.get_id_caracteristica_x_componente(id_componente, nombre_caracteristica)

                            insercion = ("INSERT INTO caracteristicas_x_componentes_x_maquinas "
                                    "(id_componente, id_maquina, id_caracteristica, posicion, valor) "
                                    "VALUES (%s, %s, %s, %s, %s)")
                            cursor.execute(insercion, (id_componente, self.id_maquina, id_caracteristica, posicion, valor_caracteristica))
                            cnx.commit()
                        posicion += 1
        else:
            pass

class Solicitud():

    def __init__(self):
        # Genera un id único, tiene en cuenta un número aleatorio (deberia tener en cuenta tambien el timepo). Es necesario ponerse de acuerdo y usar strings en todo los ins informe y solicitud.
        self._id = random.randint(1, 10000)
        self.informacion = []

    def get_id(self):
        return self._id


if __name__ == "__main__":
    con = Connection(None)
    #con.maquina_nueva()
    dic = con.inicio(2)
    print (dic)
