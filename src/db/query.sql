
-- ALTER TABLE forecast_trend RENAME TO forecast_trend_old;
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

-- INSERT INTO forecast_data (Repuesto, FechaCompleta, TipoRepuesto, Año, Mes, TotalAño, TotalMes, Promedio, IndiceAnual, IndiceEstacional)
-- SELECT Repuesto, FechaCompleta, TipoRepuesto, Año, Mes, TotalAño, TotalMes, Promedio, IndiceAnual, IndiceEstacional
-- FROM forecast_data_old;

-- DROP TABLE forecast_data_old;
