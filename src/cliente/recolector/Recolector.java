package cliente.recolector;

import comun.maquina.*;
import comun.componente.*;
import java.util.List;

/**
 *
 * @author Barrionuevo Diego
 */
public abstract class Recolector {

    public abstract Maquina getMaquina();

    public abstract Bios getBios();

    public abstract DiscoDuro getDiscoDuro();

    public abstract List<MemoriaRam> getMemoriasRam();

    public abstract Procesador getProcesador();

}
