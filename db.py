import json
import MySQLdb

txt = json.loads()

iphost = txt["iphost"]

hostname = txt["hostname"]

password = txt["password"]

database = txt["database_name"]

def execute(k):
    connection = MySQLdb.connect(iphost, hostname, password, database)

    cursor = connection.cursor()

    cursor.execute(k)

    connection.commit()

    connection.close()


def fetchone(k):
    connection = MySQLdb.connect(iphost, hostname, password, database)

    cursor = connection.cursor()

    cursor.execute(k)

    b = cursor.fetchone()

    connection.commit()

    connection.close()

    return b