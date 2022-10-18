CREATE TABLE IF NOT EXISTS "Cines"
(
    id_provincia bigint,
    pantallas bigint,
    butacas bigint,
    espacio_incaa text,
    TimeStamp date
);

ALTER TABLE IF EXISTS public."Cines"
    OWNER to postgres;