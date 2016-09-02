# encoding: utf-8
# Revisiones 2013-2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: constants.py 388 2011-03-22 14:20:06Z nicolasw $
#
# Modificado y adaptado por Parisi Germán para el HardwareCollector. 2015.
#

DEFAULT_ADDR = 'localhost'
DEFAULT_PORT = 30330


MAQUINA_NUEVA = 'maquina_nueva'

SALIR = 'salir'

EOL = '\r\n'

OK = 0
ERROR = 100
COMANDO_INVALIDO = 200

def valid_status(s):
    return s in error_messages.keys()


def fatal_status(s):
    assert valid_status(s)
    return 100 <= s < 200


VALID_CHARS = set(".-_;")
for i in xrange(ord('A'), ord('Z')):
    VALID_CHARS.add(chr(i))
for i in xrange(ord('a'), ord('z')):
    VALID_CHARS.add(chr(i))
for i in xrange(ord('0'), ord('9')):
    VALID_CHARS.add(chr(i))
