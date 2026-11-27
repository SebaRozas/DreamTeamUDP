-- ============================================================
-- Consultas SQL -- Monitor de Coyuntura y Proyeccion de la TPM
-- Equipo DreamTeam (Sebastian Rozas, Sofia Vergara, Natalia Luco)
-- Pregunta de investigacion (Hito 1): cual es la trayectoria
-- proyectada para la TPM a 24 meses mediante una Regla de Taylor
-- adaptada a economia abierta, y como la condicionan la Fed y
-- la persistencia inflacionaria.
-- Validadas contra data/coyuntura.db con el catalogo de 12 series
-- BCCh/FRED definido en el Hito 1.
-- Tecnicas: JOIN, GROUP BY y funciones de ventana (LAG, AVG OVER).
-- ============================================================

-- ------------------------------------------------------------
-- Consulta 1 (JOIN): últimas observaciones de cada serie,
-- con su nombre legible y tema.
-- ------------------------------------------------------------
SELECT s.nombre,
       t.tema,
       o.fecha,
       o.valor,
       s.unidad
FROM observaciones o
JOIN series s ON s.id_serie = o.id_serie
JOIN temas  t ON t.id_tema  = s.id_tema
WHERE o.fecha = (SELECT MAX(fecha) FROM observaciones o2 WHERE o2.id_serie = o.id_serie)
ORDER BY t.tema, s.nombre;

-- ------------------------------------------------------------
-- Consulta 2 (GROUP BY): promedio anual de cada serie mensual.
-- Útil para tablas resumen del informe.
-- ------------------------------------------------------------
SELECT s.nombre,
       strftime('%Y', o.fecha)      AS anio,
       ROUND(AVG(o.valor), 2)       AS promedio_anual,
       COUNT(*)                     AS n_observaciones
FROM observaciones o
JOIN series s ON s.id_serie = o.id_serie
GROUP BY s.nombre, anio
ORDER BY s.nombre, anio;

-- ------------------------------------------------------------
-- Consulta 3 (función de ventana): variación interanual (12 meses)
-- calculada directamente en SQL con LAG.
-- Esta es la transformación más usada en análisis de coyuntura.
-- ------------------------------------------------------------
SELECT id_serie,
       fecha,
       valor,
       LAG(valor, 12) OVER (PARTITION BY id_serie ORDER BY fecha)  AS valor_12m_atras,
       ROUND( 100.0 * (valor / LAG(valor, 12) OVER (PARTITION BY id_serie ORDER BY fecha) - 1), 2) AS var_interanual_pct
FROM observaciones
-- Solo índices y precios (IPC empalmado, IPC sin volátiles, Imacec, Imacec no minero, cobre, IPC EE.UU.):
-- en las tasas la variación en % no tiene sentido, ver Consulta 3b.
WHERE id_serie IN ('F074.IPC.IND.Z.EP23.C.M', 'G073.IPCSV.IND.2023.M', 'F032.IMC.IND.Z.Z.EP18.Z.Z.0.M', 'F032.IMC.IND.Z.Z.EP18.N03.Z.0.M', 'F019.PPB.PRE.40.M', 'CPIAUCSL')
ORDER BY id_serie, fecha;

-- ------------------------------------------------------------
-- Consulta 4 (función de ventana): promedio móvil de 3 meses,
-- para suavizar series volátiles antes de graficarlas.
-- ------------------------------------------------------------
SELECT id_serie,
       fecha,
       valor,
       ROUND(AVG(valor) OVER (
             PARTITION BY id_serie
             ORDER BY fecha
             ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS promedio_movil_3m
FROM observaciones
ORDER BY id_serie, fecha;

-- ------------------------------------------------------------
-- Consulta 3b (función de ventana): cambio en 12 meses de las
-- tasas e índices de difusión, en puntos porcentuales.
-- En tasas se reporta la diferencia (ej: desempleo pasa de 8%
-- a 9% = +1 pp), no la variación porcentual.
-- ------------------------------------------------------------
SELECT id_serie,
       fecha,
       valor,
       ROUND(valor - LAG(valor, 12) OVER (PARTITION BY id_serie ORDER BY fecha), 2) AS dif_12m_pp
FROM observaciones
WHERE id_serie IN ('F089.IPC.V12.15.M', 'F049.DES.TAS.INE9.10.M', 'FEDFUNDS')
ORDER BY id_serie, fecha;

-- ------------------------------------------------------------
-- Consulta 5 (JOIN + GROUP BY): control de calidad de la base.
-- Cobertura y rango de cada serie, para verificar que se
-- cargaron datos reales (no del modo demo) y sin huecos.
-- ------------------------------------------------------------
SELECT s.id_serie,
       s.nombre,
       s.frecuencia,
       COUNT(*)               AS n_obs,
       MIN(o.fecha)           AS desde,
       MAX(o.fecha)           AS hasta,
       ROUND(MIN(o.valor), 2) AS minimo,
       ROUND(MAX(o.valor), 2) AS maximo
FROM observaciones o
JOIN series s ON s.id_serie = o.id_serie
GROUP BY s.id_serie, s.nombre, s.frecuencia
ORDER BY s.frecuencia, s.nombre;


