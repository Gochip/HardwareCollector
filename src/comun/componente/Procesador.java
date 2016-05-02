package comun.componente;

/**
 *
 * @author Barrionuevo Diego
 */
public class Procesador extends Componente {

    private String arquitectura;//(32/64 bits)
    private int cantidadNucleos;//fisicos
    private int cantidadProcesadores;//logicos
    private String fabricante;
    private String nombre;
    private String descripcion;
    private double cache; //(kBytes)

    public String getArquitectura() {
        return arquitectura;
    }

    public void setArquitectura(String arquitectura) {
        this.arquitectura = arquitectura;
    }

    public int getCantidadNucleos() {
        return cantidadNucleos;
    }

    public void setCantidadNucleos(int cantidadNucleos) {
        this.cantidadNucleos = cantidadNucleos;
    }

    public int getCantidadProcesadores() {
        return cantidadProcesadores;
    }

    public void setCantidadProcesadores(int cantidadProcesadores) {
        this.cantidadProcesadores = cantidadProcesadores;
    }

    public String getFabricante() {
        return fabricante;
    }

    public void setFabricante(String fabricante) {
        this.fabricante = fabricante;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    public double getCache() {
        return cache;
    }

    public void setCache(double cache) {
        this.cache = cache;
    }

}
