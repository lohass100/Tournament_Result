#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
# Udacity Nanodegree project 2 Done By Wei-Chung Chen

import psycopg2
import sys
import pprint


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    DB = psycopg2.connect("dbname=tournament")
    return DB


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    DB.commit()
    print 'delete all matches\' records'


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM player CASCADE")
    DB.commit()
    print 'delete all player'

 
def deleteSwissPairing():
    """Remove all the swissPairings' records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM swissPairing CASCADE")
    DB.commit()
    print 'delete all swissPairing'


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT name, COUNT(name) as num FROM player GROUP BY name")
    num = c.rowcount
    return num


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO player(name) VALUES (%s);", (name,))
    DB.commit()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,\
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT *FROM view_player_standing")
    records = c.fetchall()
    pprint.pprint(records)
    return records


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches(winner, loser) VALUES(%s, %s);",\
    (winner, loser,))
    DB.commit()


def swissPairings():
#Return a list of pairs of players for the next round of a match.

    """Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    DB = connect()
    c = DB.cursor()
    standings = playerStandings()
    playerNum = countPlayers()
    print 'total number of players: ' + str(playerNum)  
    pairingNum = playerNum/2
    print 'total number of pairings: ' + str(pairingNum)
    idTup = [row[0] for row in standings]
    nameTup = [row[1] for row in standings]
    winTup = [row[2] for row in standings]
    matchTup = [row[3] for row in standings]

# test for-loop function     
    for i in range(0, playerNum, +1):

      print 'id: ' + str(idTup[i]) + ' name: ' + str(nameTup[i])   + ' wins: ' + str(winTup[i]) +' matches: '+ str(matchTup[i])

  
    print "*******************"
    """pairing algorithm"""
    j = 0
    for i in range(0, playerNum, +1):
      
       while (winTup[i] != winTup[j]):
        j += 1
       
       if (idTup[i] != idTup[j]):
        print 'j: ' + str(j)
        print nameTup[i]+str(winTup[i])+" wins" + ","\
        + nameTup[j]+ str(winTup[j])+" wins"

        pairingsTup= [idTup[i], nameTup[i], idTup[j], nameTup[j]]
        print pairingsTup
        DB = connect()
        c = DB.cursor()
        c.execute("INSERT INTO swissPairing VALUES(%s, %s, %s, %s);", (idTup[i], nameTup[i], idTup[j], nameTup[j]))
        DB.commit()

    """return value"""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT *FROM swissPairing")  
    swissPairingResults = c.fetchall()
    pprint.pprint(swissPairingResults)
    return swissPairingResults
