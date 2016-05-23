package cliente.principal;

import cliente.recolector.Recolector;
import cliente.recolector.RecolectorWindows;
import comun.componente.DiscoDuro;
import comun.componente.Procesador;

/**
 *
 * @author Barrionuevo Diego
 */
public class ClientePrincipal {

    public static void main(String[] args) {
        Recolector recolector = new RecolectorWindows();
        Procesador procesador = recolector.getProcesador();
        System.out.println(procesador.getFabricante());
        DiscoDuro disco  = recolector.getDiscoDuro();
        System.out.println(disco.getModelo());
    }
}
