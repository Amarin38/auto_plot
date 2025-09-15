-- ALTER TABLE indice_repuesto RENAME TO index_repuesto;
-- ALTER TABLE forecast_data RENAME TO forecast_data_old;


-- CREATE TABLE forecast_data (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     Repuesto TEXT,
--     FechaCompleta TEXT,
--     TipoRepuesto TEXT,
--     Año INTEGER,
--     Mes INTEGER,
--     TotalAño INTEGER,
--     TotalMes INTEGER,
--     Promedio REAL,
--     IndiceAnual REAL,
--     IndiceEstacional REAL
-- );

ATTACH DATABASE 'C:/Users/repuestos01/Documents/Programas/auto_plot/src/db/common_data.db' as COMMONDB;

INSERT INTO COMMONDB.internos_cabecera (Linea, Interno, Cabecera)
SELECT Linea, Interno, Cabecera
FROM internos_cabecera;

DETACH DATABASE COMMONDB;



-- DELETE FROM "json_config" 
-- WHERE id == 4

DROP TABLE "internos_cabecera";

-- Update a datos de coches_cabecera
-- UPDATE "coches_cabecera"
-- SET CantidadCoches = 136
-- WHERE Cabecera LIKE 'CUSA'; 

-- DROP TABLE "deviation"

