import mariadb
import sys

def db_connect():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="herve",
            password="e92]sPW6FXhZ5y_)",
            host="chillpaper.fr",
            port=3306,
            database="herve"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    return conn.cursor()
