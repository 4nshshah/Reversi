from functions import *
from connection import *
import mysql.connector
from tabulate import tabulate
import os
import random

print("Please enter your MySQL password")
password = input()
createDatabase(password)
displayArt()
database, cursor = establishConnection(password)


turnCount = 0
turnKey = '@'


print("Black, please enter your username:")
name1 = input()
print("White, please enter your username:")
name2 = input()

frenzy = False
if name1 == name2 == 'switch up':
    frenzy = True


# Game Loop
gameKey = 'y'
while gameKey == 'y':
    gameboard = createBoard()
    initialize(gameboard)
    showBoard(gameboard)
    moves = allMoves(gameboard)

    while moves != []:
        if frenzy:
            turnCount += random.randint(0, 5)

        if turnCount % 2 == 0:
            turnKey = '@'
        else:
            turnKey = 'O'

        moveEntered = getMovePlayed(gameboard, turnKey)
        if moveEntered == 0:
            turnCount += 1
            continue
        flippingPoints = checkMove(gameboard, moveEntered, turnKey)
        flipPieces(gameboard, moveEntered, flippingPoints, turnKey)
        showBoard(gameboard)
        turnCount += 1
        moves = allMoves(gameboard)

    # End game sequence
    else:
        white, black = getScore(gameboard)
        print(f"""
    White:                              Black:           
    {white}                                   {black}""")
        if white > black:
            winner = 'O'
            loser = "@"
            win = white
            loss = black
        else:
            winner = '@'
            loser = "O"
            win = black
            loss = white

        scoreDiff = win-loss
        print(f"{winner} won by {scoreDiff} points!")

    print("Press y to play again.")
    gameKey = input().lower()


# SQL connectivity
users = {"@": name1, "O": name2}
usernames = []
allData = getAllData(database, cursor)
for i in allData:
    usernames.append(i[0])

names = [name1, name2]
for i in names:
    if i not in usernames:
        addUser(database, cursor, i)
    allData = getAllData(database, cursor)
    for i in allData:
        usernames.append(i[0])

modifyTable(users[winner], 'wins', 1, database, cursor)
modifyTable(users[winner], 'score', scoreDiff, database, cursor)
modifyTable(users[winner], 'total', 1, database, cursor)

modifyTable(users[loser], 'total', 1, database, cursor)
modifyTable(users[loser], 'score', -(scoreDiff), database, cursor)

print("To display the leaderboard, enter 'leaderboard'")
if input().lower() == 'leaderboard':
    displayLeaderboardAscending(database, cursor)
database.close()
cursor.close()
