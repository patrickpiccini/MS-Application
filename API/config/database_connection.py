import psycopg2
import os

HOST_DATABSE = os.environ['HOST_DATABASE']
# HOST_DATABSE = '144.22.193.219'

class ConnectionDatabase():

    def __init__(self):
        try:
            self.connection  = psycopg2.connect(
                host=HOST_DATABSE,
                port=5432,
                database="baseapplication",
                user="postgres",
                password="postgres")
            self.cursor = self.connection.cursor()
            # start tables
            self.create_tables()
            print('[✓] Connected to Postgres')
        except Exception as error:
            print(f'[X] CONNECTING POSTGRES ERROR: {error}')
    
    def create_tables(self):
        self.cursor.execute("SELECT version();")
        record = self.cursor.fetchone()
        print("[✓] You are connected to - ", record)

        create_table_query = '''
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL NOT NULL,
                nick_name varchar(50) UNIQUE NOT NULL,
                password varchar(256) NOT NULL,
                full_name varchar(50) NOT NULL,
                cpf varchar(11) NOT NULL,
                email varchar(50) NOT NULL,
                phone_number varchar(50) NOT NULL,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                PRIMARY KEY (user_id)
            );

            CREATE TABLE IF NOT EXISTS orders (
                order_id SERIAL NOT NULL,
                user_id integer NOT NULL,
                item_description varchar(256) NOT NULL,
                item_quantity integer NOT NULL,
                item_price integer NOT NULL,
                total_value integer NOT NULL,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                PRIMARY KEY (order_id),
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            );'''
        
        self.cursor.execute(create_table_query)
        self.connection.commit()
        print('[✓] Created tables on DataBase')

        