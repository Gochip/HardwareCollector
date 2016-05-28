package cliente.principal;

import cliente.recolector.Recolector;
import cliente.recolector.RecolectorWindows;
import comun.maquina.Maquina;

/**
 *
 * @author Barrionuevo Diego
 */
public class ClientePrincipal {

    public static void main(String[] args) {
        Recolector recolector = new RecolectorWindows();
        Maquina maquina = recolector.getMaquina();
        System.out.println(maquina.getDiscoDuro().getModelo());
    }
}
