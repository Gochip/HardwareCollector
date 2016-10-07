/*
	Agrego tablas para informes
*/

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
)ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE componentes(
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100),
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE componentes_x_maquinas(
    id_componente INT NOT NULL,
    id_maquina INT NOT NULL,
    nombre VARCHAR(100),
    PRIMARY KEY(id_componente, id_maquina),
    FOREIGN KEY(id_maquina) REFERENCES maquinas(id),
    FOREIGN KEY(id_componente) REFERENCES componentes(id)
)ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE caracteristicas_x_componentes(
    id_caracteristica INT NOT NULL AUTO_INCREMENT,
    id_componente INT NOT NULL,
    nombre VARCHAR(100),
    PRIMARY KEY(id_caracteristica, id_componente),
    FOREIGN KEY(id_componente) REFERENCES componentes(id)
)ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE caracteristicas_x_componentes_x_maquinas(
    id_maquina INT NOT NULL,
    id_componente INT NOT NULL,
    id_caracteristica INT NOT NULL,
    valor VARCHAR(300) NOT NULL,
    PRIMARY KEY(id_maquina, id_componente, id_caracteristica),
    FOREIGN KEY(id_maquina, id_componente) REFERENCES componentes_x_maquinas(id_maquina, id_componente),
    FOREIGN KEY(id_componente, id_caracteristica) REFERENCES caracteristicas_x_componentes(id_componente, id_caracteristica)
)ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE tipos_informes(
    id INT NOT NULL AUTO_INCREMENT,
	nombre VARCHAR(100) NOT NULL,
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE informes_x_maquina(
    id_informe INT NOT NULL AUTO_INCREMENT,
    id_maquina INT NOT NULL,
    id_tipo_informe INT NOT NULL,
    hora_informe_programado TIME NULL, -- Es distintio de null unicamente para reportes informes programados
    PRIMARY KEY(id_informe),
    UNIQUE(id_maquina, id_tipo_informe),
    FOREIGN KEY(id_maquina) REFERENCES maquinas(id),
    FOREIGN KEY(id_tipo_informe) REFERENCES tipos_informes(id)
)ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE componentes_x_informe(
    id_maquina INT NOT NULL,
    id_informe INT NOT NULL,
	id_componente INT NOT NULL,
    PRIMARY KEY(id_maquina, id_informe, id_componente),
    FOREIGN KEY(id_informe) REFERENCES informes_x_maquina(id_informe)
    -- FOREIGN KEY(id_componente, id_maquina) REFERENCES componentes_x_maquinas(id_componente, id_maquina)
)ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;


-- Componentes

INSERT INTO componentes (nombre) VALUES ('disco');
INSERT INTO componentes (nombre) VALUES ('procesador');
INSERT INTO componentes (nombre) VALUES ('memoria_ram');

SET @id_disco = (SELECT id FROM componentes WHERE nombre='disco');
SET @id_procesador = (SELECT id FROM componentes WHERE nombre='procesador');
SET @id_memoria_ram = (SELECT id FROM componentes WHERE nombre='memoria_ram');


-- Características

-- Disco duro
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_disco,'fabricante');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_disco,'modelo');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_disco,'numero_serie');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_disco,'tipo_interfaz'); -- SCSI, IDE, USB, ...
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_disco,'firmware');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_disco,'cantidad_particiones');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_disco,'tamanio'); -- Bytes

-- Procesador
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_procesador,'nombre');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_procesador,'descripcion');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_procesador,'fabricante');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_procesador,'arquitectura');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_procesador,'cantidad_nucleos');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_procesador,'cantidad_procesadores');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_procesador,'velocidad'); -- En MHz
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_procesador,'tamanio_cache'); -- En KB

-- Memoria ram
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_memoria_ram,'banco');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_memoria_ram,'tecnologia'); -- EPROM, VRAM, ...
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_memoria_ram,'fabricante');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_memoria_ram,'numero_serie');
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_memoria_ram,'tamanio_bus_datos'); -- Bits
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_memoria_ram,'velocidad'); -- MHz
INSERT INTO caracteristicas_x_componentes (id_componente, nombre) VALUES (@id_memoria_ram,'tamanio'); -- Bytes

-- Tipos de infomes

INSERT INTO tipos_informes (nombre) VALUES ('programado');
INSERT INTO tipos_informes (nombre) VALUES ('inicio_sistema');
INSERT INTO tipos_informes (nombre) VALUES ('inicio_sesion');
INSERT INTO tipos_informes (nombre) VALUES ('apagado');

SET @id_informe_programado = (SELECT id FROM tipos_informes WHERE nombre='programado');
SET @id_informe_inicio_sistema = (SELECT id FROM tipos_informes WHERE nombre='inicio_sistema');
SET @id_informe_inicio_sesion = (SELECT id FROM tipos_informes WHERE nombre='inicio_sesion');
SET @id_informe_apagado = (SELECT id FROM tipos_informes WHERE nombre='apagado');

