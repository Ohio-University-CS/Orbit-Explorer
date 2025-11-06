import psycopg2
from config import config

def create_tables():
    commands = (
        #users
        """
        CREATE TABLE IF NOT EXISTS users ( 
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS visibility_requests (
            request_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(user_id) ON DELETE SET NULL,
            object_name VARCHAR(100) NOT NULL,
            input_temperature NUMERIC(6,2),
            input_date DATE NOT NULL,
            latitude NUMERIC(9,6),
            longitude NUMERIC(9,6),
            visible_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """ #visibility_requests
    )

    params = config()
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        conn.commit()
        cur.close()
        print("tables created.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error creating tables:", error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    create_tables()
