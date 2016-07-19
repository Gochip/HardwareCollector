#!/usr/bin/env python3
#encoding: UTF-8
import recoleccion.collector as collector

recolector = collector.Collector()
maquina = recolector.get_maquina()
print(maquina.tostr())
