import psycopg2
from config import config

def create_users_table():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    params = config()
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(create_table_sql)
        conn.commit()
        cur.close()
        print("users table created.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error creating users table:", error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    create_users_table()

