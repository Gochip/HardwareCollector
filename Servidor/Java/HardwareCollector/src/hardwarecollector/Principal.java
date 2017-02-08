package hardwarecollector;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Diego
 */
public class Principal {

    
    public static void main(String[] args) {
        try {
            (new Servidor()).comenzar();
        } catch (IOException ex) {
            Logger.getLogger(Principal.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
}
