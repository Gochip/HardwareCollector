package comun.maquina;

import comun.componente.*;

/**
 *
 * @author Barrionuevo Diego
 */
public class Maquina {

    private String id;//int?
    private String nombre;
    private String fabricante;
    private String placeMadre;//deberia ser una clase?
    private Bios bios;
    private SistemaOperativo sistemaOperativo;
    private DiscoDuro discoDuro;
    private MemoriaRam memoriaRam;
    private Procesador procesador;

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getFabricante() {
        return fabricante;
    }

    public void setFabricante(String fabricante) {
        this.fabricante = fabricante;
    }

    public String getPlaceMadre() {
        return placeMadre;
    }

    public void setPlaceMadre(String placeMadre) {
        this.placeMadre = placeMadre;
    }

    public Bios getBios() {
        return bios;
    }

    public void setBios(Bios bios) {
        this.bios = bios;
    }

    public SistemaOperativo getSistemaOperativo() {
        return sistemaOperativo;
    }

    public void setSistemaOperativo(SistemaOperativo sistemaOperativo) {
        this.sistemaOperativo = sistemaOperativo;
    }

    public DiscoDuro getDiscoDuro() {
        return discoDuro;
    }

    public void setDiscoDuro(DiscoDuro discoDuro) {
        this.discoDuro = discoDuro;
    }

    public MemoriaRam getMemoriaRam() {
        return memoriaRam;
    }

    public void setMemoriaRam(MemoriaRam memoriaRam) {
        this.memoriaRam = memoriaRam;
    }

    public Procesador getProcesador() {
        return procesador;
    }

    public void setProcesador(Procesador procesador) {
        this.procesador = procesador;
    }

    public Maquina() {
    }

}
