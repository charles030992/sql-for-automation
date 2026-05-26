-- Sample fleet data

INSERT INTO vehiculos VALUES
(1, '1234ABC', 'Ford',       'Transit',  'activo'),
(2, '5555DEF', 'Renault',    'Master',   'activo'),
(3, '9999XYZ', 'Peugeot',   'Expert',   'taller'),
(4, '7777GHI', 'Volkswagen', 'Crafter',  'activo'),
(5, '3333JKL', 'Ford',       'Ranger',   'baja');

INSERT INTO itv VALUES
(1, 1, '2026-06-10', NULL,         'pendiente'),
(2, 2, '2026-07-20', 'favorable',  'ok'),
(3, 4, '2026-05-30', NULL,         'pendiente'),
(4, 3, '2026-08-15', NULL,         'pendiente');

INSERT INTO facturas VALUES
(1, 'ALD',    'Renting mensual',  3200.00, '2026-05-01'),
(2, 'ARVAL',  'Renting mensual',  1800.00, '2026-05-01'),
(3, 'ALD',    'Mantenimiento',     900.00, '2026-05-15'),
(4, 'ARVAL',  'Reparación',        450.00, '2026-05-20'),
(5, 'Repsol', 'Combustible',      1200.00, '2026-05-10'),
(6, 'Repsol', 'Combustible',       980.00, '2026-05-25');
