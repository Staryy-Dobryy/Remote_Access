import sqlite3
from sqlite3 import Error
from datetime import datetime

class users:
    def __init__(self, systemName, IPaddr):
        self.systemName = systemName
        self.IPaddr = IPaddr
        self.status = "OFFLINE"

def init_conn(path):
    conn = None
    try:
        conn = sqlite3.connect(path)
        print ("Connection established!")
    except Error as e:
        print (e)
        print ("Connection failed!")
    return conn    

def init_tables(connection):
    sql = "CREATE TABLE IF NOT EXISTS users(systemName text, IPaddr text);"
    connection.execute(sql)

def prepareDb(name):
    conn = init_conn(name)
    init_tables(conn)
    conn.close()

def addData(db, data):
    connection = init_conn(db)
    sql = "INSERT INTO users(`systemName`, `IPaddr`) VALUES('{}', '{}')".format(data[1], data[2])
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()

def getData(db):
    connection = init_conn(db)
    sql = "SELECT * FROM users;"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.close()
    return rows

def getObjects(db):
    # Returns data about users
    objects = []
    data = getData(db)
    for obj in data:
        objects.append(users(obj[0], obj[1]))
    return objects
