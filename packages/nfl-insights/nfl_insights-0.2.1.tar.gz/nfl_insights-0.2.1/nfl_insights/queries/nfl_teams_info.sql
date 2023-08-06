SELECT
  id AS teamId,
  name AS teamName,
  city,
  season,
  FORMAT('%s %s',city, name) AS teamFullname
FROM
  `sportsight-tests.NFL_Data.game_boxscore_*`
LEFT JOIN
  UNNEST ( references.teamReferences )
GROUP BY
  teamId,
  teamName,
  city,
  season
ORDER BY
  season DESC,
  teamId