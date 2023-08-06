SELECT
  schedule.id as gameid,
  schedule.homeTeam.abbreviation as homeTeam,
  schedule.awayTeam.abbreviation as awayTeam,
  schedule.startTime,
  score.homeScoreTotal,
  score.awayScoreTotal,
  schedule.playedStatus,
  Season
FROM
  `sportsight-tests.NFL_Data.seasonal_games`
LEFT JOIN
  UNNEST (Seasondata.games)
where schedule.playedStatus = 'COMPLETED'
order by startTime desc