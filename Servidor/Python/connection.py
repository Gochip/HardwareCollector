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
        self.password = "12345678"
        self.db = "hc_bd"
        self.id_maquina = None

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
                print "Command:", command[:50]
                command_status = self.execute(command)
                print "Command status:", command_status
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
        print(command)
        command_status = COMANDO_INVALIDO
        if True:
        #try:
            json_comando = json.loads(command)
            resultado = None
            comando = json_comando["comando"]
            #datos = json_comando["datos"]
            if comando == MAQUINA_NUEVA:
                resultado = {}
                id_maquina = self.maquina_nueva()
                resultado["comando"] = MAQUINA_REGISTRADA
                resultado["datos"] = {"id": id_maquina}
                self.id_maquina = id_maquina
                print("MAQUINA REGISTRADA")
                command_status = OK
            elif comando == INICIO:
                resultado = {}
                respuesta = self.inicio()
                resultado["comando"] = CONFIGURACION
                resultado["datos"] = {"configuracion": respuesta}
                print("MAQUINA REGISTRADA")
                command_status = OK
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

    def validate_command(self, command):
        # Primero chequeamos que los caracteres tengan sentido
        for i in xrange(0, len(command)):
            if command[i] not in VALID_CHARS:
                return False
        return True

    def validate_argument(self, arg):
        return self.validate_command(arg)

    def close(self):
        self.socket.close()

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

    def maquina_nueva(self):
        """
            Método que ejecuta el comando MAQUINA_NUEVA.
            Retorna el ID de máquina creada.
        """
        cnx = mysql.connector.connect(user=self.user, password=self.password, database=self.db)
        cursor = cnx.cursor()

        insercion = "INSERT INTO maquinas (fecha_alta) VALUES (NOW())"
        cursor.execute(insercion)
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

    def inicio(self, id_maquina):
        """
            Método que ejecuta el comando INICIO.
        """
        resultado = {}
        if self.id_maquina is not None:
            id_maquina = self.id_maquina

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
                #informe["tipo"] = tipo
                #if tipo == "programado":
                #    informe["hora"] = "12:00"
                configuracion["informes"].append(informe)
            resultado["configuracion"] = configuracion
        return resultado


if __name__ == "__main__":
    con = Connection(None)
    #con.maquina_nueva()
    dic = con.inicio(2)
    print (dic)
