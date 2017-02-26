import platform
import subprocess
import componentes.maquina as maquina
import componentes.sistemaoperativo as sistemaoperativo
import componentes.discoduro as discoduro
import componentes.procesador as procesador
import componentes.memoriaram as memoriaram
from util.excepciones import *

class Collector():
    
    def get_maquina(self):
        maq = maquina.Maquina()
        maq.setdiscosduro(self.get_discosduro())
        maq.setprocesador(self.get_procesador_cpuinfo())
        maq.setmemoriasram(self.get_memoriasram())
        return maq

    def get_maquina_nueva(self):
        maq = maquina.Maquina()
        maq.setnombre(platform.node())
        sistema = platform.system()
        if sistema == '':
            sistema = None
        version = platform.version()
        if version == '':
            version = None
        so = sistemaoperativo.SistemaOperativo(sistema, version)
        maq.setsistemaoperativo(so)
        return maq
    
    def get_memoriasram(self):
        memorias = []
        try:        
            mem_dmidecode = ((subprocess.check_output(['dmidecode', '-t', 'memory'])).decode('UTF-8')).split('\n\n')        
            for dmi in mem_dmidecode:
                if(dmi.find('Memory Device') != -1):
                    memoria = memoriaram.MemoriaRam()
                    datos_memoria = dmi.split('\n')
                    for dato in datos_memoria:
                        dato = dato.lstrip()
                        if(dato.startswith('Bank Locator:')):
                            memoria.setbanco(self.limpiar_string(dato.split(': ')[1]))
                        elif(dato.startswith('Manufacturer:')):
                            memoria.setfabricante(self.limpiar_string(dato.split(': ')[1]))
                        elif(dato.startswith('Speed:')):
                            memoria.setvelocidad(self.limpiar_string(dato.split(': ')[1]))
                        elif(dato.startswith('Serial Number:')):
                            memoria.setnumeroserie(self.limpiar_string(dato.split(': ')[1]))
                        elif(dato.startswith('Data Width:')):
                            memoria.settamaniobusdatos(self.limpiar_string(dato.split(': ')[1]))
                        elif(dato.startswith('Size:')):
                            memoria.settamanio(self.limpiar_string(dato.split(': ')[1]))
                        elif(dato.startswith('Form Factor:')):
                            memoria.settecnologia(self.limpiar_string(dato.split(': ')[1]))
                    memorias.append(memoria)                              
        except subprocess.CalledProcessError:
