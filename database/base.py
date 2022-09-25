from __future__ import annotations
from models import *
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

    def seed_db(self):
        # Table banks
        self.add_seed('banks', {
            "brand": "BTG Pactual",
            "cnpj": "12345678901234",
        })

        self.add_seed('banks', {
            "brand": "NuBank",
            "cnpj": "19283192321312",
        })

        self.add_seed('banks', {
            "brand": "Itau Unibanco",
            "cnpj": "12928912932231",
        })

        # Table clients
        self.add_seed("clients", {
            "customer_id": "44801389864",
            "banks_ids": [0, 1, 2],
            "investments_ids": [0, 1]
        })

        self.add_seed("clients", {
            "customer_id": "19293829293",
            "banks_ids": [2],
            "investments_ids": [3]
        })

        # Table investments
        self.add_seed("investments", {
            "bank_id": 0,
            "name": None,
            "itype": None,
            "exempt": None,
            "interest_rate": None,
            "sell_date": None,
            "date": None,
            "price": None,
            "rate": None
        })

        self.add_seed("investments", {
            "bank_id": 1,
            "name": None,
            "itype": None,
            "exempt": None,
            "interest_rate": None,
            "sell_date": None,
            "date": None,
            "price": None,
            "rate": None
        })

        self.add_seed("investments", {
            "bank_id": 2,
            "name": None,
            "itype": None,
            "exempt": None,
            "interest_rate": None,
            "sell_date": None,
            "date": None,
            "price": None,
            "rate": None
        })

        # Table profit_loss
        # self.add_seed('profit_loss', {
        #    "customer_id": "44801389864",
        #    "day_trade_profit": None,
        #    "swing_trade_profit": None,
        #    "cripto_profit": None,
        #    "fi_profit": None,
        #    "day_trade_accumulated_loss": None,
        #    "swing_trade_accumulated_loss": None,
        #    "fi_loss": None,
        #    "cripto_accumulated_loss": None,
        #    "acumulated_loss": None,
        #    "date": None
        # })

        # self.add_seed('profit_loss', {
        #    "customer_id": "44801389864",
        #    "day_trade_profit": None,
        #    "swing_trade_profit": None,
        #    "cripto_profit": None,
        #    "fi_profit": None,
        #    "day_trade_accumulated_loss": None,
        #    "swing_trade_accumulated_loss": None,
        #    "fi_loss": None,
        #    "cripto_accumulated_loss": None,
        #    "acumulated_loss": None,
        #    "date": None
        # })

        # self.add_seed('profit_loss', {
        #    "customer_id": "44801389864",
        #    "day_trade_profit": None,
        #    "swing_trade_profit": None,
        #    "cripto_profit": None,
        #    "fi_profit": None,
        #    "day_trade_accumulated_loss": None,
        #    "swing_trade_accumulated_loss": None,
        #    "fi_loss": None,
        #    "cripto_accumulated_loss": None,
        #    "acumulated_loss": None,
        #    "date": None
        # })

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

    def add_seed(self, table: str, data: dict) -> None:
        """Add seed data to a table"""
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO {} ({}) VALUES ({})".format(
                table, ", ".join(data.keys()), ", ".join(["%s"] * len(data))), list(data.values()))
            self.conn.commit()
        except Exception as e:
            print("Query failed due to {}".format(e))

    def setup(self) -> None:
        """Setup the database"""
        print("Setting up the database...")
        self.run_sql_from_file("database/sql_assets/schema.sql")
        print("Database setup complete!")
        print("\n")
        print("Want to add seed data? Y/N")
        if input().lower() == "y":
            self.seed_db()
            print("Seed data added!")
        else:
            print("Skipping seed data...")

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
    def __init__(self, table: object) -> None:
        self.table = table
        self.query = ""
        self.result = None

    def select(self, columns: list = None) -> QueryConstructor:
        """Select columns"""
        if columns is None:
            self.query += "SELECT * FROM {}".format(self.table.__table__)
        else:
            self.query += "SELECT {} FROM {}".format(
                ", ".join(columns), self.table.__table__)
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
            column, ",".join(map(str, array)))
        return self

    def execute(self,  params: tuple = None) -> list:
        """Execute the query"""
        self.results = db.execute(self.query, params)
        self.results = self.results if self.results is not None else []

        self.items = [i for i in self.table.headers()]
        for item in self.items:
            if item.startswith("_"):
                self.items.remove(item)

        self.results = [dict(zip(self.items, i)) for i in self.results]


# Create database object instance
db = Database()  # Create a database object
db.setup()  # Setup the database
