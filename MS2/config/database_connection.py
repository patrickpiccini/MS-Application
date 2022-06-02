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
            print('[✓] Connected to Postgres')
        except Exception as error:
            print(f'[X] CONNECTING POSTGRES ERROR: {error}')
        

    def select_version(self):
        print("PostgreSQL server information")
        print(self.connection.get_dsn_parameters())
        self.cursor.execute("SELECT version();")

        record = self.cursor.fetchone()
        print("[✓] You are connected to - ", record, "\n")
        self.cursor.close()
  