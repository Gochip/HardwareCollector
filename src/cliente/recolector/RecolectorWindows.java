package cliente.recolector;

import comun.componente.Bios;
import comun.componente.DiscoDuro;
import comun.componente.MemoriaRam;
import comun.componente.Procesador;
import comun.maquina.Maquina;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Barrionuevo Diego
 */
public class RecolectorWindows extends Recolector {

    @Override
    public Maquina getMaquina() {
        Maquina maquina = new Maquina();
        maquina.setDiscoDuro(getDiscoDuro());
        maquina.setMemoriasRam(getMemoriasRam());
        maquina.setDiscoDuro(getDiscoDuro());
        return maquina;
    }

    @Override
    public Bios getBios() {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    @Override
    public DiscoDuro getDiscoDuro() {
        DiscoDuro disco = new DiscoDuro();
        try {
            String[] lineasComando = obtenerLineasComando("diskdrive", "manufacturer,model,size,interfacetype,partitions");//faltan firmware y nro de serie
            if (lineasComando != null) {
                String cadenaAtributos = lineasComando[0], cadenaValores = lineasComando[1];
                if (!cadenaAtributos.isEmpty() && !cadenaValores.isEmpty()) {
                    String[] atributos = cadenaAtributos.split(",");
                    String[] valores = cadenaValores.split(",");
                    for (int i = 0; i < atributos.length; i++) {
                        String atributo = atributos[i];
                        if (atributo.equalsIgnoreCase("manufacturer")) {
                            disco.setFabricante(valores[i]);
                        } else if (atributo.equalsIgnoreCase("model")) {
                            disco.setModelo(valores[i]);
                        } else if (atributo.equalsIgnoreCase("size")) {
                            disco.setCapacidad(Double.parseDouble(valores[i]));
                        } else if (atributo.equalsIgnoreCase("interfacetype")) {
                            disco.setTipoInterfaz(valores[i]);
                        } else if (atributo.equalsIgnoreCase("partitions")) {
                            disco.setCantidadParticiones(Integer.parseInt(valores[i]));
                        }
                    }
                }
            }
        } catch (IOException ex) {
            Logger.getLogger(RecolectorWindows.class
                    .getName()).log(Level.SEVERE, null, ex);
        }
        return disco;
    }

    @Override
    public List<MemoriaRam> getMemoriasRam() {
        List<MemoriaRam> memoriasRam = null;
        try {
            String[] lineasComando = obtenerMuchasLineasComando("memorychip", "banklabel,capacity,speed,datawidth,manufacturer,serialnumber");
            if (lineasComando != null) {
                String cadenaAtributos = lineasComando[0];
                String[] cadenasValores = new String[lineasComando.length - 1];
                memoriasRam = new ArrayList<MemoriaRam>();
                //memoriasRam = new MemoriaRam[lineasComando.length - 1];
                for (int i = 0; i < cadenasValores.length; i++) {
                    cadenasValores[i] = lineasComando[i + 1];
                    String cadenaValores = cadenasValores[i];
                    MemoriaRam bancoMemoria = new MemoriaRam();
                    if (!cadenaAtributos.isEmpty() && !cadenaValores.isEmpty()) {
                        String[] atributos = cadenaAtributos.split(",");
                        String[] valores = cadenaValores.split(",");
                        for (int j = 0; j < atributos.length; j++) {
                            String atributo = atributos[j];
                            if (atributo.equalsIgnoreCase("banklabel")) {
                                bancoMemoria.setBanco(valores[j]);
                            } else if (atributo.equalsIgnoreCase("manufacturer")) {
                                bancoMemoria.setFabricante(valores[j]);
                            } else if (atributo.equalsIgnoreCase("capacity")) {
                                bancoMemoria.setCapacidad(Double.parseDouble(valores[j]) / 1000);//me la da en bytes, y la guardo en kb
                            } else if (atributo.equalsIgnoreCase("speed")) {
                                bancoMemoria.setVelocidad(Double.parseDouble(valores[j]));
                            } else if (atributo.equalsIgnoreCase("datawidth")) {
                                bancoMemoria.setTamanioBusDatos(valores[j]);
                            } else if (atributo.equalsIgnoreCase("serialnumber")) {
                                bancoMemoria.setNumeroSerie(valores[j]);
                            } else if (atributo.equalsIgnoreCase("serialnumber")) {
                                bancoMemoria.setNumeroSerie(valores[j]);
                            }
                        }
                    }
                    //memoriasRam[i] = bancoMemoria;
                    memoriasRam.add(bancoMemoria);
                }
            }
        } catch (IOException ex) {
            Logger.getLogger(RecolectorWindows.class
                    .getName()).log(Level.SEVERE, null, ex);
        }
        return memoriasRam;
    }

    @Override
    public Procesador getProcesador() {
        Procesador procesador = new Procesador();
        try {
            String[] lineasComando = obtenerLineasComando("cpu", "addresswidth,manufacturer,name,description,l2cachesize");
            if (lineasComando != null) {
                String cadenaAtributos = lineasComando[0], cadenaValores = lineasComando[1];
                if (!cadenaAtributos.isEmpty() && !cadenaValores.isEmpty()) {
                    String[] atributos = cadenaAtributos.split(",");
                    //atributos[0] siempre es Node
                    String[] valores = cadenaValores.split(",");
                    for (int i = 0; i < atributos.length; i++) {
                        String atributo = atributos[i];
                        if (atributo.equalsIgnoreCase("addresswidth")) {
                            procesador.setArquitectura(valores[i]);
                        } else if (atributo.equalsIgnoreCase("manufacturer")) {
                            procesador.setFabricante(valores[i]);
                        } else if (atributo.equalsIgnoreCase("name")) {
                            procesador.setNombre(valores[i]);
                        } else if (atributo.equalsIgnoreCase("description")) {
                            procesador.setDescripcion(valores[i]);
                        } else if (atributo.equalsIgnoreCase("l2cachesize")) {
                            procesador.setCache(Double.parseDouble(valores[i]));

                        }
                        //procesador.setCantidadNucleos(contadorLineas);
                        //procesador.setCantidadProcesadores(contadorLineas);
                    }
                }
            }
        } catch (IOException ex) {
            Logger.getLogger(RecolectorWindows.class
                    .getName()).log(Level.SEVERE, null, ex);
        }
        return procesador;
    }

    private String[] obtenerLineasComando(String elemento, String cadenaAtributosComando) throws IOException {
        String comando = "wmic " + elemento + " get " + cadenaAtributosComando + " /format:csv";
        Process proceso = Runtime.getRuntime().exec(comando);
        BufferedReader stdInput = new BufferedReader(new InputStreamReader(proceso.getInputStream()));
        String cadenaAtributos = "", cadenaValores = "";
        String linea = null;
        int contadorLineas = 1;
        while ((linea = stdInput.readLine()) != null) {
            if (!linea.isEmpty()) {
                if (contadorLineas == 1) {
                    cadenaAtributos = linea;
                } else {
                    cadenaValores = linea;
                }
                contadorLineas++;
            }
        }
        if (!cadenaAtributos.isEmpty() && !cadenaValores.isEmpty()) {
            return new String[]{cadenaAtributos, cadenaValores};
        }
        return null;
    }

    private String[] obtenerMuchasLineasComando(String elemento, String cadenaAtributosComando) throws IOException {
        String comando = "wmic " + elemento + " get " + cadenaAtributosComando + " /format:csv";
        Process proceso = Runtime.getRuntime().exec(comando);
        BufferedReader stdInput = new BufferedReader(new InputStreamReader(proceso.getInputStream()));
        String cadenaAtributos = "";
        List<String> cadenasValores = new ArrayList();
        String linea = null;
        int contadorLineas = 1;
        while ((linea = stdInput.readLine()) != null) {
            if (!linea.isEmpty()) {
                if (contadorLineas == 1) {
                    cadenaAtributos = linea;
                } else {
                    cadenasValores.add(linea);
                }
                contadorLineas++;
            }
        }
        if (!cadenaAtributos.isEmpty() && !cadenasValores.isEmpty()) {
            String[] resultados = new String[cadenasValores.size() + 1];
            resultados[0] = cadenaAtributos;
            for (int i = 1; i < resultados.length; i++) {
                resultados[i] = cadenasValores.get(i - 1);
            }
            return resultados;
        }
        return null;
    }
}
