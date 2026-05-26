-- Operational queries used in the pipeline

-- Q1: Vehicles with pending ITV, ordered by date
SELECT
    v.matricula,
    v.marca,
    v.modelo,
    v.estado AS estado_vehiculo,
    i.fecha_itv
FROM vehiculos v
INNER JOIN itv i ON v.id = i.vehiculo_id
WHERE i.estado = 'pendiente'
ORDER BY i.fecha_itv ASC;

-- Q2: Total spend and invoice count per provider
SELECT
    proveedor,
    COUNT(*)            AS num_facturas,
    SUM(importe)        AS total_euros,
    ROUND(AVG(importe), 2) AS media_euros
FROM facturas
GROUP BY proveedor
ORDER BY total_euros DESC;

-- Q3: Fleet status summary
SELECT
    estado,
    COUNT(*) AS total
FROM vehiculos
GROUP BY estado;
