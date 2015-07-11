-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- Udacity NanoDegree Project 2 done by Wei-Chung Chen
--Tournament PostgreSQL database 

--create database tournament and connect it
DROP DATABASE IF EXISTS tournament; 
CREATE DATABASE tournament;
\c tournament;

--create table player to store players' information
CREATE TABLE player(
	                p_id  serial primary key,
                    name varchar(30)
);


--create table matches to store matches' result

CREATE TABLE matches(
                     m_id serial primary key,	                 
	                 winner int references player(p_id),
	                 loser int references player(p_id)
                    
	);


---create table SwissPairing to store swisspairing result
CREATE TABLE swissPairing(  
	                      id1 int, 
	                      name1 varchar(30),
	                      id2 int,
	                      name2 varchar(30),
	                      primary key(id1,id2)

);

--create a view for showing the player standings
CREATE VIEW view_player_standing AS SELECT A.p_id, A.name, 
COUNT(B.winner) AS Total_number_of_win, 
COALESCE((SELECT COUNT(A.p_id) FROM matches AS C, player AS A 
WHERE C.winner = A.p_id OR C.loser = A.p_id 
GROUP BY p_id ORDER BY p_id LIMIT 1), 0) AS Total_number_of_matches
FROM player AS A 
LEFT OUTER JOIN matches AS B
ON A.p_id = B.winner 
GROUP BY A.p_id, A.name
ORDER BY  COUNT(B.winner) DESC;





