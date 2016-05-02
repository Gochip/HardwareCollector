package comun.componente;

/**
 *
 * @author Barrionuevo Diego
 */
public class DiscoDuro extends Componente {

    private String fabricante;
    private String modelo;
    private String numeroSerie;
    private double capacidad;//kBytes
    private String tipoInterfaz;//(SCSI , PCI, IDE)
    private String firmware;
    private int cantidadParticiones;
    //private int bytesPorSector;//cantidad
    //(Total de sectores, cilindros, cabeceras, pistas, pistas por cilindro)

    public String getFabricante() {
        return fabricante;
    }

    public void setFabricante(String fabricante) {
        this.fabricante = fabricante;
    }

    public String getModelo() {
        return modelo;
    }

    public void setModelo(String modelo) {
        this.modelo = modelo;
    }

    public String getNumeroSerie() {
        return numeroSerie;
    }

    public void setNumeroSerie(String numeroSerie) {
        this.numeroSerie = numeroSerie;
    }

    public double getCapacidad() {
        return capacidad;
    }

    public void setCapacidad(double capacidad) {
        this.capacidad = capacidad;
    }

    public String getTipoInterfaz() {
        return tipoInterfaz;
    }

    public void setTipoInterfaz(String tipoInterfaz) {
        this.tipoInterfaz = tipoInterfaz;
    }

    public String getFirmware() {
        return firmware;
    }

    public void setFirmware(String firmware) {
        this.firmware = firmware;
    }

    public int getCantidadParticiones() {
        return cantidadParticiones;
    }

    public void setCantidadParticiones(int cantidadParticiones) {
        this.cantidadParticiones = cantidadParticiones;
    }

}
