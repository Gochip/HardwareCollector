from __future__ import print_function
import componentes.discoduro as discoduro
import componentes.memoriaram as memoriaram
import componentes.procesador as procesador
import componentes.maquina as maquina
import platform
import subprocess

class Collector():
    
    def get_maquina(self):
        maq = maquina.Maquina()
        maq.setdiscosduro(self.get_discosduro())
        maq.setprocesador(self.get_procesador())
        maq.setmemoriasram(self.get_memoriasram())
        return maq
    
    def get_memoriasram(self):
        memorias = []        
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
    
    def get_procesador(self):
        #faltan tamanio_cache
        proc = procesador.Procesador()        
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
        # Verificar calculo.        
        proc.setarquitectura(platform.architecture()[0])
        return proc
    
    def limpiar_string(self, valor):
        return valor.lstrip().rstrip()
