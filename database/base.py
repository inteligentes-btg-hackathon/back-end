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
                session = boto3.Session()  # AWS profile name
                client = session.client('rds')  # AWS RDS client

                # Get the credentials from AWS with the RDS / AWS info
                token = client.generate_db_auth_token(DBHostname=os.getenv("AWS_ENDPOINT"), Port=os.getenv(
                    "AWS_PORT"), DBUsername=os.getenv("AWS_USER"),  password=os.getenv("AWS_PASSWORD"), Region=os.getenv("AWS_REGION"))

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
            "banks_ids": [0, 1],
            "investments_ids": [1, 2, 3, 4, 5, 6]
        })

        # Table investments
        self.add_seed("investments", {
            "bank_id": 0,
            "name": "brd2",
            "itype": "ação",
            "exempt": False,
            "sell_date": "2023-02-01",
            "buy_date": "2023-01-01",
            "price": 1000,
            "rate": None,
            "sell_price": 1100,
            "buy_price": 1000,
        })

        # Table investments
        self.add_seed("investments", {
            "bank_id": 0,
            "name": "brd2",
            "itype": "ação",
            "exempt": False,
            "sell_date": None,
            "buy_date": "2023-01-01",
            "price": 995,
            "rate": 10,
            "sell_price": 400,
            "buy_price": 500,
        })

        self.add_seed("investments", {
            "bank_id": 1,
            "name": "bras3",
            "itype": "ação",
            "exempt": False,
            "sell_date": "2023-02-03",
            "buy_date": "2023-01-01",
            "price": 500,
            "rate": 20,
            "sell_price": 322,
            "buy_price": 233,
        })

        self.add_seed("investments", {
            "bank_id": 1,
            "name": "bras3",
            "itype": "ação",
            "exempt": False,
            "sell_date": None,
            "buy_date": "2023-09-01",
            "price": 510,
            "rate": 20,
            "sell_price": 12300,
            "buy_price": 12500,
        })

        self.add_seed("investments", {
            "bank_id": 2,
            "name": "btg",
            "itype": "fundo_imobiliário",
            "exempt": False,
            "sell_date": "2023-04-03",
            "buy_date": "2023-01-01",
            "price": 100,
            "rate": 0,
            "sell_price": 12300,
            "buy_price": 12600,
        })

        self.add_seed("investments", {
            "bank_id": 2,
            "name": "btg",
            "itype": "fundo_imobiliário",
            "exempt": False,
            "sell_date": "2023-03-03",
            "buy_date": "2023-01-01",
            "price": 98,
            "rate": 0,
            "sell_price": 1300,
            "buy_price": 1500,
        })

        # Table profit_loss
        self.add_seed("profit_loss", {
            "customer_id": "44801389864",
            "day_trade_profit": 100,
            "swing_trade_profit": 100,
            "cripto_profit": 100,
            "fii_profit": 100,
            "day_trade_accumulated_loss": 0,
            "swing_trade_accumulated_loss": 0,
            "fii_accumulated_loss": 0,
            "cripto_accumulated_loss": 0,
            # "accumulated_loss": None,
            "generate_date": "2023-02-03",
            "taxes": 1000,
            "paid": "false"
        })

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

    def is_null(self, column: str) -> QueryConstructor:
        """Add a where clause for null values"""
        self.query += " AND {} IS NULL".format(column)
        return self

    def is_not_null(self, column: str) -> QueryConstructor:
        """Add a where clause for not null values"""
        self.query += " AND {} IS NOT NULL".format(column)
        return self

    def and_(self, column: str, operator: str, value: str) -> QueryConstructor:
        """Add an and clause"""
        if isinstance(value, str):
            value = "'{}'".format(value)

        if value is None:
            self.query += " AND {} IS NULL".format(column)
        else:
            self.query += " AND {} {} {}".format(column, operator, value)

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

    def insert(self, data: dict) -> QueryConstructor:
        """Insert data into a table"""
        self.query += "INSERT INTO {} ({}) VALUES ({})".format(
            self.table.__table__, ", ".join(data.keys()), ", ".join(["%s"] * len(data)))
        self.result = list(data.values())

        self.execute(tuple(data.values()))
        return self

    def update(self, data: dict) -> QueryConstructor:
        """Update data in a table"""
        self.query += " UPDATE {} SET {}".format(
            self.table.__table__, ", ".join(["{} = %s".format(key) for key in data.keys()]))
        self.result = list(data.values())

        self.execute(tuple(data.values()))
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
