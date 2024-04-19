import sqlite3
from datetime import datetime, timedelta


# use with the server

# function to connect to a sqlite3 database


def connect_sqlite3(dbname):
    connection = sqlite3.connect(dbname, check_same_thread=False)
    # connect to the database file with the given name
    return connection
    # return the connection object


# function to execute a database change command
def db_change(connection, sql):
    cursor = connection.cursor()
    # create a cursor object for database operations
    cursor.execute(sql)
    # execute the given SQL command
    connection.commit()
    # commit the changes made to the database


# function to execute a database query command
def db_query(connection, sql):
    cursor = connection.cursor()
    # create a cursor object for database operations
    cursor.execute(sql)
    # execute the given SQL command
    rows = cursor.fetchall()
    # fetch all rows returned by the command
    return rows
    # return the rows fetched from the database


# create a connection to the 'Usersdb.db' database file

connection = connect_sqlite3("Usersdb.db")

# create a SQL command to create the 'users' table if it does not exist
sql = """ CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT,
    MAC_ADD TEXT,
    call_1 TEXT,
    call_2 TEXT,
    call_3 TEXT,
    call_4 TEXT,
    call_5 TEXT
    );
"""

# execute the 'CREATE TABLE' command
db_change(connection, sql)


# function to add a new call record to a user's call history
def add_call(name, data):
    # create a SQL command to retrieve the current call history of the given user
    sql = f"""SELECT call_1, call_2, call_3, call_4, call_5 FROM users WHERE username = '{name}'"""
    # execute the SQL command and get the result
    row = db_query(connection, sql)
    # convert the result to a string and count the number of non-null fields
    row = str(row)
    count = 5 - row.count("None")
    # split the string by double quotes and extract the non-null fields
    row = row.split('"')
    lst = []
    i = 1
    while count > 0:
        lst.append(row[i])
        i += 2
        count -= 1
    # fill the remaining fields with None
    i = (i - 1) / 2 + 1
    while i > 0:
        lst.append(None)
        i -= 1
    # if the first field is None, update it with the new call record
    if lst[0] is None:
        sql = f"""UPDATE users SET call_1 = "{data}" WHERE username = "{name}";"""
        db_change(connection, sql)
        return True
    # if the first field is not None, shift the call history to the right and insert the new record
    for i in range(1, 6):
        if lst[i] is None or i == 5:
            for j in range(i - 1, -1, -1):
                if j != 4:
                    table = "call_" + str(j + 2)
                    sql = f"""UPDATE users SET {table} = "{lst[j]}" WHERE username = "{name}";"""
                    db_change(connection, sql)
            sql = f"""UPDATE users SET call_1 = "{data}" WHERE username = "{name}";"""
            db_change(connection, sql)
            return True


# add_call("username","1/2/23","12:43:22","01:30:02","ano_name")


def add_new_user(username, password, MAC):
    # First, we check if the user already exists in the database
    sql = """SELECT * FROM users"""
    rows = db_query(connection, sql)
    for row in rows:
        if row[0] == username:
            return False

    # If the user does not exist, we insert a new row into the table with the given details
    sql = f"""INSERT INTO users (username,password,MAC_ADD) VALUES ("{username}","{password}","{MAC}");"""
    db_change(connection, sql)
    return True


def update_time(name, lst, end_time):
    # We first parse the start and end times from the given list and end_time
    fmt = '%H:%M:%S'  # format string for parsing times
    start = datetime.strptime(lst[2], fmt)  # parse start time
    end = datetime.strptime(end_time, fmt)  # parse end time

    # We then calculate the time difference and convert it to a string
    diff = end - start  # calculate time difference
    time_diff = str(timedelta(seconds=diff.total_seconds()))  # convert to timedelta string

    # Finally, we update the relevant row in the database with the updated time difference
    lst[2] = time_diff
    sql = f"""UPDATE users SET call_1 = "{lst}" WHERE username = "{name}";"""
    db_change(connection, sql)


def check_password(name, password, MAC):
    # We retrieve the row corresponding to the given username
    # from the database and check if the password and MAC address match
    sql = """SELECT * FROM users"""
    rows = db_query(connection, sql)
    for row in rows:
        if row[0] == name and row[1] == password and row[2] == MAC:
            return True
    return False


def update_min(name, lst):
    # We update the relevant row in the database with the given list of call details
    sql = f"""UPDATE users SET call_1 = "{lst}" WHERE username = "{name}";"""
    db_change(connection, sql)


def last_calls(table, name):
    # We retrieve the row corresponding to the given username from the
    # database and extract the list of call details for the given table
    table = "call_" + str(table)
    sql = f"""SELECT ({table}) FROM users WHERE username = '{name}'"""
    rows = db_query(connection, sql)

    # If the row exists and contains a non-null value for the given table,
    # we extract the list of call details from the string format used in the database and return it
    if rows != [(None,)]:
        row = str(rows)
        row = row.split('"')
        new_str = row[1]
        new_str = new_str[1:-1]
        new_lst = new_str.split(',')
        return new_lst