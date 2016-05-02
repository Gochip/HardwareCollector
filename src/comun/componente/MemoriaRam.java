package comun.componente;

/**
 *
 * @author Barrionuevo Diego
 */
public class MemoriaRam extends Componente {

    private String banco;//numero o nombre de socalo
    private String tecnologia;
    private String fabricante;
    private String numeroSerie;
    private String tamanioBusDatos;
    private double velocidad;//Hz
    private double capacidad;//kBytes

    public String getBanco() {
        return banco;
    }

    public void setBanco(String banco) {
        this.banco = banco;
    }

    public String getTecnologia() {
        return tecnologia;
    }

    public void setTecnologia(String tecnologia) {
        this.tecnologia = tecnologia;
    }

    public String getFabricante() {
        return fabricante;
    }

    public void setFabricante(String fabricante) {
        this.fabricante = fabricante;
    }

    public String getNumeroSerie() {
        return numeroSerie;
    }

    public void setNumeroSerie(String numeroSerie) {
        this.numeroSerie = numeroSerie;
    }

    public String getTamanioBusDatos() {
        return tamanioBusDatos;
    }

    public void setTamanioBusDatos(String tamanioBusDatos) {
        this.tamanioBusDatos = tamanioBusDatos;
    }

    public double getVelocidad() {
        return velocidad;
    }

    public void setVelocidad(double velocidad) {
        this.velocidad = velocidad;
    }

    public double getCapacidad() {
        return capacidad;
    }

    public void setCapacidad(double capacidad) {
        this.capacidad = capacidad;
    }

}
