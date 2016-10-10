INSERT INTO maquinas(fecha_alta, fecha_sincronizacion) VALUES (now(), now());

SET @id_disco = (SELECT id FROM componentes WHERE nombre='disco');
SET @id_procesador = (SELECT id FROM componentes WHERE nombre='procesador');
SET @id_memoria_ram = (SELECT id FROM componentes WHERE nombre='memoria_ram');

INSERT INTO componentes_x_maquinas(id_componente, id_maquina) VALUES (@id_procesador, 1);
INSERT INTO caracteristicas_x_componentes_x_maquinas(id_maquina, id_componente, id_caracteristica, valor) 
VALUES 
(1, @id_procesador, 11, "Intel x64"),
(1, @id_procesador, 13, 4),
(1, @id_procesador, 14, "2300 MHz")
;