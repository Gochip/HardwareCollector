package comun.maquina;

import comun.componente.*;
import java.util.List;

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
    private DiscoDuro discoDuro;//podria ser un array
    private List<MemoriaRam> memoriasRam;
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

    public void agregarMemoriasRam(MemoriaRam memoriaRam) {
        this.memoriasRam.add(memoriaRam);
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public List<MemoriaRam> getMemoriasRam() {
        return memoriasRam;
    }

    public void setMemoriasRam(List<MemoriaRam> memoriasRam) {
        this.memoriasRam = memoriasRam;
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
