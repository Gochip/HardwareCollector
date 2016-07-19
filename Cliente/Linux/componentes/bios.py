#!/usr/bin/env python3
#encoding: UTF-8

class Bios(): 
	        
    def __init__(self, nombre, fabricante, modelo, version, numero_serie):        
        self.nombre = nombre
        self.fabricante = fabricante
        self.modelo = modelo
        self.version = version
        self.numero_serie = numero_serie
        
    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_fabricante(self, fabricante):
        self.fabricante = fabricante

    def set_modelo(self, modelo):
        self.modelo = modelo

    def set_version(self, version):
        self.version = version	

    def set_numero_serie(self, numero_serie):
        self.numero_serie = numero_serie