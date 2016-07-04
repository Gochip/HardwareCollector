DROP DATABASE IF EXISTS hc_bd;
CREATE DATABASE hc_bd;
USE hc_bd;

CREATE TABLE maquinas(
    id INT NOT NULL AUTO_INCREMENT,
    mac VARCHAR(20),
    ipv4 VARCHAR(20),
    ipv6 VARCHAR(200),
    fecha_alta DATETIME,
    fecha_sincronizacion DATETIME,
    PRIMARY KEY(id)
)ENGINE=MyInnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE componentes(
    id INT NOT NULL,
    nombre VARCHAR(100),
    PRIMARY KEY(id)
)ENGINE=MyInnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE componentes_x_maquinas(
    id_componente INT NOT NULL,
    id_maquina INT NOT NULL,
    nombre VARCHAR(100),
    PRIMARY KEY(id_componente, id_maquina),
    FOREIGN KEY(id_maquina) REFERENCES maquinas(id),
    FOREIGN KEY(id_componente) REFERENCES componentes(id)
)ENGINE=MyInnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE caracteristicas_x_componentes(
    id_caracteristica INT NOT NULL AUTO_INCREMENT,
    id_componente INT NOT NULL,
    nombre VARCHAR(100),
    PRIMARY KEY(id_caracteristica, id_componente),
    FOREIGN KEY(id_componente) REFERENCES componentes(id)
)ENGINE=MyInnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE caracteristicas_x_componentes_x_maquinas(
    id_maquina INT NOT,
    id_componente INT NOT NULL,
    id_caracteristica INT NOT NULL,
    nombre VARCHAR(100),
    PRIMARY KEY(id_maquina, id_componente, id_caracteristica),
    FOREIGN KEY(id_maquina, id_componente) REFERENCES componentes_x_maquinas(id_componente, id_maquina),
    FOREIGN KEY(id_componente, id_caracteristicas) REFERENCES caracteristicas_x_componentes(id_caracteristica, id_componente)
)ENGINE=MyInnoDB DEFAULT CHARACTER SET=utf8;


-- Disco duro
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'fabricante');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'modelo');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'numero_serie');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'tipo_interfaz'); -- SCSI, IDE, USB, ...
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'firmware');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'cantidad_particiones');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'tamanio'); -- Bytes

-- Procesador
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'nombre');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'descripcion');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'fabricante');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'arquitectura');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'cantidad_nucleos');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'cantidad_procesadores');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'velocidad'); -- En MHz
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'tamanio_cache'); -- En KB

-- Memoria ram
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'banco');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'tecnologia'); -- EPROM, VRAM, ...
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'fabricante');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'numero_serie');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'tamanio_bus_datos'); -- Bits
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'velocidad'); -- MHz
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (1,'tamanio'); -- Bytes

