import socket
import sys

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

server_address = './hc'
print 'Conectacto a %s' % server_address
try:
    sock.connect(server_address)
except socket.error, msg:
    print >>sys.stderr, msg
    sys.exit(1)

try:
    # Send data
    mensaje = 'solicitar'
    sock.sendall(mensaje)

    recibido = sock.recv(2)
    print recibido

finally:
    print 'Socket cerrado'
    sock.close()
