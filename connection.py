import mysql.connector
from tabulate import tabulate


def establishConnection(password):
    mydb = mysql.connector.connect(
        host="localhost",
        user='root',
        password=password,
        database="othello"
    )
    cursor = mydb.cursor()

    return mydb, cursor


def createDatabase(password):
    mydb = mysql.connector.connect(
        host="localhost",
        user='root',
        password=password

    )
    cursor = mydb.cursor()
    cursor.execute('create database if not exists othello')
    cursor.execute('use othello')
    cursor.execute(
        'create table if not exists leaderboard (user varchar(255), score integer default 0, wins integer default 0, total integer default 0)')
    mydb.close()
    cursor.close()


def addUser(db, cursor, username):
    sql = f"insert into leaderboard (user) values ('{username}')"
    cursor.execute(sql)
    db.commit()


def modifyTable(user, field, newValue, db, cursor):
    query = f"UPDATE leaderboard SET {field} = {field} + {newValue} WHERE user = '{user}'"
    cursor.execute(query)
    db.commit()


def displayLeaderboardAscending(db, cursor):

    def pdtabulate(df): return tabulate(
        df, headers='firstrow', tablefmt='psql')

    sql = "SELECT *, wins/total as ratio FROM leaderboard ORDER BY score * wins desc"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    myresult = [['USERNAME', 'SCORE', 'WINS', 'TOTAL', 'RATIO']] + myresult
    print(pdtabulate(myresult))


def getAllData(db, cursor):
    cursor.execute("SELECT * FROM leaderboard")
    return cursor.fetchall()
