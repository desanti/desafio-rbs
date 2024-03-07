-- DW E PERMISSÕES

CREATE DATABASE dw_desafio_rbs;

GRANT ALL PRIVILEGES ON DATABASE dw_desafio_rbs TO desafio_rbs;

-- TABELA DE USUÁRIO

CREATE TABLE IF NOT EXISTS fact_user (
    id bigserial NOT NULL,
    gender VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    country VARCHAR NOT NULL,
    date_of_birth DATE,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
	CONSTRAINT pk_random_user PRIMARY KEY (id)
);

ALTER TABLE fact_user OWNER TO desafio_rbs;
GRANT ALL ON TABLE fact_user TO desafio_rbs;
GRANT SELECT ON TABLE fact_user TO desafio_rbs;
