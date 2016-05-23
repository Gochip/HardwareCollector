package cliente.recolector;

import comun.componente.Bios;
import comun.componente.DiscoDuro;
import comun.componente.MemoriaRam;
import comun.componente.Procesador;
import comun.maquina.Maquina;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Barrionuevo Diego
 */
public class RecolectorWindows extends Recolector {

    @Override
    public Maquina getMaquina() {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    @Override
    public Bios getBios() {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    @Override
    public DiscoDuro getDiscoDuro() {
        DiscoDuro disco = new DiscoDuro();
        try {
            String[] linasComando = obtenerLineasComando("diskdrive", "manufacturer,model,size,interfacetype,partitions");//faltan firmware y nro de serie
            if (linasComando != null) {
                String cadenaAtributos = linasComando[0], cadenaValores = linasComando[1];
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
    public MemoriaRam getMemoriaRam() {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
//        MemoriaRam memoriaRam = new MemoriaRam();
//        try {
//            String[] linasComando = obtenerLineasComando("memphysical", "addresswidth,manufacturer,name,description,l2cachesize");
//            if (linasComando != null) {
//                String cadenaAtributos = linasComando[0], cadenaValores = linasComando[1];
//                if (!cadenaAtributos.isEmpty() && !cadenaValores.isEmpty()) {
//                    String[] atributos = cadenaAtributos.split(",");
//                    //atributos[0] siempre es Node
//                    String[] valores = cadenaValores.split(",");
//                    for (int i = 0; i < atributos.length; i++) {
//                        String atributo = atributos[i];
//                    }
//                }
////                private String banco;//numero o nombre de socalo
////    private String tecnologia;
////    private String fabricante;
////    private String numeroSerie;
////    private String tamanioBusDatos;
////    private double velocidad;//Hz
////    private double capacidad;//kBytes
//            }
//        } catch (IOException ex) {
//            Logger.getLogger(RecolectorWindows.class
//                    .getName()).log(Level.SEVERE, null, ex);
//        }
//        return memoriaRam;
    }

    @Override
    public Procesador getProcesador() {
        Procesador procesador = new Procesador();
        try {
            String[] linasComando = obtenerLineasComando("cpu", "addresswidth,manufacturer,name,description,l2cachesize");
            if (linasComando != null) {
                String cadenaAtributos = linasComando[0], cadenaValores = linasComando[1];
                if (!cadenaAtributos.isEmpty() && !cadenaValores.isEmpty()) {
                    String[] atributos = cadenaAtributos.split(",");
                    //atributos[0] siempre es Node
                    String[] valores = cadenaValores.split(",");
                    for (int i = 0; i < atributos.length; i++) {
                        String atributo = atributos[i];
                        if (atributo.equalsIgnoreCase("addresswidth")) {
                            //addresswidth,manufacturer,name,description,l2cachesize
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
        System.out.println(comando);
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
}
