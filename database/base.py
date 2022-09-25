from __future__ import annotations
import psycopg2
import sys
import boto3
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


class Database:
    def __init__(self) -> None:
        try:
            print("Connecting to database with environment: {}".format(
                os.getenv("PYTHON_ENV")))
            if os.getenv('PYTHON_ENV') == 'production':  # If the environment is production
                session = boto3.Session(
                    profile_name='RDSCreds')  # AWS profile name
                client = session.client('rds')  # AWS RDS client

                # Get the credentials from AWS with the RDS / AWS info
                token = client.generate_db_auth_token(DBHostname=os.getenv("AWS_ENDPOINT"), Port=os.getenv(
                    "AWS_PORT"), DBUsername=os.getenv("AWS_USER"), Region=os.getenv("AWS_REGION"))

                # Connect to the database with the credentials
                self.conn = psycopg2.connect(host=os.getenv("AWS_ENDPOINT"), port=os.getenv("AWS_PORT"), database=os.getenv("AWS_DBNAME"),
                                             user=os.getenv("AWS_USER"), password=token, sslrootcert="SSLCERTIFICATE")
            else:
                # Connect to the database with the local (development) credentials
                self.conn = psycopg2.connect(host=os.getenv("L_HOST"), port=os.getenv("L_PORT"), database=os.getenv("L_DBNAME"),
                                             user=os.getenv("L_USERNAME"), password=os.getenv("L_PASSWORD"))
            if __name__ == "__main__":  # Verify if the script is being executed directly
                # Debug the connection to test if it's working correctly
                cur = self.conn.cursor()
                cur.execute("""SELECT now()""")
                query_results = cur.fetchall()
                print(query_results)

        except Exception as e:
            print("Database connection failed due to {}".format(e))

    def run_sql_from_file(self, filepath: str) -> None:
        """Run a SQL file"""

        # Open and read the file as a single buffer
        fd = open(filepath, 'r')
        sql_file = fd.read()
        fd.close()

        # All SQL commands (split on ';')
        sql_commands = sql_file.split(';')

        # Execute every command from the input file
        for command in sql_commands:
            try:
                if command.strip() != '':
                    self.conn.cursor().execute(command)
                    self.conn.commit()

            except Exception as e:
                print("Command skipped: {} due to:\n{}".format(command, e))

    def setup(self) -> None:
        """Setup the database"""
        print("Setting up the database...")
        self.run_sql_from_file("database/sql_assets/schema.sql")
        print("Database setup complete!")

    def execute(self, query: str, params: tuple = None) -> list:
        """Execute a query"""
        try:
            cur = self.conn.cursor()
            cur.execute(query, params)
            self.conn.commit()
            return cur.fetchall()
        except Exception as e:
            print("Query failed due to {}".format(e))


class QueryConstructor:
    def __init__(self, table: str) -> None:
        self.table = table
        self.query = ""
        self.result = None

    def select(self, columns: list = None) -> QueryConstructor:
        """Select columns"""
        if columns is None:
            self.query += "SELECT * FROM {}".format(self.table)
        else:
            self.query += "SELECT {} FROM {}".format(
                ", ".join(columns), self.table)
        return self

    def where(self, column: str, operator: str, value: str) -> QueryConstructor:
        """Add a where clause"""
        self.query += " WHERE {} {} '{}'".format(column, operator, value)
        return self

    def and_(self, column: str, operator: str, value: str) -> QueryConstructor:
        """Add an and clause"""
        self.query += " AND {} {} '{}'".format(column, operator, value)
        return self

    def or_(self, column: str, operator: str, value: str) -> QueryConstructor:
        """Add an or clause"""
        self.query += " OR {} {} '{}'".format(column, operator, value)
        return self

    def limit(self, limit: int) -> QueryConstructor:
        """Add a limit clause"""
        self.query += " LIMIT {}".format(limit)
        return self

    def get_query(self) -> str:
        """Get the query"""
        return self.query

    def where_in_array(self, column: str, array: list) -> QueryConstructor:
        """Add a where in array clause"""
        self.query += " WHERE {} = ANY(ARRAY[{}])".format(
            column, ", ".join(array))
        return self

    def inner_join(self, table: str, column1: str, column2: str, alias: str = None) -> QueryConstructor:
        """Add an inner join clause"""
        if alias is None:
            self.query += " INNER JOIN {} ON {} = {}".format(
                table, column1, column2)
        else:
            self.query += " INNER JOIN {} AS {} ON {} = {}".format(
                table, alias, column1, column2)
        return self

    def execute(self,  params: tuple = None) -> list:
        """Execute the query"""
        self.result = db.execute(self.query, params)


if __name__ == "__main__":  # Verify if the script is being executed directly
    database = Database()  # Create a database object
    database.setup()  # Setup the database

# Create database object instance
db = Database()  # Create a database object
db.setup()  # Setup the database
