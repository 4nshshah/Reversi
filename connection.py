def establishConnection():
    import mysql.connector
    mydb = mysql.connector.connect(
        host="localhost",
        username="root",
        password="ansh",
        database="othello"
    )
    cursor = mydb.cursor()

    return mydb, cursor


def addUser(db, cursor, username):
    sql = f"insert into leaderboard (user) values ('{username}')"
    cursor.execute(sql)
    db.commit()


def modifyTable(user, field, newValue, db, cursor):
    query = f"UPDATE leaderboard SET {field} = {field} + {newValue} WHERE user = '{user}'"
    cursor.execute(query)
    db.commit()


def displayLeaderboardAscending(db, cursor):

    sql = "SELECT *, wins/total as ratio FROM leaderboard ORDER BY score * wins desc"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    print("   USER   |   SCORE   |   WINS   |   TOTAL   |   RATIO   |")
    for x in myresult:
        for j in x:
            print(j, end='         ')
        print()


def getAllData(db, cursor):
    cursor.execute("SELECT * FROM leaderboard")
    return cursor.fetchall()
