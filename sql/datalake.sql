-- DATABASE E PERMISSÕES

CREATE DATABASE desafio_rbs;

CREATE USER desafio_rbs WITH PASSWORD 'desafio_rbs';
GRANT ALL PRIVILEGES ON DATABASE desafio_rbs TO desafio_rbs;

-- RAW

CREATE SCHEMA IF NOT EXISTS raw AUTHORIZATION desafio_rbs;

CREATE TABLE IF NOT EXISTS raw.user (
    id bigserial NOT NULL,
    event json NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
	CONSTRAINT pk_random_user PRIMARY KEY (id)
);

ALTER TABLE raw.user OWNER TO desafio_rbs;
GRANT ALL ON TABLE raw.user TO desafio_rbs;
GRANT SELECT ON TABLE raw.user TO desafio_rbs;


-- CURATED

CREATE SCHEMA IF NOT EXISTS curated AUTHORIZATION desafio_rbs;

CREATE TABLE IF NOT EXISTS curated.user (
    id bigserial NOT NULL,
    gender VARCHAR NOT NULL,
    title_name VARCHAR,
    firstname VARCHAR NOT NULL,
    lastname VARCHAR NOT NULL,
    street_name VARCHAR,
    street_number INTEGER,
    city VARCHAR,
    state VARCHAR,
    country VARCHAR NOT NULL,
    postcode VARCHAR,
    latitude VARCHAR,
    longitude VARCHAR,
    tz_offset VARCHAR,
    tz_description VARCHAR,
    date_of_birth timestamp,
    email VARCHAR,
    phone VARCHAR,
    cell VARCHAR,
    nat VARCHAR,
    registered_date timestamp,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
	CONSTRAINT pk_random_user PRIMARY KEY (id)
);

ALTER TABLE curated.user OWNER TO desafio_rbs;
GRANT ALL ON TABLE curated.user TO desafio_rbs;
GRANT SELECT ON TABLE curated.user TO desafio_rbs;
