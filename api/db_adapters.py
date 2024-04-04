import os



"""
this adapter should folow PEP 249 – Python Database API Specification v2.0
https://peps.python.org/pep-0249/
"""


class PostgresDatabase:
    def __init__(self):
        self.db = self.get_connection_string()

    def get_connection_string(self):
        conn_string = f"postgres://{os.environ.get('SQL_DATABASE')}:{os.environ.get('SQL_PASSWORD')}@{os.environ.get('SQL_HOST')}/{os.environ.get('SQL_USER')}"
        return conn_string
    