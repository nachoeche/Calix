CREATE TABLE IF NOT EXISTS "DataUnificada"
(
    cod_localidad bigint,
    id_provincia bigint,
    id_departamento bigint,
    categoria text,
    provincia text,
    localidad text,
    nombre text,
    domicilio text,
    codigo_postal text,
    numero_de_telefono text,
    mail text,
    web text,
    TimeStamp date
);

ALTER TABLE IF EXISTS public."DataUnificada"
    OWNER to postgres;