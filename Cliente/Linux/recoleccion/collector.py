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
                        elif(dato.startswith('Speed: Unknown')):
                            memoria = None
                            break;
                        elif(dato.startswith('Speed:')):
                            memoria.setvelocidad(self.limpiar_string(dato.split(': ')[1]))
                        elif(dato.startswith('Serial Number:')):
                            memoria.setnumeroserie(self.limpiar_string(dato.split(': ')[1]))
                        elif(dato.startswith('Data Width:')):
                            memoria.settamaniobusdatos(self.limpiar_string(dato.split(': ')[1]))
                        elif(dato.startswith('Size: No Module Installed')):
                            memoria = None
                            break;
                        elif(dato.startswith('Size:')):
                            memoria.settamanio(self.limpiar_string(dato.split(': ')[1]))
                        elif(dato.startswith('Form Factor:')):
                            memoria.settecnologia(self.limpiar_string(dato.split(': ')[1]))
                    if memoria is not None:
                        memorias.append(memoria)                              
        except subprocess.CalledProcessError:
            pass
        return memorias
    
    def get_discosduro(self):
        """Obtiene datos de los discos duros no removibles. Usa una combinación
            de comando: lsblk, /sbin/udevadm y lee del archivo
            s/sys/class/block/{nombre}/device/vendor"""
        discos_duro = []
        posibles_discos = [] #[nombre, tipo, tamanio, particiones]

        lsblk_salida = (subprocess.check_output(['lsblk', '-o', 'KNAME,TYPE,SIZE']).decode('UTF-8').split('\n'))

        for disco_o_part in lsblk_salida:
            if disco_o_part != '' and disco_o_part != 'KNAME TYPE':
                posibles_discos.append(disco_o_part.split())

        inicial_posibles_discos = len(posibles_discos)
        for i in range(0, inicial_posibles_discos):
            if posibles_discos[i][1] == "disk":
                cantidad_particiones = 0
                for j in range(i+1, len(posibles_discos)):
                    if posibles_discos[j][1] == "part":
                        cantidad_particiones += 1
                    else:
                        break
                posibles_discos[i].append(cantidad_particiones)
                posibles_discos.append(posibles_discos[i])
        posibles_discos = posibles_discos[inicial_posibles_discos:]

        for posible_disco in posibles_discos:            
            datos = subprocess.check_output(['/sbin/udevadm', 'info', '--query=property', '--name=' + posible_disco[0]]).decode('UTF-8')
            datosdiscoduro = datos.split('\n')
            disco = None
            for linea in datosdiscoduro:
                if (linea.startswith('ID_BUS=usb') or linea.startswith("ID_USB_DRIVER")):
                    disco = None
                    break
                if disco is None:
                    disco = discoduro.DiscoDuro()
                else:
                    if linea.startswith('ID_MODEL='):
                        disco.setmodelo(linea.split('=')[1])
                    if linea.startswith('ID_SERIAL_SHORT='):
                        disco.setnumeroserie(linea.split('=')[1])
                    if linea.startswith('ID_REVISION='):
                        disco.setfirmware(linea.split('=')[1])
                    if linea.startswith('ID_BUS='):
                        disco.settipointerfaz(linea.split('=')[1])
            if disco is not None:
                url_fabricante = '/sys/class/block/' #{nombre}/device/vendor
                url_fabricante += posible_disco[0] + '/device/vendor'
                disco.setfabricante((subprocess.check_output(['cat', url_fabricante ]).decode('UTF-8').split('\n')[0]).strip())
                disco.setcantidadparticiones(posible_disco[3])
                disco.settamanio(posible_disco[2])
                discos_duro.append(disco)
        return discos_duro
    
    def get_procesador_dmicode(self):
        #faltan tamanio_cache
        proc = procesador.Procesador()
        try:
            proc_dmidecode = subprocess.check_output(['dmidecode', '-t', 'processor']).decode('UTF-8').split('\n')
        except subprocess.CalledProcessError:
            pass
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
        proc.setarquitectura(platform.architecture()[0])
        return proc
    
    def get_procesador_cpuinfo(self):
        """Lee desde el archivo /proc/cpuinfo para obtener la mayoría de datos
            del procesador. Otros datos los obtiene desde 
            /sys/devices/system/cpu/cpu/{id_procesador_fisico}/cpufreq/scaling_max_freq."""
        url_cpuinfo = "/proc/cpuinfo"
        url_archivo_max_velocidad = '/sys/devices/system/cpu/cpu'
        _procesador = procesador.Procesador()
        procesador_fisico_datos = None
        procesadores_logicos = None
        procesador_fisico = {}
        cantidad_procesadores = 0
        try:
            file_procesadores_logicos = open(url_cpuinfo, 'r')
            procesadores_logicos = file_procesadores_logicos.read().split('\n\n')
            file_procesadores_logicos.close()
            procesador_fisico_datos = procesadores_logicos[0].split('\n')
        except (IOError, FileNotFoundError):
            pass #raise ExcepcionFileIO(url_cpuinfo)
        if procesador_fisico_datos is not None:
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
            try:
                _procesador.setfabricante(procesador_fisico['vendor_id'])
                _procesador.setnombre(procesador_fisico['model name'])
                _procesador.setdescripcion(procesador_fisico['model name'])
                _procesador.settamaniocache(procesador_fisico['cache size'])#KB
                _procesador.setcantidadnucleos(int(procesador_fisico['cpu cores']))
            except:
                pass
        if procesadores_logicos is not None:
            try:
                for proc in procesadores_logicos:
                    if proc.find('\nphysical id\t: '+procesador_fisico['physical id']+'\n') != -1:
                        cantidad_procesadores += 1
            except:
                pass
        if cantidad_procesadores != 0:
            _procesador.setcantidadprocesadores(cantidad_procesadores)
        else:
            _procesador.setcantidadprocesadores(1)
        _procesador.setarquitectura(platform.architecture()[0])
        try:
            url_archivo_max_velocidad += procesador_fisico['processor'] + '/cpufreq/scaling_max_freq'
            archivo_max_velocidad = open(url_archivo_max_velocidad, 'r')#en Khz
            velocidad = (float(archivo_max_velocidad.readline())/1000) #Mhz
            _procesador.setvelocidad(self.limpiar_string(str(velocidad)))
            archivo_max_velocidad.close()
        except:
            pass
        return _procesador

    def limpiar_string(self, valor):
        return valor.lstrip().rstrip()

    def obtener_valor(self, linea, separador = ': ', posicion = 1):
        """Dado una linea la separa en clave valor según el separador especificado"""
        return linea.split(separador)[posicion].lstrip()
