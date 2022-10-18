CREATE TABLE IF NOT EXISTS "FiltroCategoria"
(
    categoria text,
    cantidad bigint,
    TimeStamp date
);

ALTER TABLE IF EXISTS public."FiltroCategoria"
    OWNER to postgres;