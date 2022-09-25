import psycopg2
import sys
import boto3
import os

if __name__ == "__main__":  # Verify if the script is being executed directly
    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()


class Database:
    def __init__(self) -> None:
        try:
            print("Connecting to database...")
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
        try:
            # Open and read the file as a single buffer
            fd = open(filepath, 'r')
            sql_file = fd.read()
            fd.close()

            # All SQL commands (split on ';')
            sql_commands = sql_file.split(';')

            # Execute every command from the input file
            for command in sql_commands:
                if command.strip() != '':
                    self.conn.cursor().execute(command)
                    self.conn.commit()

        except Exception as e:
            print("Command skipped: {}".format(e))

    def setup(self) -> None:
        """Setup the database"""
        print("Setting up the database...")
        self.run_sql_from_file("src/database/sql_assets/schema.sql")
        print("Database setup complete!")

    def get_table(self, table_name: str) -> list:
        """Get a table from the database"""
        cur = self.conn.cursor()
        cur.execute("""SELECT * FROM {}""".format(table_name))
        query_results = cur.fetchall()
        return query_results

    def get_table_with_filter(self, table_name: str, filter: str) -> list:
        """Get a table from the database with a filter"""
        cur = self.conn.cursor()
        cur.execute("""SELECT * FROM {} WHERE {}""".format(table_name, filter))
        query_results = cur.fetchall()
        return query_results


if __name__ == "__main__":  # Verify if the script is being executed directly
    database = Database()  # Create a database object
    database.setup()  # Setup the database
