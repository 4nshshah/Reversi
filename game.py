from functions import *
from connection import *


print("started running")

displayArt()
gameboard = createBoard()
initialize(gameboard)


turnCount = 0
turnKey = "@"
moves = allMoves(gameboard)


print("Black, please enter your username:")
name1 = input()
print("White, please enter your username:")
name2 = input()
database, cursor = establishConnection()

print(
    """
STARTING GAME
...
...
...
"""
)
showBoard(gameboard)
# Game Loop
while moves != []:
    if turnCount % 2 == 0:
        turnKey = "@"
    else:
        turnKey = "O"

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
    print(
        f"""
White:                              Black:           
{white}                                   {black}"""
    )
    if white > black:
        winner = "O"
        loser = "@"
        win = white
        loss = black
    else:
        winner = "@"
        loser = "O"
        win = black
        loss = white

    scoreDiff = win - loss
    print(f"{winner} won by {scoreDiff} points!")

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

modifyTable(users[winner], "wins", 1, database, cursor)
modifyTable(users[winner], "score", scoreDiff, database, cursor)
modifyTable(users[winner], "total", 1, database, cursor)

modifyTable(users[loser], "total", 1, database, cursor)
modifyTable(users[loser], "score", -(scoreDiff), database, cursor)

displayLeaderboardAscending(database, cursor)
database.close()
cursor.close()
