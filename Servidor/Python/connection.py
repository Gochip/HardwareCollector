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
import mysql
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
        self.password = "Gochi199236"
        self.db = "kkkfsdfewf"

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
        try:
            json_comando = json.loads(command)
            resultado = None
            comando = json_comando["comando"]
            #datos = json_comando["datos"]
            if comando == MAQUINA_NUEVA:
                resultado = {}
                id_maquina = self.maquina_nueva()
                resultado["comando"] = MAQUINA_NUEVA
                resultado["datos"] = {"id": id_maquina}
                print(resultado)
                print("MAQUINA NUEVA")
                command_status = OK
        except:
            print("Formato incorrecto de datos")
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

    def maquina_nueva(self):
        #insercion = "INSERT INTO maquinas (fecha_alta) VALUES (NOW())"
        #mysql.query(insercion)
        
        # obtener id insertado
        
        return 1

    def get_hash(self, id_desafio):
        try:
            id_desafio = int(id_desafio)
            if id_desafio <= 0:
                return "ERROR"
            if id_desafio >= 1000:
                return "ERROR"
        except ValueError:
            return "ERROR"
        try:
            mysql = _mysql.connect('127.0.0.1', self.user, self.password, self.db)
            mysql.query("SELECT hash FROM hash_desafios WHERE id_desafio=%d" %
                                                                  (id_desafio))
            result = mysql.use_result()
            hash = result.fetch_row()[0][0]
            mysql.close()
        except _mysql.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return "ERROR"
        return hash

    def save_response(self, id_desafio, hash, id_grupo):
        print ("GUARDAR RESPUESTA: %s, %s, %s\n" % (id_desafio, hash, id_grupo))
        try:
            id_desafio = int(id_desafio)
            if id_desafio <= 0:
                return "ERROR"
            if id_desafio >= 1000:
                return "ERROR"
        except ValueError:
            return "ERROR"

        try:
            id_grupo = int(id_grupo)
            if id_grupo <= 0:
                return "ERROR"
            if id_grupo >= 1000:
                return "ERROR"
        except ValueError:
            return "ERROR"

        ok = False
        try:
            hash_correcto = self.get_hash(id_desafio)
            mysql = mysql.connect('127.0.0.1', self.user, self.password, self.db)

            ok = hash == hash_correcto
            if(hash == hash_correcto):
                print ("HASH CORRECTO POR %d EN %d" % (id_grupo, id_desafio))
                insercion = "INSERT INTO historico_grupo(id_grupo, id_desafio, fecha_hora) " \
                        "VALUES(%d, %d, NOW())" % (id_grupo, id_desafio)
                mysql.query(insercion)

                insercion2 = "INSERT INTO intentos_por_grupo (id_grupo, id_desafio, hash_intento, fecha_hora, correcto) " \
                " VALUES (%d, %d, '%s', NOW(), true)" % (id_grupo, id_desafio, hash)
                mysql.query(insercion2)

                insercion3 = "UPDATE grupos SET puntaje=puntaje+(SELECT puntos FROM desafios WHERE id=%d) " \
                        "WHERE id=%d AND 1=(SELECT COUNT(*) FROM intentos_por_grupo WHERE id_grupo=%d AND id_desafio=%d AND correcto)" % (id_desafio, id_grupo, id_grupo, id_desafio)
                mysql.query(insercion3)
                print ("OK TODO BIEN")
            else:
                print ("HASH FALLIDO POR %d EN %d" % (id_grupo, id_desafio))
                insercion = "INSERT INTO intentos_por_grupo (id_grupo, id_desafio, hash_intento, fecha_hora, correcto) " \
                " VALUES (%d, %d, '%s', NOW(), false)" % (id_grupo, id_desafio, hash)

                mysql.query(insercion)
                print ("FALLO")
            mysql.close()
        except mysql.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return "ERROR"
        print ("FIN")
        if ok:
            return "OK"
        else:
            return "NO"