#            raise ExcepcionSubprocess
            pass
        return memorias
    
    def get_discosduro(self):
        discos_duro = []
        disco = discoduro.DiscoDuro()
        #ejecuto lsblk
        lsblk_salida = (subprocess.check_output(['lsblk']).decode('UTF-8').split('\n'))
        datos = ''
        datosdiscoduro = [] #['NAME,MAJ:MIN,RM,SIZE,RO,TYPE,MOUNTPOINT(no hay punto de montura en sda-disk)']
        for lsblk_line in lsblk_salida:
            if (lsblk_line.rfind('disk') != -1):
                datos = lsblk_line.rstrip().split(' ')
                break
        for dato in datos:
            if(dato != ''):
                datosdiscoduro.append(dato) 
        #seteo el tamaño del disco        
        disco.settamanio(datosdiscoduro[3])
        #obtengo modelo y numero_serial del disco
        datos = subprocess.check_output(['/sbin/udevadm', 'info', '--query=property', '--name=sda']).decode('UTF-8')
        datosdiscoduro = datos.split('\n')
        for linea in datosdiscoduro:
            if linea.startswith('ID_MODEL='):
                disco.setmodelo(linea.split('=')[1])
            if linea.startswith('ID_SERIAL_SHORT='):
                disco.setnumeroserie(linea.split('=')[1])
        #seteo fabricante        
        disco.setfabricante(subprocess.check_output(['cat', '/sys/class/block/sda/device/vendor']).decode('UTF-8').split('\n')[0])
        discos_duro.append(disco)
        return discos_duro

    def get_discosduro_(self):
        discos_duro = []
        disco = discoduro.DiscoDuro()
        #ejecuto lsblk
        lsblk_salida = (subprocess.check_output(['lsblk', '-o', 'NAME,MODEL,TYPE,SIZE']).decode('UTF-8').split('\n'))
        datos = ''
        datosdiscoduro = [] #['NAME,MAJ:MIN,RM,SIZE,RO,TYPE,MOUNTPOINT(no hay punto de montura en sda-disk)']
        for lsblk_line in lsblk_salida:
            if (lsblk_line.rfind('disk') != -1):
                datos = lsblk_line.rstrip().split(' ')
                break
        for dato in datos:
            if(dato != ''):
                datosdiscoduro.append(dato) 
        #seteo el tamaño del disco        
        disco.settamanio(datosdiscoduro[3])
        #obtengo modelo y numero_serial del disco
        datos = subprocess.check_output(['/sbin/udevadm', 'info', '--query=property', '--name=sda']).decode('UTF-8')
        datosdiscoduro = datos.split('\n')
        for linea in datosdiscoduro:
            if linea.startswith('ID_MODEL='):
                disco.setmodelo(linea.split('=')[1])
            if linea.startswith('ID_SERIAL_SHORT='):
                disco.setnumeroserie(linea.split('=')[1])
        #seteo fabricante        
        disco.setfabricante(subprocess.check_output(['cat', '/sys/class/block/sda/device/vendor']).decode('UTF-8').split('\n')[0])
        discos_duro.append(disco)
        return discos_duro

    
    def get_procesador_dmicode(self):
        #faltan tamanio_cache
        proc = procesador.Procesador()
        try:
            proc_dmidecode = subprocess.check_output(['dmidecode', '-t', 'processor']).decode('UTF-8').split('\n')          
            for proc_dato in proc_dmidecode:            
                proc_dato = proc_dato.lstrip()             
                if proc_dato.startswith('Family:'):
                    proc.setnombre(self.limpiar_string(proc_dato.split(': ')[1]))
                elif proc_dato.startswith('Version:'):
                    proc.setdescripcion(self.limpiar_string(proc_dato.split(': ')[1]))
                elif proc_dato.startswith('Manufacturer:'):
                    proc.setfabricante(self.limpiar_string(proc_dato.split(': ')[1]))
                elif proc_dato.startswith('Current Speed:'):
                    proc.setvelocidad(proc_dato.split(': ')[1])
                    proc.setarquitectura(self.limpiar_string(proc_dato.split(': ')[1]))
                elif proc_dato.startswith('Core Count:'): # Puede ser distinto a Core Enabled
                    proc.setcantidadnucleos(self.limpiar_string(proc_dato.split(': ')[1]))
                # hilos por nucle, verificar
                elif proc_dato.startswith('Thread Count:'):                
                    proc.setcantidadprocesadores(int(self.limpiar_string(proc_dato.split(': ')[1])))
        except subprocess.CalledProcessError:
            raise ExcepcionSubprocess
        # Verificar calculo.        
        proc.setarquitectura(platform.architecture()[0])
        return proc
    
    def get_procesador_cpuinfo(self):
        #lee archivo /proc/cpuinfo
        _procesador = procesador.Procesador()
        #procesadores_logicos = subprocess.check_output(['cat', '/proc/cpuinfo']).decode('UTF-8').split('\n\n')
        url_cpuinfo = "/proc/cpuinfo"
        try:
            file_procesadores_logicos = open(url_cpuinfo, 'r')
            procesadores_logicos = file_procesadores_logicos.read().split('\n\n')
            file_procesadores_logicos.close()
            procesador_fisico_datos = procesadores_logicos[0].split('\n')
            procesador_fisico = {}
            for proc in procesador_fisico_datos:
                if proc.startswith('physical id\t:'):
                    procesador_fisico['physical id'] = self.obtener_valor(proc,': ',1)
                elif proc.startswith('processor\t:'):
                    procesador_fisico['processor'] = self.obtener_valor(proc,': ',1)
                elif proc.startswith('vendor_id\t:'):
                    procesador_fisico['vendor_id'] = self.obtener_valor(proc,': ',1)
                elif proc.startswith('cpu family\t:'):
                    procesador_fisico['cpu family'] = self.obtener_valor(proc,': ',1)
                elif proc.startswith('model\t\t:'):
                    procesador_fisico['model'] = self.obtener_valor(proc,': ',1)
                elif proc.startswith('model name\t:'):
                    procesador_fisico['model name'] = self.obtener_valor(proc,': ',1)
                elif proc.startswith('cache size\t:'):
                    procesador_fisico['cache size'] = self.obtener_valor(proc,': ',1)
                elif proc.startswith('cpu cores\t:'):
                    procesador_fisico['cpu cores'] = self.obtener_valor(proc,': ',1)
            cantidad_procesadores = 0
            for proc in procesadores_logicos:
                if proc.find('\nphysical id\t: '+procesador_fisico['physical id']+'\n') != -1:
                    cantidad_procesadores += 1
            _procesador.setcantidadprocesadores(cantidad_procesadores)
            _procesador.setfabricante(procesador_fisico['vendor_id'])
            _procesador.setnombre(procesador_fisico['model name'])
            _procesador.setdescripcion(procesador_fisico['model name'])
            _procesador.settamaniocache(procesador_fisico['cache size'])#KB
            _procesador.setcantidadnucleos(int(procesador_fisico['cpu cores']))
        except (IOError, FileNotFoundError):
            raise ExcepcionFileIO(cpuinfo)
        _procesador.setarquitectura(platform.architecture()[0])
        url_archivo_max_velocidad = '/sys/devices/system/cpu/cpu'+procesador_fisico['processor']+'/cpufreq/scaling_max_freq'
        try:
            archivo_max_velocidad = open(url_archivo_max_velocidad, 'r')#en Khz
            velocidad = (float(archivo_max_velocidad.readline())/1000) #Mhz
            _procesador.setvelocidad(self.limpiar_string(str(velocidad)))
            archivo_max_velocidad.close()
        except (IOError, FileNotFoundError):
            raise ExcepcionFileIO(url_archivo_max_velocidad)
        return _procesador

    def limpiar_string(self, valor):
        return valor.lstrip().rstrip()

    def obtener_valor(self, linea, separador = ': ', posicion = 1):
        """Dado una linea la separa en clave valor según el separador especificado"""
        return linea.split(separador)[posicion].lstrip()
