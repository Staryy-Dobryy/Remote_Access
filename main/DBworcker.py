import sqlite3
from sqlite3 import Error
from datetime import datetime

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
    sql = "CREATE TABLE IF NOT EXISTS users(systemName text, IPaddr text, status text);"
    connection.execute(sql)

def prepareDb(name):
    conn = init_conn(name)
    init_tables(conn)
    conn.close()

def addData(db, data):
    connection = init_conn(db)
    requestIPs = getStatus(db)
    print("try set")
    print(requestIPs[0])
    if data[2] in requestIPs:
        print("seted status")
        sql = "UPDATE users SET status = '{}' WHERE IPaddr = '{}'".format(data[3], data[2])
    else:
        sql = "INSERT INTO users(`systemName`, `IPaddr`, `status`) VALUES('{}', '{}', '{}')".format(data[1], data[2], data[3])
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    print("seted")
    connection.close()

def getStatus(db):
    connection = init_conn(db)
    sql = "SELECT IPaddr FROM users;"
    cursor = connection.cursor()
    cursor.execute(sql)
    IPs = cursor.fetchall()
    connection.close()
    return IPs

def getData(db):
    connection = init_conn(db)
    sql = "SELECT * FROM users;"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.close()
    return rows