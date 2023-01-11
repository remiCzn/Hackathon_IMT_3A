import json
import sys

import mariadb

cursor = None


def db_connect():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="herve",
            password="e92]sPW6FXhZ5y_)",
            host="db",
            port=3306,
            database="herve"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    global cursor
    cursor = conn.cursor()
    return conn


def db_close(conn):
    if conn:
        conn.close()


def send_request(request):
    cur = cursor
    cur.execute(request)
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)
    # Get Cursor
    # return conn.cursor()
