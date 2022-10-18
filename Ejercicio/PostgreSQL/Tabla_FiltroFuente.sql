CREATE TABLE IF NOT EXISTS "FiltroFuente"
(
    fuente text,
    cantidad bigint,
    TimeStamp date
);

ALTER TABLE IF EXISTS public."FiltroFuente"
    OWNER to postgres;