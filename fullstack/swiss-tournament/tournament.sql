-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- The next lines of code bring you into the database and drop any tables and views that
-- were left over from previous tests
\c tournament
DROP VIEW IF EXISTS standings;
DROP VIEW IF EXISTS count_matches;
DROP VIEW IF EXISTS count_wins;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

-- Creates a table where all of the players will be located in
CREATE TABLE players (
	id SERIAL primary key,
	name text
);

-- Creates a table where all of the matches will be recorded in
CREATE TABLE matches (
	player1 SERIAL references players(id),
	player2 SERIAL references players(id)
);


-- Creates a view which counts the number of wins for each player
CREATE VIEW count_wins as SELECT players.id, COUNT(matches.player1) as wins from players
LEFT JOIN matches on players.id = matches.player1 group by players.id;

-- Creates view to count the number of matches each player has played
CREATE VIEW count_matches as SELECT players.id, count(matches.player2) as num from players
LEFT JOIN matches on players.id = matches.player2 or players.id = matches.player1 group by players.id;

-- Creates a view which shows the current standings of all of the players
-- the columns being:
--  id | name | wins | matches
CREATE VIEW standings as SELECT
players.id, players.name, count_wins.wins, count_matches.num as matches
FROM players, count_matches, count_wins WHERE players.id = count_matches.id and count_matches.id = count_wins.id order by wins desc;
