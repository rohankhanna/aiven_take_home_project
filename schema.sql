CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TABLE IF EXISTS availability CASCADE;
DROP TABLE IF EXISTS websites CASCADE;

CREATE TABLE IF NOT EXISTS websites (
    id INT GENERATED ALWAYS AS IDENTITY,
    url VARCHAR NOT NULL,    
    content TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY(id)
);

CREATE TRIGGER set_timestamp_websites
BEFORE UPDATE ON websites
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();


CREATE TABLE IF NOT EXISTS availability (
    id INT GENERATED ALWAYS AS IDENTITY,
    website_id INT,
    content TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY(id),
    CONSTRAINT fk_website
      FOREIGN KEY(website_id) 
      REFERENCES websites(id)
      ON DELETE SET NULL
);

CREATE TRIGGER set_timestamp_availability
BEFORE UPDATE ON availability
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();