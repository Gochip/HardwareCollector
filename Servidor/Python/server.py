#!/usr/bin/env python
# encoding: utf-8

import optparse
import select
import socket
import connection
import threading
import sys
import os
import json
from constants import *


class Server(object):
    """
    Servidor de hashes.
    """

    def __init__(self, addr=DEFAULT_ADDR, port=DEFAULT_PORT):
        """Construye un servidor de hashes que atiende a clientes
        concurrentemente.
        """
        print ("Parámetros de entrada %s, %s" % (addr, port))

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((addr, port))
        self.socket.listen(10)
        self.socket.setblocking(0)

    def serve(self):
        """
        Loop principal del servidor. Acepta varias conexiones a la vez.
        """
        poll = select.poll()
        poll.register(self.socket.fileno(), select.POLLIN)
        self.clients = {}
        clients = self.clients
        try:
            while True:
                events = poll.poll()
                for (fileno, event) in events:
                    try:
                        if event & select.POLLIN:
                            if fileno == self.socket.fileno():
                                (client, address) = self.socket.accept()
                                client.setblocking(0)
                                poll.register(client, select.POLLIN)
                                con = connection.Connection(client)
                                clients[client.fileno()] = con
                            else:
                                con = clients[fileno]
                                if con.handle_input():
                                    poll.modify(con.get_fileno(), select.POLLOUT)
                                else:
                                    poll.unregister(con.get_fileno())
                                    con.close()
                        elif event & select.POLLOUT:
                            con = clients[fileno]
                            if not con.handle_output():
                                poll.modify(con.get_fileno(), select.POLLIN)
                            if con.is_closed():
                                poll.unregister(con.get_fileno())
                                con.close()
                    except Exception as ex:
                        print ex
                        print "Se desconectó un cliente"
        except KeyboardInterrupt or socket.error:
            print "\nCerrando server"
            self.socket.close()


def main():
    """Parsea los argumentos y lanza el servidor"""
    try:
        parser = optparse.OptionParser()
        parser.add_option("-p", "--port",
                          help=u"Número de puerto TCP donde escuchar",
                          default=DEFAULT_PORT)
        parser.add_option("-a", "--address",
                          help=u"Dirección donde escuchar", default=DEFAULT_ADDR)
        (options, args) = parser.parse_args()
        if len(args) > 0:
            parser.print_help()
            sys.exit(1)
        try:
            port = int(options.port)
        except ValueError:
            sys.stderr.write(
                "Numero de puerto inválido: %s\n" % repr(options.port))
            parser.print_help()
            sys.exit(1)

        server = Server(options.address, port)
        t1 = threading.Thread(target=server.serve)
        t1.start()
        print "OK"
        
        server_address = './hc'
        try:
            os.unlink(server_address)
        except OSError:
            if os.path.exists(server_address):
                raise
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        
        sock.bind(server_address)
        
        sock.listen(1)
        while True:
            connection, client_address = sock.accept()
            try:
                while True:
                    data = connection.recv(16)
                    print >>sys.stderr, 'Recibido "%s"' % data
                    if data and data == "solicitar":
                        for clave, conexion in server.clients.items():
                            salida = conexion.solicitar(["procesador", "discos_duros", "memorias_ram"])
                            print salida
                            conexion.output += json.dumps(salida)
                            conexion.send()
                        connection.sendall("ok")
                    else:
                        connection.sendall("no")
                        break
            except:
                pass
            finally:
                connection.close()
    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == '__main__':
    main()
