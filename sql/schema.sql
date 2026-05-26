-- Fleet management database schema

CREATE TABLE IF NOT EXISTS vehiculos (
    id       INTEGER PRIMARY KEY,
    matricula TEXT NOT NULL,
    marca    TEXT,
    modelo   TEXT,
    estado   TEXT  -- activo | taller | baja
);

CREATE TABLE IF NOT EXISTS itv (
    id           INTEGER PRIMARY KEY,
    vehiculo_id  INTEGER NOT NULL,
    fecha_itv    TEXT,
    resultado    TEXT,           -- favorable | desfavorable | NULL si no pasada aún
    estado       TEXT,           -- pendiente | ok
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id)
);

CREATE TABLE IF NOT EXISTS facturas (
    id        INTEGER PRIMARY KEY,
    proveedor TEXT,
    concepto  TEXT,
    importe   REAL,
    fecha     TEXT
);
