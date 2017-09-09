/* sng_types.sql */
DROP TABLE IF EXISTS sng_types CASCADE;
CREATE TABLE sng_types (
  id SERIAL,
  date_added DATE,
  name VARCHAR(64),
  buyin float,
  rake float,
  players int,
  PRIMARY KEY(id)
);

DROP TABLE IF EXISTS sng_prizes;
CREATE TABLE sng_prizes (
  sng_id int,
  place int,
  prize float,
  PRIMARY KEY(sng_id, place)
);
