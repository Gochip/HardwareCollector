package hardwarecollector;

import java.io.DataInputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class Servidor {

    private final int puerto = 30330;
    private ServerSocket socket;

    public void comenzar() throws IOException, ParseException {
        socket = new ServerSocket(puerto);
        Socket socket_cli = socket.accept();
        System.out.println("Cliente conectado");
        DataInputStream in = new DataInputStream(socket_cli.getInputStream());
//        String mensaje = "";
//        System.out.println("por leer");
//        mensaje = in.readUTF();
        byte[] lenBytes = new byte[4];
        in.read(lenBytes, 0, 4);
        int len = (((lenBytes[3] & 0xff) << 24) | ((lenBytes[2] & 0xff) << 16) | ((lenBytes[1] & 0xff) << 8) | (lenBytes[0] & 0xff));
        byte[] receivedBytes = new byte[len];
        in.read(receivedBytes, 0, len);
        String mensaje = new String(receivedBytes, 0, len);
        System.out.println("Me llego algo: " + mensaje);
        JSONObject json = (JSONObject) new JSONParser().parse(mensaje);
        System.out.println("comando es " + json.get("comando"));
    }
}
