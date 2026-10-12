-- Infrastructure checks only; not migration, tenant, routing, or concurrency tests.
\pset pager off
\echo PostgreSQL/PostGIS infrastructure preflight
SELECT current_database() AS database_name, version() AS server_version;
SELECT PostGIS_Full_Version() AS postgis_version;
BEGIN READ ONLY;
DO $$
DECLARE
    distance_m double precision;
BEGIN
    IF current_database() <> 'claim2car_test' THEN
        RAISE EXCEPTION 'Preflight restricted to claim2car_test';
    END IF;
    IF current_setting('server_version_num')::integer / 10000 <> 16 THEN
        RAISE EXCEPTION 'Expected PostgreSQL major version 16';
    END IF;
    distance_m := ST_Distance(
        ST_SetSRID(ST_MakePoint(-98.4936, 29.4241), 4326)::geography,
        ST_SetSRID(ST_MakePoint(-98.4936, 29.4241), 4326)::geography
    );
    IF distance_m IS DISTINCT FROM 0.0 THEN
        RAISE EXCEPTION 'Identical synthetic points did not return zero distance';
    END IF;
    RAISE NOTICE 'PASS: isolated database name, PostgreSQL major version, PostGIS geography execution';
END $$;
ROLLBACK;
\echo Preflight finished; business acceptance gates remain pending.
