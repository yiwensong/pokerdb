/* sng_summary.sql */
DROP VIEW IF EXISTS  sng_summary;
CREATE VIEW sng_summary AS
SELECT sng_results.id,
  sng_results.time_played,
  sng_results.place,
  sng_types.name,
  sng_types.buyin,
  sng_types.rake,
  sng_types.players,
  sng_prizes.prize,
  sng_prizes.prize - sng_types.buyin - sng_types.rake AS pl
FROM ((sng_results
INNER JOIN sng_types ON sng_results.sng_id = sng_types.id)
LEFT JOIN sng_prizes ON sng_prizes.sng_id = sng_results.sng_id
  AND sng_prizes.place = sng_results.place) ORDER BY id;
