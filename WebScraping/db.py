import psycopg2


def connect():
    # Define your connection parameters
    params = {
        'database': 'scraping_app',
        'user': 'prwlr',
        'host': 'localhost',  # or another host if not local
        'port': 5432  # the default port for PostgreSQL
    }

    # Connect to the PostgreSQL server
    try:
        conn = psycopg2.connect(**params)
        print("Connected to the database successfully!")
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None


def fetch_all(conn):
    # Create a new cursor
    cur = conn.cursor()

    # Execute a statement
    cur.execute('SELECT band, city, date FROM events;')

    # Fetch the result
    all_rows = cur.fetchall()

    # Close the cursor
    cur.close()

    return all_rows


def query_by_date(conn, date):
    # Create a new cursor
    cur = conn.cursor()

    # Execute a statement
    cur.execute(f"SELECT * FROM events WHERE date = '{date}';")

    # Fetch the result
    events = cur.fetchall()

    # Close the cursor
    cur.close()

    return events


def insert(conn, new_rows):
    # Create a new cursor
    cur = conn.cursor()

    # Insert
    cur.executemany('INSERT INTO events (band, city, date) VALUES (%s, %s, %s);', new_rows)

    # Commit the transaction
    conn.commit()

    # Close the cursor
    cur.close()
