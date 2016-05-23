package cliente.recolector;

import comun.maquina.*;
import comun.componente.*;

/**
 *
 * @author Barrionuevo Diego
 */
public abstract class Recolector {

    public abstract Maquina getMaquina();

    public abstract Bios getBios();

    public abstract DiscoDuro getDiscoDuro();

    public abstract MemoriaRam[] getMemoriasRam();

    public abstract Procesador getProcesador();

}
