import os
import mysql.connector
from mysql.connector import Error


def connect():
    """ Connect to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(host='xtract-adventure-db-1',
                                       database=os.environ['MYSQL_DATABASE'],
                                       user=os.environ['MYSQL_USER'],
                                       password=os.environ['MYSQL_PASSWORD'])

        if conn.is_connected():
            print('Connection established.')
            return conn
        else:
            print('Connection failed.')
            return null

    except Error as error:
        print(error)

def query_with_fetchall():
    try:
        conn = connect()

        cursor = conn.cursor()
        cursor.execute("select * from employee")
        rows = cursor.fetchall()

        print('Total Employee(s):', cursor.rowcount)
        for row in rows:
            print(row)

        cursor = conn.cursor()
        cursor.execute("select * from event")
        rows = cursor.fetchall()

        print('Total Event:', cursor.rowcount)
        for row in rows:
            print(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
if __name__ == '__main__':
    query_with_fetchall()