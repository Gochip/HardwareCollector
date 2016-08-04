package hardwarecollector;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class Servidor {

    private final int puerto = 30330;
    private ServerSocket socket;

    public void comenzar() throws IOException {
        socket = new ServerSocket(puerto);
        Socket socketCliente = socket.accept();
        //cliente conectado
        //espero comandos, el cliente debe mandar 'maquina_nueva' si es nuevo
        JSONObject jsonComando = recibirComando(socketCliente);
        System.out.println(jsonComando.get("comando"));
        if ((jsonComando.get("comando")).equals("maquina_nueva")) {
            System.out.println("!");
            String idUnico = String.valueOf(Math.round((float) (Math.random() * 1000)));
            JSONObject jsonComandoMaquinaRegistrada = new JSONObject();
            jsonComandoMaquinaRegistrada.put("comando", "maquina_registrada");
            jsonComandoMaquinaRegistrada.put("datos", new JSONObject(
                    new HashMap<String, String>() {
                        {
                            put("id", idUnico);
                        }
                    }));
            System.out.println(jsonComandoMaquinaRegistrada.toJSONString());
            enviarComando(socketCliente, jsonComandoMaquinaRegistrada);
        }
    }

    public void enviarComando(Socket socketCliente, JSONObject jsonComando) throws IOException {
        OutputStream os = socketCliente.getOutputStream();
        byte[] toSendBytes = (jsonComando.toJSONString()).getBytes();
        int toSendLen = toSendBytes.length;
        byte[] toSendLenBytes = new byte[4];
        toSendLenBytes[0] = (byte) (toSendLen & 0xff);
        toSendLenBytes[1] = (byte) ((toSendLen >> 8) & 0xff);
        toSendLenBytes[2] = (byte) ((toSendLen >> 16) & 0xff);
        toSendLenBytes[3] = (byte) ((toSendLen >> 24) & 0xff);
        os.write(toSendLenBytes);
        os.write(toSendBytes);
    }

    public JSONObject recibirComando(Socket socketCliente) throws IOException {
        JSONObject respuesta = null;
        try {
            DataInputStream in = new DataInputStream(socketCliente.getInputStream());
            byte[] lenBytes = new byte[4];
            in.read(lenBytes, 0, 4);
            int len = (((lenBytes[3] & 0xff) << 24) | ((lenBytes[2] & 0xff) << 16) | ((lenBytes[1] & 0xff) << 8) | (lenBytes[0] & 0xff));
            byte[] receivedBytes = new byte[len];
            in.read(receivedBytes, 0, len);
            String mensaje = new String(receivedBytes, 0, len);
            System.out.println("Me llego algo: " + mensaje);
            respuesta = (JSONObject) new JSONParser().parse(mensaje);
        } catch (ParseException e) {
            System.err.println("Error al parsear comando");
        }
        return respuesta;
    }
}
