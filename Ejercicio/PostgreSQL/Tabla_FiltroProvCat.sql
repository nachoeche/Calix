CREATE TABLE IF NOT EXISTS "FiltroProvCat"
(
    ProvCat text,
    cantidad bigint,
    TimeStamp date
);

ALTER TABLE IF EXISTS public."FiltroProvCat"
    OWNER to postgres;