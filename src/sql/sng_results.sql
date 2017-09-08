/* sng_results.sql */
DROP TABLE IF EXISTS sng_results;
CREATE TABLE sng_results (
  id SERIAL,
  sng_id int,
  time_played TIMESTAMP,
  place int,
  PRIMARY KEY(id)
);
